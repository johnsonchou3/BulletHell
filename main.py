import os
import random
from random import randint
import pygame

from Sprite.Boss import Boss
from Sprite.EnemyMissile import EnemyMissile
from Sprite.Explosion import Explosion
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
background = pygame.image.load(os.path.join("Image", "BG1.jpg")).convert()
background_enlarge = pygame.transform.scale(background, (1000, 1000))

init_background = pygame.image.load(os.path.join("Image", "BG3.jpg")).convert()
init_background_enlarge = pygame.transform.scale(init_background, (1000, 1000))


pygame.mixer.music.load(os.path.join("Sound","BGM1.mp3"))
pygame.mixer.music.set_volume(0.4)
shoot_sound = pygame.mixer.Sound(os.path.join("Sound","shoot.wav"))
shoot_sound.set_volume(0.1)
bomb_sound = pygame.mixer.Sound(os.path.join("Sound","expl0.wav"))
bomb_sound.set_volume(0.2)

screen_shake = 0
red_effect = 0
show_init = True
dead = False


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

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
def draw_init():
    screen.blit(init_background_enlarge, (0,0))
    draw_text(screen, 'Bullet Hell', 64, Settings.Width/2, Settings.Height/4)
    draw_text(screen, 'Press direction key to move, use with shift to move slowly ', 22, Settings.Width/2, Settings.Height/2)
    draw_text(screen, 'Press Z to use bomb to eliminate enemy missiles ', 22, Settings.Width/2, Settings.Height/2 + 50)
    draw_text(screen, 'Press any key to start', 18, Settings.Width/2, Settings.Height*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # Get Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False
                pygame.mixer.music.play(-1)

while running:
    if show_init:
        draw_init()
        show_init = False
        allSprites = pygame.sprite.Group()
        playerMissiles = pygame.sprite.Group()
        enemyMissiles = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = Player()
        boss = Boss()

        allSprites.add(player)
        allSprites.add(boss)
        enemies.add(boss)
    count += 1
    dt = clock.tick(FPS)
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if player.use_bomb(enemyMissiles):
                    bomb_sound.play()
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
    if player.Hp == 0:
        dead = True