import pygame


class PlayerMissile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((0,200,100))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.yVelocity = -10

    def update(self):
        self.rect.y += self.yVelocity
        if self.rect.bottom < 0:
            self.kill()