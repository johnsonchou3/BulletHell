import os

import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.expl_anim = {}
        self.expl_anim['lg'] = []
        self.expl_anim['sm'] = []
        self.expl_anim['player'] = []
        for i in range(9):
            expl_img = pygame.image.load(os.path.join("Image", f"expl{i}.png")).convert()
            expl_img.set_colorkey((0, 0, 0))
            self.expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
            self.expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
            player_expl_img = pygame.image.load(os.path.join("Image", f"player_expl{i}.png")).convert()
            player_expl_img.set_colorkey((0, 0, 0))
            self.expl_anim['player'].append(player_expl_img)
        self.image = self.expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                self.image = self.expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center