import os.path
import pygame
from Settings import Settings

class PlayerMissile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.image = pygame.image.load(os.path.join(self.settings.image_dir, "PlayerMissile.png")).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.yVelocity = -10

    def update(self):
        self.rect.y += self.yVelocity
        if self.rect.bottom < 0:
            self.kill()

