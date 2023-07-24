import pygame
import os

# Initialize Pygame modules
pygame.font.init()
pygame.mixer.init()

# Set up the game window
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set up game elements and constants
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
VEL = 5
BULLETS_VEL = 10
FPS = 60
MAX_BULLETS = 2000
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load spaceship images and background image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Set up fonts for health and winner display
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Function to draw the game window
def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullets in red_bullets:
        pygame.draw.rect(WIN, RED, bullets)

    for bullets in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullets)

    pygame.display.update()

# Function to handle yellow player movement
def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

# Function to handle red player movement
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

# Function to handle bullets
def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    bullets_to_remove = []

    for bullets in yellow_bullets:
        bullets.x += BULLETS_VEL
        if red.colliderect(bullets):
            pygame.event.post(pygame.event.Event(RED_HIT))
            bullets_to_remove.append(bullets)

    for bullets in red_bullets:
        bullets.x -= BULLETS_VEL
        if yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            bullets_to_remove.append(bullets)

    for bullets in bullets_to_remove:
        if bullets in yellow_bullets:
            yellow_bullets.remove(bullets)
        elif bullets in red_bullets:
            red_bullets.remove(bullets)

# Function to display the winner
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# Function to check if either player has reached the maximum bullets limit
def b_z(red_bullets, yellow_bullets):
    if len(red_bullets) >= MAX_BULLETS:
        winner_text = "YELLOW WON"
        draw_winner(winner_text)

    if len(yellow_bullets) >= MAX_BULLETS:
        winner_text = "RED WON"
        draw_winner(winner_text)

# Main game loop
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullets = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullets)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullets = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullets)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if yellow_health <= 0:
            winner_text = "RED WON"

        if red_health <= 0:
            winner_text = "YELLOW WON"

        if winner_text != "":
            draw_winner(winner_text)
            break  # SOMEONE WON

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health)
        b_z(red_bullets, yellow_bullets)

    main()

if __name__ == "__main__":
    main()
