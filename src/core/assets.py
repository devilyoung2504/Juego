import pygame

class AssetManager:
    _instance = None

    def __init__(self, assets_dir):
        self.assets_dir = assets_dir
        self._images = {}

    @classmethod
    def get(cls, assets_dir):
        if cls._instance is None:
            cls._instance = cls(assets_dir)
        return cls._instance

    def image(self, name):
        if name not in self._images:
            path = f"{self.assets_dir}/{name}"
            self._images[name] = pygame.image.load(path).convert_alpha()
        return self._images[name]