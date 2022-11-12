import os
from random import randint
import pygame
import math
from math import pi
from Settings import Settings
from Sprite.EnemyMissile import EnemyMissile


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

