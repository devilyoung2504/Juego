import pygame

from gameplay.character import Character, DamageBoost, Shield
from gameplay.controllers import AIController, HumanController


class GameMode:
    def enter(self):
        pass

    def exit(self):
        pass

    def handle_event(self, event):
        del event

    def update(self, dt):
        del dt

    def render(self, surf):
        del surf


class PlayerSlot:
    def __init__(self, index: int, character, controller):
        self.index = index
        self.character = character
        self.controller = controller

    def update(self, dt: float):
        for command in self.controller.get_commands(dt):
            command.execute(self.character, dt)
        self.character.update(dt)


class FightMode(GameMode):
    BG_FILE = "bg_arena.png"
    P1_FILE = "PJ1_right.png"
    P2_FILE = "PJ2_left.png"
    CHAR_TARGET_H = 96
    INTERNAL_W = 384
    INTERNAL_H = 216

    def __init__(self, services, vs_cpu: bool = True):
        self.services = services
        self.vs_cpu = vs_cpu
        self.bg = None
        self.p1 = None
        self.p2 = None
        self.slots = []
        self.floor_y = 190

    def enter(self):
        self.bg = self.services.assets.image(self.BG_FILE)
        if self.bg.get_size() != (self.INTERNAL_W, self.INTERNAL_H):
            self.bg = pygame.transform.scale(self.bg, (self.INTERNAL_W, self.INTERNAL_H))

        p1_sprite = self.services.scale_to_height(self.services.assets.image(self.P1_FILE), self.CHAR_TARGET_H)
        p2_sprite = self.services.scale_to_height(self.services.assets.image(self.P2_FILE), self.CHAR_TARGET_H)

        p1_pos = pygame.Vector2(90, self.floor_y - p1_sprite.get_height())
        p2_pos = pygame.Vector2(250, self.floor_y - p2_sprite.get_height())

        self.p1 = DamageBoost(Character(p1_sprite, p1_pos, speed=95))
        self.p2 = Shield(Character(p2_sprite, p2_pos, speed=90))

        c1 = HumanController(pygame.K_a, pygame.K_d, pygame.K_f)
        c2 = AIController(self.p2, self.p1) if self.vs_cpu else HumanController(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL)

        self.slots = [
            PlayerSlot(1, self.p1, c1),
            PlayerSlot(2, self.p2, c2),
        ]

    def update(self, dt: float):
        for slot in self.slots:
            slot.update(dt)

        for char in (self.p1, self.p2):
            char.pos.x = self.services.clamp(char.pos.x, 0, self.INTERNAL_W - char.sprite.get_width())
            char.pos.y = self.services.clamp(char.pos.y, 0, self.INTERNAL_H - char.sprite.get_height())

    def render(self, surf: pygame.Surface):
        surf.blit(self.bg, (0, 0))
        self.p1.draw(surf)
        self.p2.draw(surf)

        font = pygame.font.Font(None, 18)
        p1_text = font.render(f"P1 HP:{self.p1.hp} DMG:{self.p1.damage()}", True, (255, 255, 255))
        p2_label = "CPU" if self.vs_cpu else "P2"
        p2_text = font.render(f"{p2_label} HP:{self.p2.hp} DMG:{self.p2.damage()}", True, (255, 255, 255))
        surf.blit(p1_text, (6, 6))
        surf.blit(p2_text, (6, 22))
