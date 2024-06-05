import random

import pygame
import sys
from pygame.locals import *

if __name__ == "__main__":
    pygame.init()

    # Set up window and resources
    WIDTH = 1020
    HEIGHT = 720
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # Load images
    bg = pygame.image.load("bg.jpg").convert()  # Convert the background image for better performance
    bg = pygame.transform.scale(bg, (1280, 720))
    bird = pygame.image.load('bird.png').convert_alpha()
    bird = pygame.transform.scale(bird, (90, 90))  # Reduce the size of the bird image
    pipe = pygame.image.load('pipe.png').convert_alpha()
    pipe = pygame.transform.scale(pipe, (100, 320))  # Reduce the size of the pipe image
    pipe_r = pygame.image.load('pipe_r.png').convert_alpha()
    pipe_r = pygame.transform.scale(pipe_r, (100, 320))  # Reduce the size of the pipe image

    # Set up fonts
    bigg_font = pygame.font.Font(None, 64)  # Reduce font size for better performance
    big_font = pygame.font.Font(None, 32)  # Reduce font size for better performance

    # Set up game variables
    clock = pygame.time.Clock()
    running = True
    state = 0
    gravity = 0.5
    speed = 4
    bird_y = HEIGHT // 2
    score = 0
    control = 0
    # Create rectangles outside the loop
    pipe_rect = pipe.get_rect()
    pipe_r_rect = pipe_r.get_rect()

    while running:
        dt = clock.tick(60)  # Increase the frame rate for smoother gameplay

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    gravity = -4.5
                elif event.key == pygame.K_RETURN and state == 0:
                    pipe_x = [1430, 1275, 1120, 965, 810, 655, 500, 345, 190, 25]
                    pipe_x = [x + 700 for x in pipe_x]
                    pipe_y = [540, 540, 540, 540, 540, 540, 540, 540, 540, 540]
                    state = 1
                    bird_y = HEIGHT // 2
                    gravity = 2
                    score = 0
                elif event.key == pygame.K_RETURN and state == 3:
                    state = 0
            if event.type == pygame.QUIT:
                running = False

        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))

        if state == 0:
            # Display start screen
            name = bigg_font.render('Flappy Bird', True, (236, 0, 128))
            name_rect = name.get_rect(center=(WIDTH // 2, 90))
            WIN.blit(name, name_rect)

            name = big_font.render('Press Enter To Play', True, (236, 0, 128))
            name_rect = name.get_rect(center=(WIDTH // 2, 370))
            WIN.blit(name, name_rect)

        elif state == 1:
            # Update bird position
            bird_y += gravity
            gravity += 0.2
            bird_rect = bird.get_rect(center=(300, bird_y))

            # Update pipe positions
            for i in range(len(pipe_y)):
                pipe_x[i] -= speed
                if (score// 60) % 10 == 0 and (score // 60) != 0 and control == 0:
                    speed += 2
                    control = 1
                if (score // 60) % 11 == 0 and (score // 60) != 0 and control == 1:
                    control = 0
                if pipe_x[i] < -100:
                    pipe_x[i] += WIDTH + 560
                    pipe_y[i] = 400 + random.randint(0, 150)

                WIN.blit(pipe, (pipe_x[i], pipe_y[i]))
                WIN.blit(pipe_r, (pipe_x[i], pipe_y[i] - 600))

                # Update rectangle positions
                pipe_rect.topleft = (pipe_x[i], pipe_y[i])
                pipe_r_rect.topleft = (pipe_x[i], pipe_y[i] - 675)

                # Check collision
                if bird_rect.colliderect(pipe_rect) or bird_rect.colliderect(pipe_r_rect):
                    state = 3

            # Render bird
            WIN.blit(bird, (300, bird_y))

            # Increment score
            score += 1

            # Render score
            name = big_font.render(f'Score: {score // 60}', True, (236, 0, 128))  # Divided score by frame rate
            name_rect = name.get_rect(center=(WIDTH // 2, 50))
            WIN.blit(name, name_rect)

        elif state == 3:
            # Display game over screen
            name = bigg_font.render('Game Over', True, (236, 0, 128))
            name_rect = name.get_rect(center=(WIDTH // 2, 75))
            WIN.blit(name, name_rect)

            name = big_font.render(f'Score: {score // 60}', True, (236, 0, 128))  # Divided score by frame rate
            name_rect = name.get_rect(center=(WIDTH // 2, 360))
            WIN.blit(name, name_rect)

            name = big_font.render('Press Enter To Play', True, (236, 0, 128))
            name_rect = name.get_rect(center=(WIDTH // 2, 600))
            WIN.blit(name, name_rect)

        pygame.display.update()

    pygame.quit()
    sys.exit()