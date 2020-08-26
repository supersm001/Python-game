import pygame
import math
import random
from pygame import mixer
# create screen
pygame.init()
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('discovery.mp3')
mixer.music.play(-1)

# title
pygame.display.set_caption("space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 20

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(30, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
# ready can't see bullet
# the bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


# game over text
over_font = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render("SCORE :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 23, y + 10))


def isCollission(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 30:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# if key stroke pressed check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x coordinates of space ship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

# checking boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730

# enemy movement
    for i in range(num_of_enemy):
        # game over
        if enemyY[i] > 370:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 700:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollission(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            blow_sound = mixer.Sound('blow.wav')
            blow_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(30, 150)
        enemy(enemyX[i], enemyY[i], i)
# bullet movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
