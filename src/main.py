import sys
from pathlib import Path
import pygame

# =================== CONFIG ===================
INTERNAL_W, INTERNAL_H = 384, 216
FPS = 60

# Assets esperados en assets/out/
BG_FILE = "bg_arena.png"
P1_FILE = "PJ1_right.png"
P2_FILE = "PJ2_left.png"

# Si tus sprites en out/ quedaron grandes, aquí fuerzas altura interna
CHAR_TARGET_H = 96  # píxeles dentro de 384x216


# =================== PATHS ===================
SRC_DIR = Path(__file__).resolve().parent          # .../Juego/src
ROOT_DIR = SRC_DIR.parent                          # .../Juego
ASSETS_DIR = ROOT_DIR / "assets" / "out"           # .../Juego/assets/out


# =================== HELPERS ===================
def load_image(name: str) -> pygame.Surface:
    path = ASSETS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Falta asset: {path}")
    return pygame.image.load(str(path)).convert_alpha()


def scale_to_height(img: pygame.Surface, target_h: int) -> pygame.Surface:
    """Escala con nearest-neighbor (pixel-art friendly)."""
    w, h = img.get_width(), img.get_height()
    if h == target_h:
        return img
    scale = target_h / h
    new_w = max(1, int(w * scale))
    return pygame.transform.scale(img, (new_w, target_h))


def choose_integer_scale() -> int:
    """Escalado entero para evitar blur."""
    info = pygame.display.Info()
    max_scale_w = max(1, info.current_w // INTERNAL_W)
    max_scale_h = max(1, info.current_h // INTERNAL_H)
    return max(1, min(max_scale_w, max_scale_h, 6))  # cap 6 para no explotar tamaño


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# =================== COMMANDS (simple) ===================
class Command:
    def execute(self, actor, dt: float):
        pass


class MoveCommand(Command):
    def __init__(self, dx: float):
        self.dx = dx

    def execute(self, actor, dt: float):
        actor.pos.x += self.dx * actor.speed * dt


class AttackCommand(Command):
    def execute(self, actor, dt: float):
        actor.try_attack()


# =================== CONTROLLERS (Strategy) ===================
class Controller:
    def get_commands(self, dt: float):
        return []


class HumanController(Controller):
    def __init__(self, left, right, attack):
        self.left = left
        self.right = right
        self.attack = attack

    def get_commands(self, dt: float):
        keys = pygame.key.get_pressed()
        cmds = []
        if keys[self.left]:
            cmds.append(MoveCommand(-1))
        if keys[self.right]:
            cmds.append(MoveCommand(+1))
        if keys[self.attack]:
            cmds.append(AttackCommand())
        return cmds


class AIController(Controller):
    """
    IA muy simple:
    - persigue al oponente
    - cuando está cerca, intenta atacar
    """
    def __init__(self, self_actor, opponent):
        self.self_actor = self_actor
        self.opponent = opponent
        self.attack_range = 40

    def get_commands(self, dt: float):
        cmds = []
        dx = self.opponent.pos.x - self.self_actor.pos.x

        if abs(dx) > 8:
            cmds.append(MoveCommand(1 if dx > 0 else -1))

        if abs(dx) < self.attack_range:
            cmds.append(AttackCommand())

        return cmds


# =================== ENTITIES ===================
class Character:
    def __init__(self, sprite: pygame.Surface, pos: pygame.Vector2, speed: float = 90.0, hp: int = 100):
        self.sprite = sprite
        self.pos = pos
        self.speed = speed
        self.hp = hp

        self.attack_cooldown = 0.0
        self.attack_cooldown_max = 0.35  # segundos

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.sprite.get_width(), self.sprite.get_height())

    def try_attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = self.attack_cooldown_max

    def update(self, dt: float):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprite, (int(self.pos.x), int(self.pos.y)))


class PlayerSlot:
    def __init__(self, index: int, character: Character, controller: Controller):
        self.index = index
        self.character = character
        self.controller = controller

    def update(self, dt: float):
        cmds = self.controller.get_commands(dt)
        for c in cmds:
            c.execute(self.character, dt)
        self.character.update(dt)


