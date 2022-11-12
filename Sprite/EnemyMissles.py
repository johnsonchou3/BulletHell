import pygame
import math
from Settings import Settings


class EnemyMissle(pygame.sprite.Sprite):
    def __init__(self, x, y, radian, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((100,100,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x_velocity, self.y_velocity = self.calculate_xy_velocity(radian, speed)
        self.x_vel = 1
        self.y_vel = 1
        self.settings = Settings()

    def update(self):
        # dispose if out of screen
        if not self.game.screen.get_rect().contains(self.rect):
            self.kill()

        # moves at corresponding direction
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

    def calculate_xy_velocity(self, radian, speed):
            return math.ceil(speed*math.cos(radian)), math.ceil(speed*math.sin(radian))
    
        