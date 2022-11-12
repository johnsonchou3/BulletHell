import os
import random
from random import randint
import pygame

from Sprite.Boss import Boss
from Sprite.EnemyMissile import EnemyMissile
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

playerHpImage = pygame.image.load(os.path.join("Image", "PlayerHp.jpg")).convert()
playerHpImage_mini = pygame.transform.scale(playerHpImage, (25, 19))
playerHpImage_mini.set_colorkey((255,255,255))
pygame.display.set_icon(playerHpImage_mini)
playerBombImage = pygame.image.load(os.path.join("Image", "Bomb.jpg")).convert()
playerBombImage_mini = pygame.transform.scale(playerBombImage, (25, 19))
playerBombImage_mini.set_colorkey((255,255,255))
background = pygame.image.load(os.path.join("Image", "background.png")).convert()
background_enlarge = pygame.transform.scale(background, (1000, 1000))

pygame.mixer.music.load(os.path.join("Sound","BGM1.mp3"))
pygame.mixer.music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound(os.path.join("Sound","shoot.wav"))
shoot_sound.set_volume(0.1)

allSprites = pygame.sprite.Group()
playerMissiles = pygame.sprite.Group()
enemyMissiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
boss = Boss()

allSprites.add(player)
allSprites.add(boss)
enemies.add(boss)

screen_shake = 0

pygame.mixer.music.play(-1)
def draw_player_health(surface, hp, img, x, y):
    for i in range(hp):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surface.blit(img, img_rect)

def draw_player_bomb(surface, bombCount, img, x, y):
    for i in range(bombCount):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surface.blit(img, img_rect)

def draw_boss_health(surf, hp, maxHp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/maxHp)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0,255,0), fill_rect)
    pygame.draw.rect(surf, (255,255,255), outline_rect, 2)

while running:
    count += 1
    dt = clock.tick(FPS)

    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #   if event.key == pygame.K_SPACE:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if player.use_bomb(enemyMissiles):
                    screen_shake = 30

    boss.shift_shooting_direction(0.1*clock.get_time())
    if count % 4 == 0:
        shoot_sound.play()
        boss_missiles = boss.shoot()
        allSprites.add(boss_missiles)
        enemyMissiles.add(boss_missiles)
    if count % 6 == 0:
        missile = player.shoot()
        allSprites.add(missile)
        playerMissiles.add(missile)
    
    # changes num of missiles the boss shoots at a time
    if count % 300 == 0:
        boss.change_missile_count()

    # Update Info
    allSprites.update()
    hitsOnBoss = pygame.sprite.groupcollide(enemies, playerMissiles, False, True)
    boss.curHp -= len(hitsOnBoss)
    hitOnPlayer = pygame.sprite.spritecollide(player, enemyMissiles, True)
    player.Hp -= len(hitOnPlayer)

    #Render Graphics
    if screen_shake:
        screen_shake -= 1
    render_offset = [0,0]
    if screen_shake:
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4

    screen.blit(background_enlarge, render_offset)
    allSprites.draw(screen)
    draw_player_health(screen, player.Hp, playerHpImage_mini, Settings.Height - 100, 50)
    draw_player_bomb(screen, player.BombCount, playerBombImage_mini, Settings.Height - 100, 100)
    draw_boss_health(screen, boss.curHp, boss.maxHp, 5, 15)
    pygame.display.update()

    # See if game ends
    if boss.curHp == 0 or player.Hp == 0:
        running = False

