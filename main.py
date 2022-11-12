import pygame

from Sprite.Boss import Boss
from Sprite.Player import Player
from Settings import Settings
pygame.init()
Settings = Settings()
FPS = 60
count = 0
pygame.display.set_caption("BulletHell")
screen = pygame.display.set_mode((Settings.Width, Settings.Height))
running = True
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
playerMissles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
boss = Boss()
allSprites.add(player)
allSprites.add(boss)
enemies.add(boss)
while running:
    count += 1
    clock.tick(FPS)
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #   if event.key == pygame.K_SPACE:
    if count % 4 == 0:
        missle = player.shoot()
        allSprites.add(missle)
        playerMissles.add(missle)
    # Update Info
    allSprites.update()
    hitsOnBoss = pygame.sprite.groupcollide(enemies, playerMissles, False, True)
    for hit in hitsOnBoss:
        boss.Hp -= 1
        if boss.Hp == 0:
            running = False

    #Render Graphics
    screen.fill((255,255,255))
    allSprites.draw(screen)
    pygame.display.update()

