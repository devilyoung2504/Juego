from pathlib import Path

import pygame

from core.assets import AssetManager


class GameServices:
    """Facade de servicios compartidos del juego."""

    def __init__(self, assets_dir: Path):
        self.assets = AssetManager.get(assets_dir)

    @staticmethod
    def scale_to_height(img: pygame.Surface, target_h: int) -> pygame.Surface:
        w, h = img.get_width(), img.get_height()
        if h == target_h:
            return img
        scale = target_h / h
        new_w = max(1, int(w * scale))
        return pygame.transform.scale(img, (new_w, target_h))

    @staticmethod
    def clamp(value: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, value))
