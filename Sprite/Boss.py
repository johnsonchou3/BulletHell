import pygame
from Settings import Settings


class Boss(pygame.sprite.Sprite):
    settings = Settings()
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (500,100)
        self.settings = Settings()
        self.Hp = 10

