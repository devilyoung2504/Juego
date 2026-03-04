from modes.fight_mode import FightMode

class ModeFactory:
    def __init__(self, services):
        self.services = services

    def create(self, mode_id: str):
        if mode_id == "fight":
            return FightMode(self.services)
        raise ValueError("Modo no soportado")