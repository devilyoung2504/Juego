from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, actor, dt: float) -> None:
        raise NotImplementedError


class MoveCommand(Command):
    def __init__(self, direction: float):
        self.direction = direction

    def execute(self, actor, dt: float) -> None:
        actor.pos.x += self.direction * actor.speed * dt


class AttackCommand(Command):
    def execute(self, actor, dt: float) -> None:
        actor.try_attack()
