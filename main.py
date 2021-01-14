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


animation_frame_surfaces = {}  # holds all the frames' surfaces
animations_dictionary = {}  # holds a list for every animation type, the keys being the name of each animation


def load_animation(directory,frame_frequency):  # frame_frequency holds a list, ex. [1,1] specifying how many times should appear in an animation
    global animation_frame_surfaces
    animation_name = directory.split('/')[-1]
    animation_frame_names = []

    for num, frame in enumerate(frame_frequency):
        frame_name = animation_name + str(num)  # create the name of the frame
        frame_location = directory + '/' + frame_name + '.png'  # create the location of each frame image
        frame_image = pygame.image.load(frame_location).convert()  # load in each frame image
        frame_image.set_colorkey((255,255,255))  # sets white bg to transparent
        frame_image = pygame.transform.scale(frame_image,(100,100))
        animation_frame_surfaces[frame_name] = frame_image.copy()  # load into dictionary the frame name + its actual surface

        for _ in range(frame):
            animation_frame_names.append(frame_name)

    return animation_frame_names  # return all the frame names for an animation


def change_animation(animation_name,frame,new_animation,lock):
    if animation_name != new_animation and not lock:
        char_animation = new_animation
        char_frame = 0
        return char_animation, char_frame
    return animation_name,frame

# loading in game variables -------------------------------------#


# animations
animations_dictionary['idle'] = load_animation('data/images/animations/idle',[15,15])
animations_dictionary['walk'] = load_animation('data/images/animations/walk',[10,10,10])
animations_dictionary['jump'] = load_animation('data/images/animations/jump',[2,2,10,2,5,1])

# char animation variables
char_current_animation = 'idle'  # create variable to hold character's current animation
char_current_frame = 0
char_animation_flip = False  # flip the frame depending on direction moving
char_animation_lock = False

game_scroll = [0,0]

