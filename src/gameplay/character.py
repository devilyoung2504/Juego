import pygame


class Character:
    def __init__(self, sprite: pygame.Surface, pos: pygame.Vector2, speed: float = 90.0, hp: int = 100, base_damage: int = 10):
        self.sprite = sprite
        self.pos = pos
        self.speed = speed
        self.hp = hp
        self.base_damage = base_damage

        self.attack_cooldown = 0.0
        self.attack_cooldown_max = 0.35

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.sprite.get_width(), self.sprite.get_height())

    def try_attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = self.attack_cooldown_max

    def damage(self) -> int:
        return self.base_damage

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    def update(self, dt: float):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprite, (int(self.pos.x), int(self.pos.y)))


class CharacterDecorator:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, item):
        return getattr(self.wrapped, item)

    def damage(self) -> int:
        return self.wrapped.damage()

    def take_damage(self, amount: int):
        return self.wrapped.take_damage(amount)


class DamageBoost(CharacterDecorator):
    def damage(self) -> int:
        return self.wrapped.damage() + 5


class Shield(CharacterDecorator):
    def take_damage(self, amount: int):
        reduced = max(0, amount - 3)
        return self.wrapped.take_damage(reduced)
