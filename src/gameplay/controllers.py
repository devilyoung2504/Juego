from abc import ABC, abstractmethod

import pygame

from gameplay.commands import AttackCommand, MoveCommand


class Controller(ABC):
    @abstractmethod
    def get_commands(self, dt: float):
        raise NotImplementedError


class HumanController(Controller):
    def __init__(self, left: int, right: int, attack: int):
        self.left = left
        self.right = right
        self.attack = attack

    def get_commands(self, dt: float):
        del dt
        keys = pygame.key.get_pressed()
        commands = []
        if keys[self.left]:
            commands.append(MoveCommand(-1))
        if keys[self.right]:
            commands.append(MoveCommand(1))
        if keys[self.attack]:
            commands.append(AttackCommand())
        return commands


class AIController(Controller):
    def __init__(self, self_actor, opponent, attack_range: float = 40):
        self.self_actor = self_actor
        self.opponent = opponent
        self.attack_range = attack_range

    def get_commands(self, dt: float):
        del dt
        commands = []
        dx = self.opponent.pos.x - self.self_actor.pos.x

        if abs(dx) > 8:
            commands.append(MoveCommand(1 if dx > 0 else -1))
        if abs(dx) < self.attack_range:
            commands.append(AttackCommand())

        return commands
