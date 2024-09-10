import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 800

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Game settings
gravity = 0.20
bird_movement = 0.5
game_active = True
score = 0

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Load and scale images
bird_image = pygame.image.load('bird.png').convert_alpha()
bird_image = pygame.transform.scale(bird_image, (50, 35))
bird_rect = bird_image.get_rect(center=(100, screen_height // 2))

pipe_surface = pygame.image.load('pipe.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (50, 300))

# Load fonts
game_font = pygame.font.Font(None, 40)

# Function to create pipes
def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = pipe_surface.get_rect(midtop=(screen_width + 50, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(screen_width + 50, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Function to check collisions
def check_collision(pipes):
    global game_active
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -25 or bird_rect.bottom >= screen_height:
        return False
    return True

# Function to display score
def display_score():
    score_surface = game_font.render(f'Score: {int(score)}', True, black)
    score_rect = score_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(score_surface, score_rect)

# Function to handle game over
def game_over():
    game_over_surface = game_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_surface, game_over_rect)

# Pipe settings
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, screen_height // 2)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.fill(white)

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_image, bird_rect)

        # Pipe movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Check collision
        game_active = check_collision(pipe_list)

        # Update score
        score += 0.01
        display_score()
    else:
        game_over()

    pygame.display.update()
    clock.tick(120)

pygame.quit()