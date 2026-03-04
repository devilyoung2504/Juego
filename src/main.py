import sys
from pathlib import Path

import pygame

from core.factories import ModeFactory
from core.services import GameServices

INTERNAL_W, INTERNAL_H = 384, 216
FPS = 60

SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
ASSETS_DIR = ROOT_DIR / "assets" / "out"


def choose_integer_scale() -> int:
    info = pygame.display.Info()
    max_scale_w = max(1, info.current_w // INTERNAL_W)
    max_scale_h = max(1, info.current_h // INTERNAL_H)
    return max(1, min(max_scale_w, max_scale_h, 6))


class Game:
    def __init__(self):
        services = GameServices(ASSETS_DIR)
        factory = ModeFactory(services)
        self.mode = factory.create("fight", vs_cpu=True)
        self.mode.enter()

    def handle_event(self, event):
        self.mode.handle_event(event)

    def update(self, dt: float):
        self.mode.update(dt)

    def render(self, surf: pygame.Surface):
        self.mode.render(surf)


def main():
    pygame.init()
    pygame.display.set_caption("Juego - Laboratorio de patrones")

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

        scaled = pygame.transform.scale(internal, (INTERNAL_W * scale, INTERNAL_H * scale))
        window.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\n[ERROR]", error)
        print("ASSETS_DIR =", ASSETS_DIR)
        raise