bridge = load_image('bridge').convert()
bridge = pygame.transform.scale(bridge,(101,169))
green_block = load_image('ground_green').convert()
green_block = pygame.transform.scale(green_block,(101,170))
green_tree = load_image('green_tree').convert()
green_tree = pygame.transform.scale(green_tree,(120,189))
green_rock = load_image('green_rock').convert()
green_rock = pygame.transform.scale(green_rock,(80,80))
found_tiles = False
found_tiles_ypos = False
bv = 51

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
    trees = []
    rocks = []
    char_center = (char_x - game_scroll[0] + 40,char_y - game_scroll[1] + 45)

    # background
    screen.fill((82, 96, 110))

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
                char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'jump',char_animation_lock)
                char_animation_lock = True
                char_prev_ypos = char_y
                char_jump = True
                char_acceleration = 20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                char_up = False
                if not char_jump:
                    char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)
            if event.key == pygame.K_s:
                char_down = False
                if not char_jump:
                    char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)
            if event.key == pygame.K_a:
                char_left = False
                if not char_jump:
                    char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)
            if event.key == pygame.K_d:
                char_right = False
                if not char_jump:
                    char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)

    # rendering map -----------------------------------------------------#

    for y, tile_row in enumerate(map_one_data):
        for x,tile in enumerate(tile_row):
            if tile != "0" and tile != "4":  # append the ground tile
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0], (10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                green_block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0], (10 + x * bv + y * bv) - game_scroll[1],green_block.get_width(),green_block.get_height())
                blocks.append([block_rect,green_block_rect])
                if tile == "2":
                    tree_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] - 10, (10 + x * bv + y * bv) - game_scroll[1] - green_tree.get_height() + 80, green_tree.get_width(),green_tree.get_height())
                    tree_hitbox = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] - green_tree.get_height() + 80, green_tree.get_width()-20,green_tree.get_height()-20)
                    trees.append([tree_rect,tree_hitbox])
                else:
                    trees.append(None)
                if tile == "3":
                    rock_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] + 5, green_rock.get_width(),green_rock.get_height())
                    rock_hitbox = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] + 25, green_rock.get_width(),green_rock.get_height() // 2)
                    rocks.append([rock_rect,rock_hitbox])
                else:
                    rocks.append(None)
            elif tile == "4":
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                bridge_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], bridge.get_width(),bridge.get_height())
                blocks.append([block_rect, bridge_rect])
                trees.append(None)
                rocks.append(None)

    # create a list ONCE containing boolean values for each tile
    if not found_tiles:
        tile_render_states = [False for block in blocks]
        found_tiles = True

    for num, block_info in enumerate(blocks):
        block_center = (block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2)
        if m.check_rect_distance(char_center,block_center,400):
            # pygame.draw.line(screen, (0, 255, 0), char_center,(block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2))
            tile_render_states[num] = True
        else:
            pass
            # pygame.draw.line(screen, (255, 0, 0), char_center,(block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2))

        if tile_render_states[num]:
            if block_info[1].h == 170:
                screen.blit(green_block, block_info[0])
            elif block_info[1].h == 169:
                screen.blit(bridge, block_info[0])
            if trees[num] is not None:
                screen.blit(green_tree,trees[num][0])
                # pygame.draw.rect(screen,(0,0,255),trees[num][1],5)
            if rocks[num] is not None:
                screen.blit(green_rock,rocks[num][0])
                # pygame.draw.rect(screen,(0,0,255),rocks[num][1],5)

    # character code -----------------------------------------------------#
    character_hitbox = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 10,70,90)
    character_feet_hitbox = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 80,70,20)

    # detect collision
    for rock in rocks:
        if rock is not None:
            rock_hb = rock[1]
            collisions = m.check_collision(character_feet_hitbox,rock_hb)
            if collisions[0]:
                char_y -= 5
            elif collisions[1]:
                char_y += 5
            elif collisions[2]:
                char_x -= 5
            elif collisions[3]:
                char_x += 5

    for tree in trees:
        if tree is not None:
            tree_hb = tree[1]
            collisions = m.check_collision(character_feet_hitbox, tree_hb)
            if collisions[0]:
                char_y -= 5
            elif collisions[1]:
                char_y += 5
            elif collisions[2]:
                char_x -= 5
            elif collisions[3]:
                char_x += 5

    if not char_jump:
        character_feet_shadow = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 80,70,20)
    else:
        character_feet_shadow = pygame.Rect(char_x - game_scroll[0] + 10,char_prev_ypos - game_scroll[1] + 80,70,20)

    # character movement
    if char_up:
        char_y -= char_speed
        char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)
        if char_jump:
            char_prev_ypos -= char_speed
    if char_down:
        char_y += char_speed
        char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)
        if char_jump:
            char_prev_ypos += char_speed
    if char_left:
        char_x -= char_speed
        # for character sprite
        char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)
        char_animation_flip = False
    if char_right:
        char_x += char_speed
        # for character sprite
        char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)
        char_animation_flip = True
    if char_jump:  # handle character jumping
        char_y -= char_acceleration
        char_acceleration -= 1
        if char_y - game_scroll[1] + 90 > character_feet_shadow.y:  # plus 90 to detect bottom edge of character
            char_jump = False
            char_animation_lock = False
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)

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

    char_current_frame += 1
    if char_current_frame >= len(animations_dictionary[char_current_animation]) and char_current_animation != 'jump':  # if the current frame is equal to the list length, reset it to 0
        char_current_frame = 0
    if char_current_animation == 'jump' and char_current_frame >= len(animations_dictionary['jump']):
        char_current_frame = len(animations_dictionary['jump']) - 1

    char_frame_name = animations_dictionary[char_current_animation][char_current_frame]  # find frame name depending on char current frame
    char_frame_to_display = animation_frame_surfaces[char_frame_name]
    screen.blit(pygame.transform.flip(char_frame_to_display,char_animation_flip,False),(char_x - game_scroll[0],char_y - game_scroll[1]))  # flip to make the character face the right way

    # screen.blit(text,text_rect)
    print(char_current_animation)
    pygame.display.flip()
    clock.tick(FPS)

