import os
from random import randint
import pygame
from Settings import Settings
from Sprite.EnemyMissile import EnemyMissile
from pygame.math import Vector2

MAX_FORCE = 0.1
MAX_SPEED = 3

class Boss(pygame.sprite.Sprite):
    settings = Settings()
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (500,100)
        self.maxHp = 500
        self.curHp = self.maxHp
        self.missile_count = 2
        self.shooting_direction = 0
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.target = (300, 50)
        self.settings = Settings()

    def shoot(self):
        missiles = []
        missiles_angle_offset = 360 / self.missile_count
        for i in range(self.missile_count):
            degree = i * missiles_angle_offset + self.shooting_direction
            missiles.append(EnemyMissile(pygame.image.load(os.path.join("Image", "MissileRed.png")).convert(), self.rect.centerx, self.rect.centery, degree, 5))
        return missiles
    
    def shift_shooting_direction(self, degree):
        self.shooting_direction += degree
        self.shooting_direction % 360

    def change_missile_count(self):
        self.missile_count = randint(2, 6)

    def shoot_AllRound(self):
        missiles = []
        for i in range(360):
            degree = i
            missiles.append(EnemyMissile(pygame.image.load(os.path.join("Image", "ArrowMissileGreen.png")).convert(), self.rect.centerx, self.rect.centery, degree, 2))
        return missiles

    def seek(self, target):
        position = Vector2(self.rect.centerx, self.rect.centery)

        # avoid normalizing by zero
        if (target - position).length() == 0:
            return (0, 0)

        desired = (target - position).normalize() * MAX_SPEED
        steer = desired - self.velocity
        return steer

    def update(self):
        self.acceleration = self.seek(self.target)
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y