# =================== MODE (State) ===================
class GameMode:
    def enter(self): pass
    def exit(self): pass
    def handle_event(self, event): pass
    def update(self, dt): pass
    def render(self, surf): pass


class FightMode(GameMode):
    def __init__(self, vs_cpu=True):
        self.vs_cpu = vs_cpu
        self.bg = None
        self.p1 = None
        self.p2 = None
        self.slots = []

        # “piso” (ajústalo a ojo según tu fondo)
        self.floor_y = 190

    def enter(self):
        # Fondo
        self.bg = load_image(BG_FILE)
        if self.bg.get_size() != (INTERNAL_W, INTERNAL_H):
            self.bg = pygame.transform.scale(self.bg, (INTERNAL_W, INTERNAL_H))

        # Sprites (por si vienen grandes)
        p1_sprite = scale_to_height(load_image(P1_FILE), CHAR_TARGET_H)
        p2_sprite = scale_to_height(load_image(P2_FILE), CHAR_TARGET_H)

        # Personajes: los “paras” sobre el piso
        p1_pos = pygame.Vector2(90,  self.floor_y - p1_sprite.get_height())
        p2_pos = pygame.Vector2(250, self.floor_y - p2_sprite.get_height())

        self.p1 = Character(p1_sprite, p1_pos, speed=95)
        self.p2 = Character(p2_sprite, p2_pos, speed=90)

        # Controllers
        c1 = HumanController(pygame.K_a, pygame.K_d, pygame.K_f)  # A/D moverse, F atacar

        if self.vs_cpu:
            c2 = AIController(self.p2, self.p1)
        else:
            c2 = HumanController(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL)  # Flechas + Ctrl derecho

        self.slots = [
            PlayerSlot(1, self.p1, c1),
            PlayerSlot(2, self.p2, c2),
        ]

        print("[OK] FightMode cargado.")
        print("BG:", self.bg.get_size(), "P1:", self.p1.sprite.get_size(), "P2:", self.p2.sprite.get_size())

    def update(self, dt: float):
        for s in self.slots:
            s.update(dt)

        # límites para no salirse del escenario
        for ch in (self.p1, self.p2):
            ch.pos.x = clamp(ch.pos.x, 0, INTERNAL_W - ch.sprite.get_width())
            ch.pos.y = clamp(ch.pos.y, 0, INTERNAL_H - ch.sprite.get_height())

    def render(self, surf: pygame.Surface):
        surf.blit(self.bg, (0, 0))

        # dibuja primero el que está “más atrás” (y más arriba) si quieres
        # aquí da igual, es solo demo
        self.p1.draw(surf)
        self.p2.draw(surf)

        # debug básico (vida/cooldown)
        # (si no quieres texto, bórralo)
        font = pygame.font.Font(None, 18)
        t1 = font.render(f"P1 HP:{self.p1.hp}", True, (255,255,255))
        t2 = font.render(f"P2 HP:{self.p2.hp} {'CPU' if self.vs_cpu else ''}", True, (255,255,255))
        surf.blit(t1, (6, 6))
        surf.blit(t2, (6, 22))


# =================== GAME MANAGER ===================
class Game:
    def __init__(self):
        self.mode: GameMode = FightMode(vs_cpu=True)
        self.mode.enter()

    def handle_event(self, event):
        self.mode.handle_event(event)

    def update(self, dt: float):
        self.mode.update(dt)

    def render(self, surf: pygame.Surface):
        self.mode.render(surf)


# =================== MAIN ===================
def main():
    pygame.init()
    pygame.display.set_caption("Juego - Base Pygame (PixelArt 384x216)")

    # escala entero automático según tu pantalla
    scale = choose_integer_scale()
    window = pygame.display.set_mode((INTERNAL_W * scale, INTERNAL_H * scale))
    internal = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)

    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            game.handle_event(event)

        game.update(dt)

        internal.fill((0, 0, 0, 0))
        game.render(internal)

        # escalado pixel-perfect (NO smoothscale)
        scaled = pygame.transform.scale(internal, (INTERNAL_W * scale, INTERNAL_H * scale))
        window.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n[ERROR]", e)
        print("ASSETS_DIR =", ASSETS_DIR)
        raise