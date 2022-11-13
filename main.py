import os
import random
import pygame

from random import randint
from Settings import Settings
from Sprite.Boss import Boss
from Sprite.EnemyMissile import EnemyMissile
from Sprite.Explosion import Explosion
from Sprite.Player import Player

BOSS_SHOOT_EVENT = pygame.USEREVENT

pygame.init()
settings = Settings()
count = 0
pygame.display.set_caption("BulletHell")
screen = pygame.display.set_mode((settings.Width, settings.Height))
running = True
clock = pygame.time.Clock()

playerHpImage = pygame.image.load(os.path.join("Image", "PlayerHp.jpg")).convert()
playerHpImage_mini = pygame.transform.scale(playerHpImage, (25, 19))
playerHpImage_mini.set_colorkey((255,255,255))
pygame.display.set_icon(playerHpImage_mini)
playerBombImage = pygame.image.load(os.path.join("Image", "Bomb.jpg")).convert()
playerBombImage_mini = pygame.transform.scale(playerBombImage, (25, 19))
playerBombImage_mini.set_colorkey((255,255,255))
background = pygame.image.load(os.path.join("Image", "BG1.jpg")).convert()
background_enlarge = pygame.transform.scale(background, (1000, 1000))
background_red = pygame.transform.scale(background, (1000, 1000))
background_red.fill((200,0,255), special_flags=pygame.BLEND_MIN)

pygame.mixer.music.load(os.path.join("Sound","BGM1.mp3"))
pygame.mixer.music.set_volume(0.4)
shoot_sound = pygame.mixer.Sound(os.path.join("Sound","shoot.wav"))
shoot_sound.set_volume(0.1)
bomb_sound = pygame.mixer.Sound(os.path.join("Sound","expl0.wav"))
bomb_sound.set_volume(0.2)

allSprites = pygame.sprite.Group()
playerMissiles = pygame.sprite.Group()
enemyMissiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
boss = Boss()

allSprites.add(player)
allSprites.add(boss)
enemies.add(boss)

# setting custom event timers
pygame.time.set_timer(BOSS_SHOOT_EVENT, 100)

screen_shake = 0
red_effect = 0

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
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Boss: DIO', True, (100,100,100))
    textRect = text.get_rect()
    textRect.topleft = (x , y + 30)
    surf.blit(text, textRect)

while running:
    count += 1
    clock.tick(settings.FPS)

    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if player.use_bomb(enemyMissiles):
                    bomb_sound.play()
                    screen_shake = 30
        elif event.type == BOSS_SHOOT_EVENT:
            shoot_sound.play()
            boss_missiles = boss.shoot()
            allSprites.add(boss_missiles)
            enemyMissiles.add(boss_missiles)

    boss.shift_shooting_direction(0.1*clock.get_time())

    if count % 6 == 0:
        missile = player.shoot()
        allSprites.add(missile)
        playerMissiles.add(missile)
    if count % 100 == 0:
        missiles = boss.shoot_AllRound()
        allSprites.add(missiles)
        enemyMissiles.add(missiles)
    # changes num of missiles the boss shoots at a time
    if count % 300 == 0:
        boss.change_missile_count()
    
    # change boss movement
    if count % 400 == 0:
        boss.is_in_place = False
        # limit boss movement in upper bound
        new_target_x = randint(30, Settings.Width - 30)
        new_target_y = randint(30, Settings.Height // 3)
        boss.target = (new_target_x, new_target_y)

    # Update Info
    allSprites.update()
    hitsOnBoss = pygame.sprite.groupcollide(enemies, playerMissiles, False, True)
    for hitOnBoss in hitsOnBoss:
        for x in hitsOnBoss[hitOnBoss]:
            hitOnBoss.curHp -= 1
            expl = Explosion(x.rect.center, 'sm')
        allSprites.add(expl)
    hitOnPlayer = pygame.sprite.spritecollide(player, enemyMissiles, True)
    if hitOnPlayer:
        red_effect = 10
        screen_shake = 20
        player.Hp -= len(hitOnPlayer)

    #Render Graphics
    render_offset = [0,0]
    if screen_shake:
        screen_shake -= 1
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4
    if red_effect:
        red_effect -= 1
        screen.fill((255,0,0))
    screen.blit(background_enlarge, render_offset)
    allSprites.draw(screen)
    draw_player_health(screen, player.Hp, playerHpImage_mini, Settings.Height - 100, 50)
    draw_player_bomb(screen, player.BombCount, playerBombImage_mini, Settings.Height - 100, 100)
    draw_boss_health(screen, boss.curHp, boss.maxHp, 5, 15)
    pygame.display.update()

    # See if game ends