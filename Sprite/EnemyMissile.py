import pygame
import math
from Settings import Settings


class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, x, y, degree, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((200,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x_velocity, self.y_velocity = self.calculate_xy_velocity(degree, speed)
        self.settings = Settings()

    def update(self):
        # dispose if out of screen
        if self.rect.centerx < 0 or self.rect.centerx > self.settings.Width or self.rect.centery < 0 or self.rect.centery > self.settings.Height:
            self.kill()
        # moves at corresponding direction
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

    def calculate_xy_velocity(self, degree, speed):
        radian = math.radians(degree)
        return round(speed*math.cos(radian)), round(speed*math.sin(radian))
    
        