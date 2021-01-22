'''
Name: Thomas Luc
Date: Jan 22, 2021
Class Code: ICS3U
Teacher: Mrs. Bokhari

Description: An (environmentally-friendly) game called 'The Green Reaper', made with the pygame Python module.
The player controls a 'grim reaper' character and casts spells using a 3x3 to kill different enemies. The premise
of the story is that the character is killing off 'mutations' which originated from pollution, and in doing so, cleans
the planet. There are 5 different zones to go through, with increasing difficulty. The game mimics an isometric style rendering,
so each tile appears to look three dimensional.
'''

# importing modules ---------------------------------------------#

import pygame

import data.scripts.math_functions as m
import data.scripts.effects as e

# setting up pygame ---------------------------------------------#

pygame.init()
pygame.display.set_caption('The Green Reaper')
size = (screen_width, screen_height) = (900,600)
screen = pygame.display.set_mode(size)
temp_display = pygame.Surface((300,300))
clock = pygame.time.Clock()
FPS = 60
frame_count = 0
second_frame_count = 0
animation_frame_surfaces = {}  # holds all the frames' surfaces
animations_dictionary = {}  # holds a list for every animation type, the keys being the name of each animation

# helpful functions and code---------------------------------------------#


def load_image(filename,*args):  # used to load in each image from the 'images' directory. optional arguments to specify colorkey.
    surface = pygame.image.load('data/images/' + filename + '.png')
    if len(args) != 0 and args[0]:  # if an optional argument was specified and it is 'True'
        surface.set_colorkey((255,255,255))  # make white bg transparent
    else:
        surface.set_colorkey((0,0,0))  # make black bg transparent
    return surface


def load_animation(directory,frame_frequency,**kwargs):  # used to load in each animation in the game
    global animation_frame_surfaces  # each actual frame contained in the specified animation will be added to this dictionary
    animation_name = directory.split('/')[-1]
    animation_frame_names = []  # this list will hold just the names (string) of each frame_name for the ENTIRE animation

    for num, frame in enumerate(frame_frequency):  # frame_frequency holds a list, ex. [1,1] specifying how many times each frame should appear in an animation
        frame_name = animation_name + str(num)  # create the name of the frame
        frame_location = directory + '/' + frame_name + '.png'  # create the location of the frame image, using the frame_name var
        frame_image = pygame.image.load(frame_location).convert()  # load in each frame image
        frame_image.set_colorkey((255,255,255))  # sets white bg to transparent

        if 'size' not in kwargs:  # if the keyworded argument 'size' was not given, this executes
            frame_image = pygame.transform.scale(frame_image,(100,100))  # by default, each frame will be 100x100 px
        else:
            frame_image = pygame.transform.scale(frame_image,kwargs['size'])  # if a size was specified, each frame image will become that size

        animation_frame_surfaces[frame_name] = frame_image.copy()  # load into dictionary the frame name + its actual surface

        for _ in range(frame):  # frame is equal to the number in each index of frame_frequency. e.g [1,1] --> frame = 1 when this loop first iterates
            animation_frame_names.append(frame_name)  # frame_name will be appended 'frame' (frame is a num) times.

    return animation_frame_names  # return all the frame names for the animation.


def change_animation(animation_name,frame,new_animation,lock):  # used to change the player's animation during the game
    if animation_name != new_animation and not lock:  # animation_name represents the char's current animation. if it is the same as the proposed new animation, don't change it
        char_animation = new_animation  # otherwise, we save the new animation in a var
        char_frame = 0  # reset the char's current frame to 0 so we start at the first frame of the new animation
        return char_animation, char_frame  # return the name of the new animation to change to + the char's frame (0)
    return animation_name,frame  # this will just return the same values found in the parameters


def create_font(font_size):  # this returns the 'Silver' font with the specified size
    return pygame.font.Font('data/Silver.ttf', font_size)


def create_bg(col):  # this is used to create the diagonal stripes seen in the background
    y = -150  # the polygon y-offset
    poly_points1 = [(0,150+y),(900,0+y),(900,100+y),(0,250+y)]  # each set of poly points have increasing y values
    poly_points2 = [(0,350+y),(900,200+y),(900,300+y),(0,450+y)]
    poly_points3 = [(0,550+y),(900,400+y),(900,500+y),(0,650+y)]
    poly_points4 = [(0,750+y),(900,600+y),(900,700+y),(0,850+y)]

    pygame.draw.polygon(screen,col,poly_points1,0)
    pygame.draw.polygon(screen,col,poly_points2,0)
    pygame.draw.polygon(screen,col,poly_points3,0)
    pygame.draw.polygon(screen,col,poly_points4,0)


