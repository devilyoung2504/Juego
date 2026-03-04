from pathlib import Path

import pygame


class AssetManager:
    """Singleton para cachear assets gráficos."""

    _instance = None

    def __init__(self, assets_dir: Path):
        self.assets_dir = Path(assets_dir)
        self._images: dict[str, pygame.Surface] = {}

    @classmethod
    def get(cls, assets_dir: Path) -> "AssetManager":
        if cls._instance is None:
            cls._instance = cls(assets_dir)
        return cls._instance

    def image(self, name: str) -> pygame.Surface:
        if name not in self._images:
            path = self.assets_dir / name
            if not path.exists():
                raise FileNotFoundError(f"Falta asset: {path}")
            self._images[name] = pygame.image.load(str(path)).convert_alpha()
        return self._images[name]
