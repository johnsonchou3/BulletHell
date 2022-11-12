import pygame
from Settings import Settings


class EnemyMissle:
    def __init__(self, x, y, xVel, yVel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((100,100,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.settings = Settings()
        self.xVelocity = xVel
        self.xVelocity = yVel

        def update(self):
            # moves at corresponding direction