def load_map(map_num):  # used for returning the map information of the map_num passed
    map_name = 'map' + str(map_num)  # create the name of the map that we're opening
    f = open('data/maps/' + map_name + '.txt', 'r')
    map_data = [[tile for tile in tile_row.rstrip("\n")] for tile_row in f]  # returns a nested list. each list holds the individual characters of one row
    f.close()
    return map_data


# creating game over screen
backdrop = pygame.Surface((900,600))  # backdrop used to place on top of glitchy screen
backdrop.set_alpha(150)  # make it semi-transparent so the user can still see the glitchy screen
game_over_font, game_over_font_2 = create_font(70), create_font(40)
game_over_txt = game_over_font.render('game over.', True,(194, 194, 194))
game_over_rect = game_over_txt.get_rect()  # create a rectangle from the given text
game_over_rect.center = (450,300)  # set its center so that I can easily display an element where I want it
game_over_txt_2 = game_over_font_2.render('press \'r\' to retry the level.', True, (204, 20, 20))
game_over_rect_2 = game_over_txt_2.get_rect()
game_over_rect_2.center = (450,350)
ending_txt_font, ending_txt_font2 = create_font(100), create_font(70)
ending_txt = ending_txt_font.render('thanks for playing!',True,(255,255,255))
ending_txt2 = ending_txt_font2.render('(and more importantly, saving the earth.)',True,(143, 146, 150))
ending_txt_rect, ending_txt_rect2 = ending_txt.get_rect(), ending_txt2.get_rect()
ending_txt_rect.center, ending_txt_rect2.center = (450,270), (450,375)

level_transition = pygame.Surface((900,600))  # screen used as transition
level_transition.fill((255,255,255))  # fill bg with white
level_transition_alpha = 0  # var to hold the Surface's alpha val
level_fade = False
level_timer = 0

game_border = load_image('border',True).convert()
game_border = pygame.transform.scale(game_border,(900,600))

# loading in game variables ----------------------------------------------------------------------------#

# loading in intro message
f = open('data/maps/game_intro.txt','r')
intro_text = ''
for line in f:
    line = line.rstrip("\n") + ' '
    intro_text += line 
f.close()

# loading in animations
animations_dictionary['idle'] = load_animation('data/images/animations/idle',[20,20])
animations_dictionary['walk'] = load_animation('data/images/animations/walk',[10,10,10])
animations_dictionary['jump'] = load_animation('data/images/animations/jump',[2,2,4,2,4,1])
animations_dictionary['slash'] = load_animation('data/images/animations/slash',[10,8,6,4,3],size=(200,200))
animations_dictionary['thunder'] = load_animation('data/images/animations/thunder',[2,2,2,2,2,2,2,2,2,2,5,2,2,2],size=(105,355))
animations_dictionary['slime'] = load_animation('data/enemies/slime',[15,15,15],size=(85,55))
animations_dictionary['slime_dmg'] = load_animation('data/enemies/damage/slime_dmg',[10],size=(85,55))
animations_dictionary['death'] = ''  # empty for now as this animations are created depending on the char's current animation
animations_dictionary['screen_glitch'] = ''  # empty for now as this animation requires a copy of the current screen when the char dies

# game HUD (head up display)
mana_bar = load_image('mana_bar',True).convert()
mana_bar = pygame.transform.scale(mana_bar,(240,48))
enemy_counter = load_image('enemy_count').convert()
enemy_counter.set_colorkey((255,0,0))
enemy_counter = pygame.transform.scale(enemy_counter,(234,102))
enemy_counter_bg = pygame.Surface((205,65))
enemy_counter_bg.fill((125, 125, 125))
enemy_counter_bg.set_alpha(100)
enemy_counter_font = create_font(55)
level_header = load_image('level',True).convert()
level_header = pygame.transform.scale(level_header,(288,80))
level_font = create_font(50)
scroll = load_image('scroll',True).convert()
scroll = pygame.transform.scale(scroll,(600,728))
scroll_font = create_font(30)

# char animation variables
char_current_animation = 'idle'  # create variable to hold character's current animation
char_current_frame = 0  # holds the char frame. it is used to draw the appropriate frame in an animation sequence
char_animation_flip = False  # flip the frame depending on direction moving
char_animation_lock = False  # used in change_animation function. if True, the char's animation will not change

