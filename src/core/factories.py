from modes.fight_mode import FightMode


class ModeFactory:
    def __init__(self, services):
        self.services = services

    def create(self, mode_id: str, **kwargs):
        if mode_id == "fight":
            return FightMode(self.services, **kwargs)
        raise ValueError(f"Modo no soportado: {mode_id}")
