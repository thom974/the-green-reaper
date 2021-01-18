# importing modules ---------------------------------------------#

import pygame
import math
import random
import sys

import data.scripts.math_functions as m
import data.scripts.effects as e

# setting up pygame ---------------------------------------------#

pygame.init()
pygame.display.set_caption('insert game title here')
size = (screen_width, screen_height) = (900,600)
screen = pygame.display.set_mode(size)
temp_display = pygame.Surface((300,300))
clock = pygame.time.Clock()
# pygame.mouse.set_visible(False)
FPS = 60
frame_count = 0
# helpful functions ---------------------------------------------#


def load_image(filename,*args):
    surface = pygame.image.load('data/images/' + filename + '.png')
    if len(args) != 0 and args[0]:
        surface.set_colorkey((255,255,255))
    else:
        surface.set_colorkey((0,0,0))  # remove black background
    return surface


animation_frame_surfaces = {}  # holds all the frames' surfaces
animations_dictionary = {}  # holds a list for every animation type, the keys being the name of each animation


def load_animation(directory,frame_frequency,**kwargs):  # frame_frequency holds a list, ex. [1,1] specifying how many times should appear in an animation
    global animation_frame_surfaces
    animation_name = directory.split('/')[-1]
    animation_frame_names = []

    for num, frame in enumerate(frame_frequency):
        frame_name = animation_name + str(num)  # create the name of the frame
        frame_location = directory + '/' + frame_name + '.png'  # create the location of each frame image
        frame_image = pygame.image.load(frame_location).convert()  # load in each frame image
        frame_image.set_colorkey((255,255,255))  # sets white bg to transparent
        if 'size' not in kwargs:
            frame_image = pygame.transform.scale(frame_image,(100,100))
        else:
            frame_image = pygame.transform.scale(frame_image,kwargs['size'])
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
animations_dictionary['idle'] = load_animation('data/images/animations/idle',[20,20])
animations_dictionary['walk'] = load_animation('data/images/animations/walk',[10,10,10])
animations_dictionary['jump'] = load_animation('data/images/animations/jump',[2,2,4,2,4,1])
animations_dictionary['slash'] = load_animation('data/images/animations/slash',[10,8,6,4,3],size=(200,200))
animations_dictionary['thunder'] = load_animation('data/images/animations/thunder',[2,2,2,2,2,2,2,2,2,2,5,2,2,2],size=(105,355))
animations_dictionary['slime'] = load_animation('data/enemies/slime',[15,15,15],size=(85,55))
animations_dictionary['slime_dmg'] = load_animation('data/enemies/damage/slime_dmg',[10],size=(85,55))

# game HUD
mana_bar = load_image('mana_bar',True).convert()
mana_bar = pygame.transform.scale(mana_bar,(300,60))

# enemies
slime1,slime2,slime3 = ['slime',[0,0],0,[],'right',None,'move',False,2,255],['slime',[0,0],0,[],'right',None,'move',False,2,255],['slime',[0,0],0,[],'right',None,'move',False,2,255]
active_enemies = [slime1,slime2,slime3]
hp_bar = load_image('health_bar',True).convert()
hp_bar = pygame.transform.scale(hp_bar,(55,15))

# char animation variables
char_current_animation = 'idle'  # create variable to hold character's current animation
char_current_frame = 0
char_animation_flip = False  # flip the frame depending on direction moving
char_animation_lock = False

# level variables
game_scroll = [0,0]
number_of_enemies = 0
found_enemies = False

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
bv = 50

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
char_mana = 255
char_alive = True

# char_scythe = pygame.image.load('data/images/scythe.png').convert()
char_scythe = load_image('scythe',True).convert()
char_scythe = pygame.transform.scale(char_scythe,(135,135))
char_shadow = load_image('char_shadow',True).convert()
display_shadow = True

# char spell casting variables
# grid_point = pygame.image.load('data/images/grid_point.png').convert()
grid_point = load_image('grid_point',True).convert()
grid_point = pygame.transform.scale(grid_point,(30,30))
# spell_bg = pygame.image.load('data/images/spell_bg.png').convert()
spell_bg = load_image('spell_bg',True).convert()
grid_scale = 1  # adjust the gap between grid points
grid_point_diff = 1
grid_points = []
grid_max = False
active_point = 4

