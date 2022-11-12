import pygame
import math
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
        self.Hp = 10
        self.shooting_direction = 0
        self.settings = Settings()

    def shoot(self):
        missiles = []

        for i in range(2):
            radian = math.pi*i + self.shooting_direction
            missiles.append(EnemyMissile(self.rect.centerx, self.rect.centery, radian, 2))
        return missiles
    
    def shift_shooting_direction(self, radian):
        self.shooting_direction += radian
