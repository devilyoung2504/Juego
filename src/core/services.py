from core.assets import AssetManager

class GameServices:
    def __init__(self, assets_dir):
        self.assets = AssetManager.get(assets_dir)