spells_dictionary = {
    'fireball': [[3, 0, 1, 2, 5, 8, 7, 6],200],  # spell pattern, cost
    'slash': [[2, 1, 0, 3, 6],50],
    'thunder': [[1, 3, 4, 5, 7],100]
}

spell_cast = [False,[0,0],[],[],['',0,[0,0]]]  # spell active, grid location, line points, points touched, [current spell active, its frame,[location]]

# glitch colours
glitch_colours = [(16, 26, 86),(22, 45, 118),(36, 86, 196),(195, 20, 118),(51, 7, 57),(28, 93, 129),(163, 127, 241),(99, 24, 79),(69, 173, 204)]
bn = 30
sn = 100
gsl = 0

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
    game_scroll[0] += (char_x - game_scroll[0] - 450 + 37) / 40
    game_scroll[1] += (char_y - game_scroll[1] - 300 + 50) / 40

    # to display mouse coordinates
    mx, my = pygame.mouse.get_pos()
    text = osu_font.render(str(mx) + ", " + str(my), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (800, 40)

    # # test spell casting
    # current_spell_frame = animations_dictionary['slime'][spell_cast[4][1]]
    # csf_surf = animation_frame_surfaces[current_spell_frame]
    # screen.blit(csf_surf, (0, 100))
    # pygame.draw.rect(screen,(255,0,0),(0,100,csf_surf.get_width(),csf_surf.get_height()),1)
    # spell_cast[4][1] += 1
    # if spell_cast[4][1] >= len(animations_dictionary['slime']):
    #     spell_cast[4][1] = 0

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

    enemy_tiles = [[]]
    first_etf = False
    pfet = 0
    for y, tile_row in enumerate(map_one_data):
        found_e_tile = False
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
                if tile == "e":  # check for enemy tile
                    if not first_etf:  # only execute once
                        pfet = y
                        first_etf = True
                        found_e_tile = True
                    if not found_e_tile:
                        if y - 1 == pfet:
                            enemy_tiles[-1].append(block_rect)
                            pfet = y
                            found_e_tile = True
                        else:
                            enemy_tiles.append([])
                            enemy_tiles[-1].append(block_rect)
                            pfet = y
                            found_e_tile = True
                    else:
                        enemy_tiles[-1].append(block_rect)
            elif tile == "4":
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                bridge_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], bridge.get_width(),bridge.get_height())
                blocks.append([block_rect, bridge_rect])
                trees.append(None)
                rocks.append(None)

    # save original number of enemies
    if not found_enemies:
        number_of_enemies = len(active_enemies)

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

    for j, area in enumerate(enemy_tiles):
        for i, e_tile in enumerate(area):
            if i == 0 and active_enemies[j][1][0] == 0 and active_enemies[j][1][1] == 0:
                active_enemies[j][1] = [e_tile.x, e_tile.y]
            # pygame.draw.rect(screen, (255, 0, 0), e_tile, 1)
            active_enemies[j][3].append(e_tile)  # append each 'territory tile' to slime

    # drawing the enemies-------------------------------------------------------------------#
    for e_num, enemy in enumerate(active_enemies):
        enemy_loc = enemy[1]
        enemy_left = False
        if enemy[6] == 'move':
            enemy_cf = animations_dictionary[enemy[0]][enemy[2]]
        else:
            enemy_cf = animations_dictionary['slime_dmg'][enemy[2]]
        enemy_surf = animation_frame_surfaces[enemy_cf]
        enemy_surf.set_alpha(enemy[9])
        enemy_hitbox = pygame.Rect(enemy_loc[0] - game_scroll[0],enemy_loc[1] - game_scroll[1],animation_frame_surfaces[enemy_cf].get_width(),animation_frame_surfaces[enemy_cf].get_height())
        enemy[5] = enemy_hitbox
        if enemy[7]:
            screen.blit(hp_bar,[enemy_loc[0] - game_scroll[0] + 15, enemy_loc[1] - game_scroll[1] - 20])
            health_val = pygame.Rect(enemy_loc[0] - game_scroll[0] + 20, enemy_loc[1] - game_scroll[1] - 16, enemy[8] * 25, 8)
            pygame.draw.rect(screen,(255,0,0),health_val,0)
        if enemy[8] <= 0:
            enemy[9] -= 40
        screen.blit(enemy_surf,[enemy_loc[0] - game_scroll[0], enemy_loc[1] - game_scroll[1]])
        # pygame.draw.rect(screen,(0,255,0),enemy_hitbox,1)
        enemy[2] += 1

        # handle enemy movement ----------------------------------------#
        # moving enemy on screen
        if enemy[4] == 'right':
            enemy[1][0] += 0.5
            enemy[1][1] += 0.5
        elif enemy[4] == 'left':
            enemy[1][0] -= 0.5
            enemy[1][1] -= 0.5
        elif enemy[4] == 'up':
            enemy[1][0] += 0.5
            enemy[1][1] -= 0.5
        elif enemy[4] == 'down':
            enemy[1][0] -= 0.5
            enemy[1][1] += 0.5

        # check if enemy left territory
        for territory_tile in enemy[3]:
            # pygame.draw.rect(screen,(0,0,255),territory_tile,2)
            if territory_tile.colliderect(enemy_hitbox):
                break
        else:
            enemy_left = True

        # handle direction changing
        if enemy_left:
            direc = enemy[4]
            if direc == 'right':
                enemy[4] = 'down'
                enemy[1][0] -= 25
                enemy[1][1] -= 25
            elif direc == 'left':
                enemy[1][0] += 25
                enemy[1][1] += 25
                enemy[4] = 'up'
            elif direc == 'up':
                enemy[1][0] -= 10
                enemy[1][1] += 10
                enemy[4] = 'right'
            elif direc == 'down':
                enemy[1][0] += 10
                enemy[1][1] -= 10
                enemy[4] = 'left'
            enemy_left = False

        if enemy[2] >= len(animations_dictionary[enemy[0]]) and enemy[6] == 'move':  # if the current frame is equal to the enemy's max frame
            enemy[2] = 0
        elif enemy[2] >= len(animations_dictionary['slime_dmg']) and enemy[6] == 'hurt':
            enemy[2] = 0
            enemy[6] = 'move'

        enemy[3] = []  # clear the enemy's territory tiles

        if enemy[9] <= 0:
            number_of_enemies -= 1  # subtract one from enemy counter
            enemy[7] = False  # don't show hp bar

    print(number_of_enemies)

    # making glitch effect for spell casting ----------------------------------------------#
    if spell_cast[0]:
        # glitch_bg_sl = pygame.Surface((600, 600))
        # glitch_bg_fl = pygame.Surface((600, 600))
        # glitch_bg = pygame.Surface((600, 600))
        # glitch_bg.fill((10, 7, 44))
        # glitch_bg.set_alpha(50)
        # glitch_bg_fl.set_colorkey((0, 0, 0))
        # frame_bg = spell_bg.copy()
        #
        # for _ in range(bn):
        #     colour = random.choice(glitch_colours)
        #     w, h = random.randint(300, 400), random.randint(75, 100)
        #     x, y = random.randint(-50, 550), random.randint(0, 550)
        #     pygame.draw.rect(glitch_bg_sl, colour, (x, y, w, h), 0)
        #
        # glitch_bg_sl.set_alpha(100)
        #
        # for _ in range(sn):
        #     colour = random.choice(glitch_colours)
        #     w, h = random.randint(100, 220), random.randint(4, 7)
        #     x, y = random.randint(-50, 550), random.randint(0, 550)
        #     pygame.draw.rect(glitch_bg_fl, colour, (x, y, w, h), 0)
        #
        # glitch_bg = pygame.transform.scale(glitch_bg, (gsl, gsl))
        # glitch_bg_sl = pygame.transform.scale(glitch_bg_sl, (gsl, gsl))
        # glitch_bg_fl = pygame.transform.scale(glitch_bg_fl, (gsl, gsl))
        # frame_bg = pygame.transform.scale(frame_bg, (int(gsl * 1.5), int(gsl * 1.5)))

        glitch_bg, glitch_bg_sl, glitch_bg_fl, frame_bg = e.create_glitch_effect(gsl,frame=spell_bg.copy())

        screen.blit(glitch_bg,(spell_cast[1][0] - glitch_bg.get_width() // 2, spell_cast[1][1] - glitch_bg.get_height() // 2))
        screen.blit(glitch_bg_sl, (spell_cast[1][0] - glitch_bg_sl.get_width() // 2, spell_cast[1][1] - glitch_bg_sl.get_height() // 2))
        screen.blit(glitch_bg_fl, (spell_cast[1][0] - glitch_bg_fl.get_width() // 2, spell_cast[1][1] - glitch_bg_fl.get_height() // 2))
        screen.blit(frame_bg,(spell_cast[1][0] - frame_bg.get_width() // 2, spell_cast[1][1] - frame_bg.get_height() // 2))

        # screen.blit(glitch_bg,(spell_cast[1][0] - glitch_bg.get_width() // 2, spell_cast[1][1] - glitch_bg.get_height() // 2))
        # screen.blit(glitch_bg_sl, (spell_cast[1][0] - glitch_bg_sl.get_width() // 2, spell_cast[1][1] - glitch_bg_sl.get_height() // 2))
        # screen.blit(glitch_bg_fl, (spell_cast[1][0] - glitch_bg_fl.get_width() // 2, spell_cast[1][1] - glitch_bg_fl.get_height() // 2))
        # screen.blit(frame_bg,(spell_cast[1][0] - frame_bg.get_width() // 2, spell_cast[1][1] - frame_bg.get_height() // 2))

    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed(3)

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
                display_shadow = True
                block_touched = True
        else:
            if not block_touched:
                display_shadow = False
            if not block_touched and not char_jump:
                char_fall = True
                char_acceleration = 10

    if not block_touched and not char_jump:
        char_y += char_acceleration
        char_acceleration += 1

    if char_acceleration >= 100:  # if player falls off the map, quit program (later implement life system)
        pygame.quit()
        sys.exit()

    # spell casting code ------------------------------------------------------------------------#
    if mb[0]:
        spell_cast[0] = True
        if spell_cast[1][0] == 0 and spell_cast[1][1] == 0:
            spell_cast[1] = [mx, my]
    else:
        if len(spell_cast[3]) != 0:  # check if the user connected any grid points
            for spell_name, spell_info in spells_dictionary.items():
                spell_points, spell_cost = spell_info
                if char_mana - spell_cost > 0:
                    if spell_points == spell_cast[3]:
                        spell_cast[4][0] = spell_name
                        char_mana -= spell_cost
            spell_cast[4][2] = spell_cast[1].copy()

        spell_cast[0] = False
        spell_cast[1][0], spell_cast[1][1] = (0, 0)
        spell_cast[2] = []
        spell_cast[3] = []
        grid_point_diff = 1
        grid_points = []
        active_point = 4
        grid_max = False
        gsl = 0

    if spell_cast[0]:
        for y in range(3):
            for x in range(3):
                grid_point_loc = [(spell_cast[1][0] - grid_point.get_width() // 2 - grid_point_diff * grid_scale) + x * grid_point_diff * grid_scale,(spell_cast[1][1] - grid_point.get_width() // 2 - grid_point_diff * grid_scale) + y * grid_point_diff * grid_scale]
                if grid_max and len(grid_points) < 9:
                    grid_points.append(pygame.Rect(grid_point_loc[0], grid_point_loc[1], grid_point.get_width(),grid_point.get_height()))
                screen.blit(grid_point, grid_point_loc)

        if len(grid_points) != 0:
            pygame.draw.line(screen, (0, 0, 0), (grid_points[active_point][0] + grid_point.get_width() // 2,grid_points[active_point][1] + grid_point.get_height() // 2),(mx, my), 10)
            for num, rect in enumerate(grid_points):
                if rect.collidepoint(mx, my) and num != active_point:
                    spell_cast[2].append([(grid_points[active_point][0] + grid_point.get_width() // 2,grid_points[active_point][1] + grid_point.get_height() // 2),(rect.x + rect.w // 2, rect.y + rect.h // 2)])
                    spell_cast[3].append(num)
                    active_point = num

        if len(spell_cast[2]) != 0:  # drawing the existing line connections
            for points in spell_cast[2]:
                x1, y1 = points[0]
                x2, y2 = points[1]
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 10)

        if grid_point_diff < 50:
            grid_point_diff += 5
        else:
            grid_max = True

        if gsl < 170:
            gsl += 15

    # spell animation handling
    if spell_cast[4][0] != '':  # check if spell was cast
        current_spell_frame = animations_dictionary[spell_cast[4][0]][spell_cast[4][1]]
        csf_surf = animation_frame_surfaces[current_spell_frame]
        if spell_cast[4][0] == 'slash':
            csf_center = (spell_cast[4][2][0] - csf_surf.get_width()//2, spell_cast[4][2][1] - csf_surf.get_height()//2)
            csf_hitbox = pygame.Rect(csf_center[0], csf_center[1], csf_surf.get_width(), csf_surf.get_height())
        elif spell_cast[4][0] == 'thunder':
            csf_center = (spell_cast[4][2][0] - csf_surf.get_width()//2, spell_cast[4][2][1] - csf_surf.get_height() + 50)
            csf_hitbox = pygame.Rect(csf_center[0], csf_center[1] + 350, csf_surf.get_width(), csf_surf.get_height()-400)
        screen.blit(csf_surf, csf_center)
        pygame.draw.rect(screen,(0,255,0),csf_hitbox,1)
        spell_cast[4][1] += 1
        if spell_cast[4][1] >= len(animations_dictionary[spell_cast[4][0]]):
            spell_cast[4] = ['', 0, [0, 0]]

    # code for combat detection-----------------------------------------------------------------------#
        for enemy in active_enemies:
            if enemy[5].colliderect(csf_hitbox) and spell_cast[4][1] == 1:  # makes sure detection occurs once per spell cast
                enemy[2] = 0
                enemy[6] = 'hurt'
                enemy[7] = True
                if spell_cast[4][0] == 'slash':
                    enemy[8] -= 1
                elif spell_cast[4][0] == 'thunder':
                    enemy[8] -= 2

    # character graphics code ------------------------------------------------------------------------#
    # pygame.draw.rect(screen,(255,0,0),character_hitbox,1)
    # pygame.draw.rect(screen,(0,255,0),character_feet_hitbox,1)
    # pygame.draw.rect(screen, shadow_col, character_feet_shadow, 0)
    char_shadow = pygame.transform.scale(char_shadow,(character_feet_shadow.w,character_feet_shadow.h))
    if display_shadow:
        screen.blit(char_shadow,character_feet_shadow)
    char_current_frame += 1
    if char_current_frame >= len(animations_dictionary[char_current_animation]) and char_current_animation != 'jump':  # if the current frame is equal to the list length, reset it to 0
        char_current_frame = 0
    if char_current_animation == 'jump' and char_current_frame >= len(animations_dictionary['jump']):
        char_current_frame = len(animations_dictionary['jump']) - 1

    char_frame_name = animations_dictionary[char_current_animation][char_current_frame]  # find frame name depending on char current frame
    char_frame_to_display = animation_frame_surfaces[char_frame_name]
    screen.blit(pygame.transform.flip(char_scythe,char_animation_flip, False), (char_x - game_scroll[0] - 15,char_y - game_scroll[1] - 50))
    screen.blit(pygame.transform.flip(char_frame_to_display,char_animation_flip,False),(char_x - game_scroll[0],char_y - game_scroll[1]))  # flip to make the character face the right way

    # HUD ----------------------------------------------------------------------------#

    screen.blit(mana_bar, (0, 20))
    mana_bar_fill_bg, mana_bar_fill_sl, mana_bar_fill_fl = e.create_glitch_effect(char_mana, height=10)
    screen.blit(mana_bar_fill_bg, (6, 45))
    screen.blit(mana_bar_fill_sl, (6, 45))
    screen.blit(mana_bar_fill_fl, (6, 45))

    if char_mana <= 255 and frame_count % 5 == 0:
        char_mana += 1

    frame_count += 1
    if frame_count > 60:
        frame_count = 0

    pygame.display.flip()
    clock.tick(FPS)

