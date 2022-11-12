import pygame
from Settings import Settings
from Sprite.PlayerMissile import PlayerMissile


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = (500,500)
        self.settings = Settings()
        self.Hp = 3
        self.BombCount = 3

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] and self.rect.right <= self.settings.Width:
            if key_pressed[pygame.K_LSHIFT] :
                self.rect.x += 2
            else:
                self.rect.x += 5
        if key_pressed[pygame.K_LEFT] and self.rect.left >= 0:
            if key_pressed[pygame.K_LSHIFT] :
                self.rect.x -= 2
            else:
                self.rect.x -= 5
        if key_pressed[pygame.K_DOWN] and self.rect.bottom <= self.settings.Height:
            if key_pressed[pygame.K_LSHIFT] :
                self.rect.y += 2
            else:
                self.rect.y += 5
        if key_pressed[pygame.K_UP] and self.rect.top >= 0:
            if key_pressed[pygame.K_LSHIFT] :
                self.rect.y -= 2
            else:
                self.rect.y -= 5
    def shoot(self):
        missle = PlayerMissile(self.rect.centerx, self.rect.top)
        return missle

    def use_bomb(self, enemyMissles):
        if self.BombCount > 0:
            for missles in enemyMissles:
                missles.kill()
            self.BombCount -= 1
            return True
        else:
            return False
