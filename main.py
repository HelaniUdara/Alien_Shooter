import pygame
import random
import math
from pygame import mixer

pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Alien Shooter")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')
# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImage = pygame.image.load('spaceship .png')
playerX = 368
playerY = 480
playerX_Change = 0

# Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 150))
    enemyX_Change.append(2.5)
    enemyY_Change.append(30)

# Bullet
# Ready - Can't see the bullet
# Fire  - The bullet is currently moving
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_Change = 5
bullet_state = "ready"

# Score
score_value = 0

textX = 10
textY = 10

# Game Over Text
gameOver_font = pygame.font.Font('freesansbold.ttf', 64)
over = False

def show_score(x, y, isGameOver):
    if isGameOver == True:
        font = pygame.font.Font('freesansbold.ttf', 48)
    else:
        font = pygame.font.Font('freesansbold.ttf', 32)

    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = gameOver_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# Drawing the player in the given position
def player(x, y):
    screen.blit(playerImage, (x, y))


# Drawing the enemy in the given position
def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # for loop is for catching all the events to pygame.event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # changing player's X position
    playerX += playerX_Change
    # Set boundaries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            over = True
            break

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 2.5
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -2.5
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    if over == True:
        show_score(300, 350, True)
    else:
        show_score(textX, textY, False)
    pygame.display.update()