# level variables
game_running = True  # bool val which is used by the main game loop
current_level = 1  # hold the current level
current_map = load_map(current_level)  # load in the map one
game_scroll = [0,0]  # allows the game to stay centered on the player as they move. 0th index = x-offset, 1st index = y-offset
number_of_enemies = 0  # hold the original number of enemies on the current level
found_enemies = False
found_tvs = False
save_screen = None
level_retry = False
scroll_obj = [[450 - scroll.get_width()//2,700],True]  # IN ORDER: scroll location (x,y), scroll active

# game assets
bridge = load_image('bridge').convert()
bridge_reverse = pygame.transform.flip(bridge,True,False)
bridge, bridge_reverse = pygame.transform.scale(bridge,(101,169)), pygame.transform.scale(bridge_reverse,(101,169))
green_block, pink_block = load_image('ground_green').convert(), load_image('ground_pink').convert()
green_block, pink_block = pygame.transform.scale(green_block,(101,170)), pygame.transform.scale(pink_block,(101,170))
green_tree, pink_tree = load_image('green_tree').convert(), load_image('pink_tree').convert()
green_tree, pink_tree = pygame.transform.scale(green_tree,(120,189)), pygame.transform.scale(pink_tree,(120,189))
green_rock, pink_rock = load_image('green_rock').convert(), load_image('pink_rock').convert()
green_rock, pink_rock  = pygame.transform.scale(green_rock,(80,80)), pygame.transform.scale(pink_rock,(80,80))
broken_tv = load_image('tv',True).convert()
broken_tv = pygame.transform.scale(broken_tv,(80,90))
bullet = load_image('bullet',True).convert()
bullet = pygame.transform.scale(bullet,(30,30))

# map tile variables
found_tiles = False
found_tiles_ypos = False
bv = 50  # number which scales the x and y distance between each rendered tile
active_block, active_tree, active_rock = green_block, green_tree, green_rock  # these three variables hold the current asset to be displayed, as blocks/trees/rocks have two potential colours
active_bg_col, active_bg_col2 = (45, 53, 61), (82, 96, 110)  # variables to hold the current background colours

clean_block = load_image('ground_clean').convert()  # load in clean assets (blocks/trees/rocks) for when the player clears the level
clean_block = pygame.transform.scale(clean_block,(101,170))
clean_tree = load_image('clean_tree').convert()
clean_tree = pygame.transform.scale(clean_tree,(120,189))
clean_rock = load_image('clean_rock').convert()
clean_rock = pygame.transform.scale(clean_rock,(80,80))

# enemies
slime_obj = ['slime',[0,0],0,[],'right',None,'move',False,2,255]  # IN ORDER: name, location, current frame, enemy tiles, direction, hp_bar, animation, display hp_bar, hp, alpha
tv_obj = [broken_tv,[],None,[],0,True, 255, 0]  # IN ORDER: frame, location, hitbox, bullet list, bullet angle, show on screen bool, alpha, angle
active_enemies = []  # variable to hold all active slimes
active_tvs = []  # variable to hold all active TVs
hp_bar = load_image('health_bar',True).convert()
hp_bar = pygame.transform.scale(hp_bar,(55,15))

# character variables
char_spawn = [100,0]  # character initial spawn location on map
char_x, char_y = (100,100)  # character x/y values
char_speed = 3
char_up = False  # up/down/left/right bool vals will turn True if their respective directional keys are held down. upon release, they become False
char_down = False
char_left = False
char_right = False
char_jump = False  # becomes True if the character is jumping (spacebar is pressed)
char_fall = False  # becomes True if the character is falling down from jump
char_acceleration = 0  # for changing character's vertical acceleration
char_prev_pos = 0  # used to store character's previous y position after a jump, for when they land
char_mana = 255  # character's mana
char_alive = True
char_loaded = False

char_scythe = load_image('scythe',True).convert()  # scythe which appears to be on the back of the character
char_scythe = pygame.transform.scale(char_scythe,(135,135))
char_shadow = load_image('char_shadow',True).convert()
char_shadow.set_alpha(200)
display_shadow = True  # character's shadow will show below their feet if this bool is True

# char spell casting variables
grid_point = load_image('grid_point',True).convert()  # each 'grid point' or 'dot' on the 3x3 grid
grid_point = pygame.transform.scale(grid_point,(30,30))
spell_bg = load_image('spell_bg',True).convert()  # the frame seen around the 3x3 grid
grid_scale = 1  # adjust the gap between grid points
grid_point_diff = 1  # used to increase the difference in distance between each point, to make the grid expand
grid_points = []  # holds the locations of all 3x3 grid points
grid_max = False  # turns True once the grid becomes a certain size
active_point = 4  # holds a num which corresponds to a certain grid point. the line being drawn will always start at this grid point
slash_pic = load_image('slash',True).convert()  # picture of the 'slash' attack pattern for scroll tutorial
slash_pic = pygame.transform.scale(slash_pic,(150,150))
thunder_pic = load_image('thunder',True).convert()  # picture of the 'thunder' attack pattern for scroll tutorial
thunder_pic = pygame.transform.scale(thunder_pic,(150,150))

spells_dictionary = {
    'slash': [[2, 1, 0, 3, 6],50],  # 0th index: each number represents a grid point which must've been drawn to. this is the spell pattern. 1st index: spell mana cost
    'thunder': [[1, 3, 4, 5, 7],100]
}

spell_cast = [False,[0,0],[],[],['',0,[0,0]]]  # spell active, grid location, line points, points touched, [current spell active, its frame,[location]]

# glitch colours
glitch_colours = [(16, 26, 86),(22, 45, 118),(36, 86, 196),(195, 20, 118),(51, 7, 57),(28, 93, 129),(163, 127, 241),(99, 24, 79),(69, 173, 204)]
gsl = 0  # grow side length - used to scale up certain glitch effects, such as the one found in the 3x3 grid

# intro variables
running = True
intro_overlay_surf = pygame.Surface((900,600))
intro_overlay_surf.set_alpha(200)
intro_font = create_font(27)
arrow_font = create_font(70)
text_rect = pygame.Rect(50,50,800,500)
intro_framecount = 0

# introductory game loop ---------------------------------------------------------------------------------------------------------------#
while running:
    mx, my = pygame.mouse.get_pos()  # vars for holding mouse position
    glitch_bgs = e.create_glitch_effect(900,height=600)  # returns a list containing each Surface a part of the 'glitch' effect. there are three overall layers
    arrow_str = '>' * (intro_framecount // 20 + 1)  # this will be a str with 1,2 or 3 '>' symbols depending on the frame count
    arrow_text = arrow_font.render(arrow_str,True,(255,255,255))
    arrow_text_rect = arrow_text.get_rect()
    arrow_text_rect.center = (800,550)

    for glitch_bg in glitch_bgs:  # blit each Surface in the glitch_bgs list onto the screen
        screen.blit(glitch_bg,(0,0))

    screen.blit(intro_overlay_surf,(0,0))
    m.drawText(screen,intro_text,(255,255,255),text_rect,intro_font,aa=True,bkg=None)  # use drawText function to draw text, which automatically wraps depending on the rectangle passed as parameter
    screen.blit(arrow_text,arrow_text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and arrow_text_rect.collidepoint(mx,my):  # check for when the user presses the arrow
            running = False  # stop the loop so that the program starts executing the main game loop

    if intro_framecount < 59:
        intro_framecount += 1
    else:
        intro_framecount = 0

    clock.tick(60)
    pygame.display.update()

# main loop ----------------------------------------------------------------------------------------------------------------#
while game_running:
    # important game variables
    blocks = []  # holds the block tiles
    trees = []  # holds the tree tiles
    rocks = []  # holds the rock tiles
    char_center = (char_x - game_scroll[0] + 40,char_y - game_scroll[1] + 45)  # this location represents the center of the character at all times // used for tile rendering
    character_hitbox = pygame.Rect(char_x - game_scroll[0] + 10, char_y - game_scroll[1] + 10, 70, 90)  # Rect object representing the character's overall hitbox
    character_feet_hitbox = pygame.Rect(char_x - game_scroll[0] + 10, char_y - game_scroll[1] + 80, 70, 20)  # Rect object representing the character's smaller feet hitbox

    # background
    screen.fill(active_bg_col)
    create_bg(active_bg_col2)

    # control game scroll
    game_scroll[0] += (char_x - game_scroll[0] - 450 + 37) / 40
    game_scroll[1] += (char_y - game_scroll[1] - 300 + 50) / 40

    # event detection -----------------------------------------------------#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN: # handle all events regarding keys being pressed down
            if event.key == pygame.K_w:  # if 'w' was pressed, char is moving up. set char_up to True
                char_up = True
            if event.key == pygame.K_s:  # same concept as with 'w' key
                char_down = True
            if event.key == pygame.K_a:
                char_left = True
            if event.key == pygame.K_d:
                char_right = True
            if event.key == pygame.K_SPACE and char_jump is False and char_fall is False:  # if space was pressed, the character isn't already jumping, and they are not currently falling
                char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'jump',char_animation_lock)  # changes the current ani. to 'jump' and sets current frame to 0
                char_animation_lock = True  # lock animation so that character's animation will not change to 'walk' if user presses WASD
                char_prev_ypos = char_y  # store char's y pos before they jump
                char_jump = True
                char_acceleration = 20  # set character's acceleration
            if event.key == pygame.K_r and not char_alive:  # handle level retrying: if the character is dead and the user presses 'r', this executes
                level_retry = True
            if event.key == pygame.K_e:  # for opening level scroll, executes if 'e' is pressed
                scroll_obj[1] = not scroll_obj[1]  # changes the scroll's active state to the inverse of what it was before (if on, turns off // if off, turns on)
        if event.type == pygame.KEYUP:  # handle all events regarding keys being lifted up
            if event.key == pygame.K_w:  # if 'w' is lifted up, the char is no longer moving up. set char_up to False
                char_up = False
                if not char_jump:  # if the character is currently not jumping (and also 'w' is lifted up), this will execute
                    char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)  # change animation to 'idle'
            if event.key == pygame.K_s:  # same concept as with 'w'
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

    # rendering map --------------------------------------------------------------------------------------------------#

    enemy_tiles = [[]]  # list of lists: each list inside represents all Rect objects which make up a single enemy territory. there is one slime per territory
    first_etf = False  # bool variable which turns True once the first enemy tile in the map has been found
    pfet = 0  # previous first enemy tile - holds the y-value of the previous row where an enemy tile was found
    for y, tile_row in enumerate(current_map):  # this nested for loop iterates through each 'tile' in current_map, which holds all tiles (represented by characters, check map text files for more info)
        found_e_tile = False  # becomes True once an enemy tile has been found in the current row
        for x,tile in enumerate(tile_row):
            if tile != "0" and tile != "4" and tile != "5":  # every tile that is not '0', '4' or '5' # requires a base/ground tile which the player can walk on
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0], (10 + x * bv + y * bv) - game_scroll[1], 101, 101)  # create a Rect object whose coords depend on the current x/y values of the for loop, and game scroll
                green_block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0], (10 + x * bv + y * bv) - game_scroll[1],green_block.get_width(),green_block.get_height())  # create a Rect whose coords again depend on x/y, where the tile Surface will be displayed
                blocks.append([block_rect,green_block_rect])  # each pair of rectangles is appended as a list to 'blocks', which holds all tiles the game will render later
                if tile == "2":  # tile num. 2 represents a tree
                    tree_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] - 10, (10 + x * bv + y * bv) - game_scroll[1] - green_tree.get_height() + 80, green_tree.get_width(),green_tree.get_height())  # create Rect obj for tree to be blitted, same concept as before
                    tree_hitbox = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] - green_tree.get_height() + 80, green_tree.get_width()-20,green_tree.get_height()-20)  # create Rect obj for the tree's hitbox
                    trees.append([tree_rect,tree_hitbox])  # append as a list both the location Rect and hitbox Rect
                else:  # 'blocks', 'trees' and 'rocks' are all related lists, so we must append None if the tile is not a tree to keep the same order
                    trees.append(None)
                if tile == "3":  # tile num. 3 represents a rock. loaded in the same exact way as trees are
                    rock_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] + 5, green_rock.get_width(),green_rock.get_height())
                    rock_hitbox = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] + 25, green_rock.get_width(),green_rock.get_height() // 2)
                    rocks.append([rock_rect,rock_hitbox])
                else:
                    rocks.append(None)
                if tile == "6" and not found_tvs:  # tile num. 6 represents a TV enemy. found_tvs becomes True after the very first iteration of the game loop, thus this if statement occurs once
                    tv_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] + 5, broken_tv.get_width(),broken_tv.get_height())
                    # tv_hitbox = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0] + 10, (10 + x * bv + y * bv) - game_scroll[1] + 25, broken_tv.get_width(),broken_tv.get_height() // 2)
                    tv_object = tv_obj.copy()  # create a copy of the tv_obj list, which holds all potential attributes of a TV
                    tv_object[1] = tv_rect  # give the object tv_rect, the location where it is to be blitted
                    tv_object[3] = []  # required because of how list pointers work
                    active_tvs.append(tv_object)  # append to list 'active_tvs' the tv object
                if tile == "e":  # checks for enemy tile
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
            elif tile == "5":
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                bridge_rev_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], bridge_reverse.get_width(),bridge_reverse.get_height())
                blocks.append([block_rect, bridge_rev_rect, 'r'])
                trees.append(None)
                rocks.append(None)

    # create the list of enemies
    if len(active_enemies) == 0:
        for _ in enemy_tiles:
            active_enemies.append(slime_obj.copy())

    # save number of tvs
    if not found_tvs:
        number_of_tvs = len(active_tvs)
        found_tvs = True

    # save original number of total enemies
    if not found_enemies:
        number_of_enemies = len(active_enemies) + len(active_tvs)

    # create a list ONCE containing boolean values for each tile
    if not found_tiles:
        tile_render_states = [False for block in blocks]
        found_tiles = True

    for num, block_info in enumerate(blocks):
        block_center = (block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2)
        if m.check_rect_distance(char_center,block_center,500):
            # pygame.draw.line(screen, (0, 255, 0), char_center,(block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2))
            tile_render_states[num] = True
        else:
            pass
            # pygame.draw.line(screen, (255, 0, 0), char_center,(block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2))

        if tile_render_states[num]:
            if block_info[1].h == 170:
                screen.blit(active_block, block_info[0])
            elif block_info[1].h == 169 and 'r' not in block_info:
                screen.blit(bridge, block_info[0])
            else:
                screen.blit(bridge_reverse, block_info[0])
            if trees[num] is not None:
                screen.blit(active_tree,trees[num][0])
                # pygame.draw.rect(screen,(0,0,255),trees[num][1],5)
            if rocks[num] is not None:
                screen.blit(active_rock,rocks[num][0])
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

        if char_loaded:
            if not char_up:
                if enemy_hitbox.colliderect(character_feet_hitbox) and enemy[9] >= 255:
                    char_alive = False
            else:
                if enemy_hitbox.colliderect(character_feet_shadow) and enemy[9] >= 255:
                    char_alive = False

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

    # tv code
    for tv_num,tv in enumerate(active_tvs):
        frame = tv[0].copy()
        frame.set_alpha(tv[6])
        tv[2] = pygame.Rect(tv[1][0] - game_scroll[0], tv[1][1] - game_scroll[1], broken_tv.get_width(), broken_tv.get_height())
        screen.blit(frame,(tv[1][0] - game_scroll[0], tv[1][1] - game_scroll[1]))
        # pygame.draw.rect(screen,(255,0,0),tv[2],1)

        if tv[2].colliderect(character_feet_hitbox) and tv[5]:
            char_alive = False

        if frame_count == 59 and tv[5]:  # will execute every 1 second
            tv[4] += tv[6]
            tv[6] += 45
            b_loc = [tv[2].x + tv[2].w//2 + game_scroll[0], tv[2].y + tv[2].h//2 + game_scroll[1]]
            tv[3].extend(m.create_bullet(b_loc,tv[4]))
            if len(tv[3]) >= 20:
                del tv[3][:5]

        if len(tv[3]) != 0:
            for b in tv[3]:
                b[0][0] += b[1][0]
                b[0][1] -= b[1][1]
                b_hitbox = pygame.Rect(b[0][0] - bullet.get_width()//2 - game_scroll[0], b[0][1] - bullet.get_height()//2 - game_scroll[1], bullet.get_width(), bullet.get_height())
                screen.blit(bullet,(b[0][0] - bullet.get_width()//2 - game_scroll[0], b[0][1] - bullet.get_height()//2 - game_scroll[1]))

                if b_hitbox.colliderect(character_hitbox):
                    char_alive = False

        if not tv[5]:  # start decreasing its alpha if hit by spell
            tv[6] -= 40

        if tv[6] <= 0:
            tv[6] = 0
            number_of_enemies -= 1

    # making glitch effect for spell casting ----------------------------------------------#
    if spell_cast[0]:
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
    # detect collision
    for rock in rocks:
        if rock is not None:
            rock_hb = rock[1]
            if not char_jump:
                collisions = m.check_collision(character_feet_hitbox,rock_hb)
            else:
                collisions = m.check_collision(character_feet_shadow,rock_hb)
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
            if not char_jump:
                collisions = m.check_collision(character_feet_hitbox, tree_hb)
            else:
                collisions = m.check_collision(character_feet_shadow, tree_hb)
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
    if char_alive:
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

    if char_acceleration >= 30:  # if player falls off the map, quit program (later implement life system)
        char_alive = False

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

        for tv in active_tvs:
            if tv[2].colliderect(csf_hitbox) and spell_cast[4][1] == 1:
                tv[5] = False  # if tv[5] is False, the tv's alpha will start decreasing
    # code for displaying number of enemies ----------------------------------------------------------#
    # create text for the number of enemies
    enemy_number_text = enemy_counter_font.render('x ' + str(number_of_enemies), True, (255, 255, 255))
    enemy_number_text2 = enemy_counter_font.render('x ' + str(number_of_enemies), True, (0, 0, 0))
    enemy_number_text_rect = enemy_number_text.get_rect()
    enemy_number_text_rect2 = enemy_number_text2.get_rect()
    enemy_number_text_rect.center = (830, 180)
    enemy_number_text_rect2.center = (833, 183)
    # character graphics code ------------------------------------------------------------------------#
    # pygame.draw.rect(screen,(255,0,0),character_hitbox,1)
    # pygame.draw.rect(screen,(0,255,0),character_feet_hitbox,1)
    # pygame.draw.rect(screen, shadow_col, character_feet_shadow, 0)

    if not char_alive:
        if animations_dictionary['death'] == '':
            if save_screen is None:
                save_screen = screen.copy()
            animations_dictionary['death'] = e.create_death_screen(10,pygame.transform.flip(char_frame_to_display,char_animation_flip,False))
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'death',False)
            char_animation_lock = True

    char_shadow = pygame.transform.scale(char_shadow,(character_feet_shadow.w,character_feet_shadow.h))

    if display_shadow:
        screen.blit(char_shadow,character_feet_shadow)

    char_current_frame += 1
    if char_current_frame >= len(animations_dictionary[char_current_animation]) and char_current_animation != 'jump':  # if the current frame is equal to the list length, reset it to 0
        char_current_frame = 0
        if char_current_animation == 'death':
            animations_dictionary['screen_glitch'] = e.create_glitch_screen(save_screen,20)
    if char_current_animation == 'jump' and char_current_frame >= len(animations_dictionary['jump']):
        char_current_frame = len(animations_dictionary['jump']) - 1

    if char_current_animation != 'death':
        char_frame_name = animations_dictionary[char_current_animation][char_current_frame]  # find frame name depending on char current frame
        char_frame_to_display = animation_frame_surfaces[char_frame_name]
    else:
        char_frame_to_display = animations_dictionary['death'][char_current_frame]

    screen.blit(pygame.transform.flip(char_scythe,char_animation_flip, False), (char_x - game_scroll[0] - 15,char_y - game_scroll[1] - 50))
    screen.blit(pygame.transform.flip(char_frame_to_display,char_animation_flip,False),(char_x - game_scroll[0],char_y - game_scroll[1]))  # flip to make the character face the right way
    char_loaded = True

    # HUD ----------------------------------------------------------------------------#

    screen.blit(game_border,(450 - game_border.get_width()//2,300 - game_border.get_height()//2))
    screen.blit(mana_bar, (8, 115))
    mana_bar_fill_bg, mana_bar_fill_sl, mana_bar_fill_fl = e.create_glitch_effect(int(char_mana*0.8), height=8)
    mana_bar_fill_bg.set_alpha(150)
    screen.blit(mana_bar_fill_bg, (13, 135))
    screen.blit(mana_bar_fill_sl, (13, 135))
    screen.blit(mana_bar_fill_fl, (13, 135))
    screen.blit(enemy_counter_bg, (682, 140))
    screen.blit(enemy_number_text2,enemy_number_text_rect2)
    screen.blit(enemy_number_text,enemy_number_text_rect)
    screen.blit(enemy_counter,(659,120))
    screen.blit(level_header,(450 - level_header.get_width()//2,5))
    if frame_count > 30:
        current_level_text = level_font.render('ZONE ' + str(current_level),True,(255,255,255))
        current_level_text2 = level_font.render('ZONE ' + str(current_level),True,(212, 212, 212))
    else:
        current_level_text = level_font.render('ZONE ' + str(current_level),True,(174,135,228))
        current_level_text2 = level_font.render('ZONE ' + str(current_level), True, (221, 203, 245))
    current_level_text_rect = current_level_text.get_rect()
    current_level_text_rect2 = current_level_text2.get_rect()
    current_level_text_rect.center = (450,42)
    current_level_text_rect2.center = (451,43)
    screen.blit(current_level_text2, current_level_text_rect2)
    screen.blit(current_level_text,current_level_text_rect)

    # scroll system --------------------------------------------------------------------------------------------#
    # add text to scroll depending on level
    scroll_surf = pygame.Surface((900,600))
    scroll_surf.set_colorkey((0,0,0))
    scroll_rect = pygame.Rect(scroll_obj[0][0] + 160,scroll_obj[0][1] + 60, scroll_surf.get_width() - 600, scroll_surf.get_height())

    if current_level == 1:
        scroll_text = "This is how I'll be communicating with you. If you want to view/close this scroll, press 'E'. To cast your basic slash attack, hold down the mouse button and drag the following pattern. Good luck! (note: follow the rainbow.)"
        m.drawText(scroll_surf,scroll_text,(49, 52, 56),scroll_rect,scroll_font,aa=True,bkg=None)
        scroll_surf.blit(slash_pic,[scroll_obj[0][0] + 230, scroll_obj[0][1] + 330])
    elif current_level == 2:
        scroll_text = "Good job on clearing those blobs. Seems as if they had mutated from some sort of chemical concoction left laying around. Keep moving onward!"
        m.drawText(scroll_surf,scroll_text,(49, 52, 56),scroll_rect,scroll_font,aa=True,bkg=None)
    elif current_level == 3:
        scroll_text = "You're moving into much more dangerous territory now. I'll show you another spell that will allow you to cast a much more powerful attack - a thunderbolt. Use it at your own discretion, however! It takes a lot of energy. "
        m.drawText(scroll_surf, scroll_text, (49, 52, 56), scroll_rect, scroll_font, aa=True, bkg=None)
        scroll_surf.blit(thunder_pic,[scroll_obj[0][0] + 230, scroll_obj[0][1] + 330])
    elif current_level == 4:
        scroll_text = "I've picked up some traces of another mutation... it appears to be what humans call 'televisions'. However, they're no ordinary televisions - they shoot bullets! Those bullets are indestructible, so don't even try destroying them. I'd recommend getting rid of those TVs first, because they are extremely annoying."
        m.drawText(scroll_surf, scroll_text, (49, 52, 56), scroll_rect, scroll_font, aa=True, bkg=None)
    elif current_level == 5:
        scroll_text = "This is the ultimate test. I'm sensing a significantly higher amount of enemies in this location... so give it your all! Those spells are all you're gonna get. I'll see you on the other side!"
        m.drawText(scroll_surf, scroll_text, (49, 52, 56), scroll_rect, scroll_font, aa=True, bkg=None)

    if scroll_obj[1] and scroll_obj[0][1] >= 100:
        scroll_obj[0][1] -= 15
    elif not scroll_obj[1] and scroll_obj[0][1] <= 650:
        scroll_obj[0][1] += 15

    screen.blit(scroll,scroll_obj[0])
    screen.blit(scroll_surf,(0,0))

    # increase character mana
    if char_mana <= 255 and frame_count % 5 == 0:
        char_mana += 1

    if animations_dictionary['screen_glitch'] != '':
        screen.blit(save_screen,(0,0))
        screen.blit(animations_dictionary['screen_glitch'][char_current_frame % 3],(0,0))
        screen.blit(backdrop,(0,0))
        screen.blit(game_over_txt, game_over_rect)
        screen.blit(game_over_txt_2,game_over_rect_2)

    # detect if level has been finished
    if number_of_enemies == 0 or level_retry:
        level_transition.set_alpha(level_transition_alpha)
        screen.blit(level_transition,(0,0))

        if level_transition_alpha < 400 and not level_fade:
            level_transition_alpha += 10
        else:
            level_fade = True
            if level_timer <= 6:
                level_transition_alpha -= 50
            level_timer += 1

        if not level_retry:
            if level_transition_alpha > 150:
                active_bg_col,active_bg_col2 = (175, 216, 222), (220, 239, 242)
                active_block,active_tree,active_rock = clean_block,clean_tree,clean_rock

            if level_timer >= 300:  # wait approx 5 seconds before transitioning to new level
                level_transition_alpha += 30
                if level_transition_alpha >= 255:
                    # reset variables
                    current_level += 1
                    current_map = load_map(current_level)
                    game_scroll = [0, 0]
                    char_x, char_y = (100, 100)
                    char_alive = True
                    char_current_animation, char_current_frame, char_animation_lock = 'idle', 0, False
                    char_acceleration = 0
                    char_jump, char_fall = False, False
                    save_screen = None
                    animations_dictionary['screen_glitch'], animations_dictionary['death'] = '', ''
                    level_transition_alpha = 0
                    level_timer = 0
                    level_fade = False
                    active_enemies = []
                    active_tvs = []
                    found_tvs = False
                    found_enemies, tile_render_states = False, []
                    level_retry = False
                    found_tiles = False
                    char_mana = 255
                    level_retry = False
                    scroll_obj = [[450 - scroll.get_width()//2,700], True]
                    if current_level % 2 == 0:
                        active_block, active_tree, active_rock = pink_block, pink_tree, pink_rock
                        active_bg_col, active_bg_col2 = (166, 27, 38), (102, 18, 25)
                    else:
                        active_block, active_tree, active_rock = green_block, green_tree, green_rock
                        active_bg_col, active_bg_col2 = (45, 53, 61), (82, 96, 110)
        else:
            if current_level != 5:
                if level_timer >= 1:
                    # reset variables
                    current_map = load_map(current_level)
                    found_tiles = False
                    game_scroll = [0, 0]
                    char_x, char_y = (100, 100)
                    char_alive = True
                    char_current_animation, char_current_frame, char_animation_lock = 'idle', 0, False
                    char_acceleration = 0
                    char_jump, char_fall = False, False
                    save_screen = None
                    animations_dictionary['screen_glitch'], animations_dictionary['death'] = '', ''
                    level_transition_alpha = 0
                    level_timer = 0
                    level_fade = False
                    active_enemies = []
                    active_tvs = []
                    found_tvs = False
                    found_enemies = False
                    found_tiles = False
                    level_retry = False
                    char_mana = 255
                    scroll_obj = [[450 - scroll.get_width()//2,700], True]
            else:
                game_running = False

    frame_count += 1
    if frame_count > 60:
        frame_count = 0

    second_frame_count += 1
    if second_frame_count > 300:
        second_frame_count = 0

    pygame.display.flip()
    clock.tick(FPS)

while True:
    glitch_bgs = e.create_glitch_effect(900,height=600)

    for glitch_bg in glitch_bgs:
        screen.blit(glitch_bg,(0,0))

    screen.blit(intro_overlay_surf,(0,0))
    screen.blit(ending_txt,ending_txt_rect)
    screen.blit(ending_txt2,ending_txt_rect2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(60)
    pygame.display.update()