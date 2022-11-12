import pygame

from Sprite.Boss import Boss
from Sprite.Player import Player
from Settings import Settings

pygame.init()
Settings = Settings()
FPS = 60
pygame.display.set_caption("BulletHell")
screen = pygame.display.set_mode((Settings.Width, Settings.Height))
running = True
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
player = Player()
boss = Boss()
allSprites.add(player)
allSprites.add(boss)

while running:
    clock.tick(FPS)
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Info
    allSprites.update()

    #Render Graphics
    screen.fill((255,255,255))
    allSprites.draw(screen)
    pygame.display.update()
