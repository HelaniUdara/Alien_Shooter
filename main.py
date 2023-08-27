import pygame
import random

pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Alien Shooter")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Player
playerImage = pygame.image.load('spaceship .png')
playerX = 368
playerY = 480
playerX_Change = 0

# Enemy
enemyImage = pygame.image.load('monster.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(30, 150)
enemyX_Change = 3
enemyY_Change = 30

# Bullet
# Ready - Can't see the bullet
# Fire  - The bullet is currently moving
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_Change = 5
bullet_state = "ready"


# Drawing the player in the given position
def player(x, y):
    screen.blit(playerImage, (x, y))


# Drawing the enemy in the given position
def enemy(x, y):
    screen.blit(enemyImage, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

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

    # changing enemy's X position
    enemyX += enemyX_Change
    # Set boundaries for enemy and changing the y position when hit the boundary
    if enemyX <= 0:
        enemyX_Change = 3
        enemyY += enemyY_Change
    elif enemyX >= 736:
        enemyX_Change = -3
        enemyY += enemyY_Change

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_Change


    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
