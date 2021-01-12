# importing modules ---------------------------------------------#

import pygame
import math
import random
import sys

import data.scripts.math_functions as m

# setting up pygame ---------------------------------------------#

pygame.init()
pygame.display.set_caption('insert game title here')
size = (screen_width, screen_height) = (900,600)
screen = pygame.display.set_mode(size)
temp_display = pygame.Surface((300,300))
clock = pygame.time.Clock()
# pygame.mouse.set_visible(False)
FPS = 60

# helpful functions ---------------------------------------------#


def load_image(filename):
    surface = pygame.image.load('data/images/' + filename + '.png')
    surface.set_colorkey((0,0,0))  # remove black background
    return surface

# loading in game variables -------------------------------------#


game_scroll = [0,0]

green_block = load_image('ground_green').convert()
green_block = pygame.transform.scale(green_block,(101,170))
bv = 51

character = load_image('character').convert()
char_x, char_y = (100,100)
char_speed = 3
char_up = False
char_down = False
char_left = False
char_right = False
char_jump = False
char_fall = False
char_acceleration = 0
char_prev_pos = 0
shadow_col = pygame.Color(255, 0, 0, a=200)

f = open('data/maps/map_one.txt','r')
map_one_data = [[tile for tile in tile_row.rstrip("\n")] for tile_row in f]
osu_font = pygame.font.Font('data/Aller_Bd.ttf', 30)

# main loop -----------------------------------------------------#
while True:
    # some variables
    blocks = []

    # background
    screen.fill((255, 255, 255))

    # control game scroll
    game_scroll[0] += (char_x - game_scroll[0] - 450 + 37) / 20
    game_scroll[1] += (char_y - game_scroll[1] - 300 + 50) / 20

    # to display mouse coordinates
    mx, my = pygame.mouse.get_pos()
    text = osu_font.render(str(mx) + ", " + str(my), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (800, 40)

    # event detection -----------------------------------------------------#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                char_up = True
            if event.key == pygame.K_s:
                char_down = True
            if event.key == pygame.K_a:
                char_left = True
            if event.key == pygame.K_d:
                char_right = True
            if event.key == pygame.K_SPACE and char_jump is False and char_fall is False:
                char_prev_ypos = char_y
                char_jump = True
                char_acceleration = 20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                char_up = False
            if event.key == pygame.K_s:
                char_down = False
            if event.key == pygame.K_a:
                char_left = False
            if event.key == pygame.K_d:
                char_right = False

    # rendering map -----------------------------------------------------#

    for y, tile_row in enumerate(map_one_data):
        for x,tile in enumerate(tile_row):
            if tile == "1":
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0], (10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                green_block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0], (10 + x * bv + y * bv) - game_scroll[1],green_block.get_width(),green_block.get_height())
                blocks.append([block_rect,green_block_rect])
                # pygame.draw.rect(screen, (0, 0, 0), block_rect, 1)   # draw each block's hitbox

    for block_info in blocks:
        screen.blit(green_block,block_info[0])

    # character code -----------------------------------------------------#
    character_hitbox = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 10,55,90)
    character_feet_hitbox = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 80,55,20)

    if not char_jump:
        character_feet_shadow = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 80,55,20)
    else:
        character_feet_shadow = pygame.Rect(char_x - game_scroll[0] + 10,char_prev_ypos - game_scroll[1] + 80,55,20)

    # character movement
    if char_up:
        char_y -= char_speed
        if char_jump:
            char_prev_ypos -= char_speed
    if char_down:
        char_y += char_speed
        if char_jump:
            char_prev_ypos += char_speed
    if char_left:
        char_x -= char_speed
    if char_right:
        char_x += char_speed
    if char_jump:  # handle character jumping
        char_y -= char_acceleration
        char_acceleration -= 1
        if char_y - game_scroll[1] + 90 > character_feet_shadow.y:  # plus 90 to detect bottom edge of character
            char_jump = False

    # check if character fallen
    block_touched = False
    if not char_fall:
        for num, block_hitbox in enumerate(blocks):
            if character_feet_shadow.colliderect(block_hitbox[0]):
                block_touched = True
        else:
            if not block_touched and not char_jump:
                char_fall = True
                char_acceleration = 10

    if not block_touched and not char_jump:
        char_y += char_acceleration
        char_acceleration += 1

    if char_acceleration >= 100:  # if player falls off the map, quit program (later implement life system)
        pygame.quit()
        sys.exit()

    # drawing the character and its hitboxes
    pygame.draw.rect(screen,(255,0,0),character_hitbox,1)
    pygame.draw.rect(screen,(0,255,0),character_feet_hitbox,1)
    pygame.draw.rect(screen, shadow_col, character_feet_shadow, 0)
    screen.blit(character,(char_x - game_scroll[0],char_y - game_scroll[1]))

    screen.blit(text,text_rect)
    pygame.display.flip()
    clock.tick(FPS)

