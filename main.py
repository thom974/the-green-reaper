# importing modules ---------------------------------------------#

import pygame
import math
import random

# setting up pygame ---------------------------------------------#

pygame.init()
pygame.display.set_caption('insert game title here')
size = (screen_width, screen_height) = (900,600)
screen = pygame.display.set_mode(size)
temp_display = pygame.Surface((300,300))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
FPS = 60

# helpful functions ---------------------------------------------#

def load_image(filename):
    surface = pygame.image.load('data/images/' + filename + '.png')
    surface.set_colorkey((0,0,0))  # remove black background
    return surface

# loading in game variables -------------------------------------#

green_block = load_image('ground_green')

# main loop -----------------------------------------------------#
while True:
    # Event detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # rendering map
    screen.blit(green_block,(0,0))

    pygame.display.flip()
    clock.tick(FPS)

