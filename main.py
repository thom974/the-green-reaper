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
                    if not first_etf:  # this conditional executes once per frame. once the first enemy tile is found bool var 'first_etf' becomes True
                        pfet = y  # set the previous first tile to the current y value, because for the first enemy tile there is no 'previous enemy tile'
                        first_etf = True
                        found_e_tile = True
                    if not found_e_tile:  # for every row of tiles, bool var found_e_tile is False until an e tile is found
                        if y - 1 == pfet:  # if this first enemy tile has a y value of 1 more than pfet, it must be a part of the same enemy territory
                            enemy_tiles[-1].append(block_rect)  # append the Rect tile to the last list in enemy_tiles
                            pfet = y  # update pfet to the current y value, so that the next row tests against this value
                            found_e_tile = True  # set found_e_tile to True so this conditional can only execute once
                        else:  # this will execute if the current y value has a difference more than 1 with pfet
                            enemy_tiles.append([])  # create an empty list to represent a new enemy territory
                            enemy_tiles[-1].append(block_rect)  # append to the last list, i.e the one we just created the Rect object
                            pfet = y  # update pfet for next iteration
                            found_e_tile = True  # set to True so this conditional can only execute once per row
                    else:  # this will execute once an enemy tile has already been found in the row
                        enemy_tiles[-1].append(block_rect)  # if an enemy tile exists in the row, the tile must belong with that enemy tile's territory
            elif tile == "4":  # tile num. 4 represents a bridge facing diagonally to the left
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], 101, 101)  #
                if tile == "e":  # checks for enemy tile. this entire conditional is an algorithm which appends to the last list 'enemy_tiles' if an enemy tile is a part of an already existing territory. if not, it appends an empty list to 'enemy_tiles' to symbolize a different territory
                    if not first_etf:  # only execute onces, for the first tile (the first tile has no previous enemy tile)
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
            elif tile == "4":  # tile num. 4 represents a bridge.
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                bridge_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], bridge.get_width(),bridge.get_height())
                blocks.append([block_rect, bridge_rect])
                trees.append(None)
                rocks.append(None)
            elif tile == "5":  # tile num. 5 represents a bridge facing diagonally to the right (same bridge tile as before, but mirrored)
                block_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], 101, 101)
                bridge_rev_rect = pygame.Rect((200 + x * bv - y * bv) - game_scroll[0],(10 + x * bv + y * bv) - game_scroll[1], bridge_reverse.get_width(),bridge_reverse.get_height())
                blocks.append([block_rect, bridge_rev_rect, 'r'])  # additionally append string lateral 'r', which stands for reverse. this allows the program to diffrentiate from left/right facing bridges
                trees.append(None)
                rocks.append(None)

    # create the list of enemies
    if len(active_enemies) == 0:  # list 'active_enemies' will be empty during the very first frame of each level
        for _ in enemy_tiles:  # enemy_tiles is a list of lists, containing all the enemy territories (which are made up of sequences of tiles)
            active_enemies.append(slime_obj.copy())  # for each territory, append a copy of slime_obj as there will be one slime per territory

    # save number of tvs
    if not found_tvs:  # will only execute once per level
        number_of_tvs = len(active_tvs)
        found_tvs = True  # once we have saved the original number of TVs, bool var found_tvs becomes False

    # hold the original number of enemies on the stage. e.g if ZONE 1 has 5 enemies, this will store 5 every frame
    number_of_enemies = len(active_enemies) + len(active_tvs)  # take the sum of the list lengths of active_enemies and active_tvs, as they are the mobs the player fights

    # create a list ONCE containing boolean values for each tile // this is for creating a 'render distance' effect
    if not found_tiles:
        tile_render_states = [False for block in blocks]  # each block tile will get its own bool var starting at False. once it becomes True, the block is permanently rendered on the screen for that level
        found_tiles = True

    # checking if a certain tile should be rendered on screen
    for num, block_info in enumerate(blocks):  # use enumerate to keep track of the block number, as tile_render_states is a related list
        block_center = (block_info[1].x + block_info[1].w // 2, block_info[1].y + block_info[1].h // 2)  # represent the center of actual tile image. block_info[1] corresponds to 'green_block_rect', has same dimensions as the tile's image

        if m.check_rect_distance(char_center,block_center,500):  # func returns True if distance between character's current center and the block_center created just above is less than 500
            tile_render_states[num] = True  # set the current block's render state to True

        if tile_render_states[num]:  # if a tile's render state is True, blit its actual Surface onto the screen depending on its dimensions
            if block_info[1].h == 170:  # the ground tile's Surface height is 170, so this will blit a ground tile at the specified location (block_info[0]) holds the blit location in the form of a Rect
                screen.blit(active_block, block_info[0])
            elif block_info[1].h == 169 and 'r' not in block_info:  # the bridge tile has a height of 169. if 'r' is not found, it will blit a left facing bridge at the specified location
                screen.blit(bridge, block_info[0])
            else:  # otherwise, the base tile must be a reverse bridge, so blit a reversed bridge at the specified location
                screen.blit(bridge_reverse, block_info[0])

            if trees[num] is not None:  # if at the current index a tree list is found (looks like this [tree_rect,tree_hitbox]), blit a tree at that location
                screen.blit(active_tree,trees[num][0])
            if rocks[num] is not None:  # if at the current index a rock list is found, blit a rock at the location
                screen.blit(active_rock,rocks[num][0])

    for j, area in enumerate(enemy_tiles):  # iterate through each territory (area) in enemy_tiles
        for i, e_tile in enumerate(area):  # iterate through each individual tile in the area
            if i == 0 and active_enemies[j][1][0] == 0 and active_enemies[j][1][1] == 0:  # active_enemies[j][1] represents the slime at index j's location, in the form of [x,y]. this conditional will evaluate once for each slime object as they start off with location [0,0]
                active_enemies[j][1] = [e_tile.x, e_tile.y]  # this represents the slime's spawning location within its territory. it is the first tile in the upper left corner of its area.
            active_enemies[j][3].append(e_tile)  # append each 'territory tile' to slime's territory tiles list

    # handling all enemy actions, drawing the enemy, moving it, etc. -------------------------------------------------------------------#
    for e_num, enemy in enumerate(active_enemies):  # iterate through each slime enemy in active_enemies, var enemy represents a list containing all necessary info
        enemy_loc = enemy[1]  # store the current enemy's location, enemy_loc is in the form of [x,y]
        enemy_left = False  # bool val to check whether or not a slime has left its territory

        if enemy[6] == 'move':  # index 6 represents the slime's animation. if it is 'move', set the enemy's current frame (animation) to its default
            enemy_cf = animations_dictionary[enemy[0]][enemy[2]]  # enemy_cf stands for enemy current frame and holds a frame name (e.g slime0). enemy[0] is equal to 'slime' and enemy[2] holds the slime's frame number, so that new frames can be are played
        else:  # slime has two possible animations, the other being when it is hurt
            enemy_cf = animations_dictionary['slime_dmg'][enemy[2]]  # set the current frame to be a part of the 'slime_dmg' animation

        enemy_surf = animation_frame_surfaces[enemy_cf]  # given the name of the frame, grab its actual Surface to be blitted from dictionary
        enemy_surf.set_alpha(enemy[9])  # enemy[9] represents the alpha each slime frame should have. this allows the slime to 'fade out' once it dies
        enemy[5] = pygame.Rect(enemy_loc[0] - game_scroll[0],enemy_loc[1] - game_scroll[1],animation_frame_surfaces[enemy_cf].get_width(),animation_frame_surfaces[enemy_cf].get_height())  # create a Rect object representing the enemy's current hitbox, which is offsetted by the game's scroll

        if char_loaded:  # bool val that turns True once character's hitboxes are created, because as of now they do not exist
            if not char_up:  # if the character is not moving upwards, its hitbox will be its feet
                if enemy[5].colliderect(character_feet_hitbox) and enemy[9] >= 255:  # check for slime hitbox + char hitbox collision and also if whether or not the slime is on the screen (alpha >= 255)
                    char_alive = False  # if collision occured, character is dead, set char_alive to False
            else:  # otherwise, its hitbox will be its shadow
                if enemy[5].colliderect(character_feet_shadow) and enemy[9] >= 255:
                    char_alive = False

        if enemy[7]:  # bool val // if true, display slime's HP bar
            screen.blit(hp_bar,[enemy_loc[0] - game_scroll[0] + 15, enemy_loc[1] - game_scroll[1] - 20])  # blit hp_bar on screen
            health_val = pygame.Rect(enemy_loc[0] - game_scroll[0] + 20, enemy_loc[1] - game_scroll[1] - 16, enemy[8] * 25, 8)  # display the slime's current HP value
            pygame.draw.rect(screen,(255,0,0),health_val,0)  # draw the health value Rect

        if enemy[8] <= 0:  # enemy[8] represents the HP of the slime. if it is 0 or less, start making the enemy 'fade out' (decrease its alpha val)
            enemy[9] -= 40  # decrease alpha

        screen.blit(enemy_surf,[enemy_loc[0] - game_scroll[0], enemy_loc[1] - game_scroll[1]])  # blit the enemy Surface
        enemy[2] += 1  # increase each enemy's current frame number by 1 each iteration

        # handle enemy movement ----------------------------------------#
        # moving enemy on screen // enemy[4] represents the current direction the slime is heading in
        if enemy[4] == 'right':  # due to isometric rendering, 'right' is diagonal to the bottom right
            enemy[1][0] += 0.5
            enemy[1][1] += 0.5
        elif enemy[4] == 'left':  # isometric rendering, left is diagonal to the top left
            enemy[1][0] -= 0.5
            enemy[1][1] -= 0.5
        elif enemy[4] == 'up':  # isometric rendering, up is diagonal to the top right
            enemy[1][0] += 0.5
            enemy[1][1] -= 0.5
        elif enemy[4] == 'down':  # isometric rendering, down is diagonal to the bottom left
            enemy[1][0] -= 0.5
            enemy[1][1] += 0.5

        # check if enemy left territory
        for territory_tile in enemy[3]:  # this will iterate through each territory tile in its territory/area
            if territory_tile.colliderect(enemy[5]):  # if at any point the slime is still inside its territory, i.e collides with one of its tiles, break
                break
        else:  # if the for loop finishes executing, that means the slime has not collided with any territory tiles
            enemy_left = True  # slime has left, set enemy_left to True

        # handle direction changing
        if enemy_left:  # first check if enemy has left its territory
            direc = enemy[4]  # save the location the slime is currently travelling in
            if direc == 'right':  # the enemy will change direction depending on the direction it was moving before it exited its territory
                enemy[4] = 'down'
                enemy[1][0] -= 25  # once the slime has left its territory, it needs to be set back inside it
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
            enemy_left = False  # once the enemy has changed direction and is reset back into its territory, set this back to False

        if enemy[2] >= len(animations_dictionary[enemy[0]]) and enemy[6] == 'move':  # if the current frame is equal to the last index of its current animation list, reset frame count to 0
            enemy[2] = 0  # reset frame count to 0
        elif enemy[2] >= len(animations_dictionary['slime_dmg']) and enemy[6] == 'hurt':  # reset frame number if it is equal to the max index of animation 'hurt'
            enemy[2] = 0
            enemy[6] = 'move'  # additionally once the hurt animation is over, change animation back to 'move'

        enemy[3] = []  # clear the enemy's territory tiles

        if enemy[9] <= 0:  # once the enemy is completely invisible (alpha <= 0)
            number_of_enemies -= 1  # subtract one from enemy counter
            enemy[7] = False  # don't show hp bar

    # handling all tv actions -----------------------------------------------------------------------------------#
    for tv_num,tv in enumerate(active_tvs):  # iterate through each tv (each tv is a list containing all its info)
        tv[0].set_alpha(tv[6])  # set the alpha of the tv's Surface being blitted to the alpha value stored in its list
        tv[2] = pygame.Rect(tv[1][0] - game_scroll[0], tv[1][1] - game_scroll[1], broken_tv.get_width(), broken_tv.get_height())  # create and store the tv hitbox in the tv list
        screen.blit(tv[0],(tv[1][0] - game_scroll[0], tv[1][1] - game_scroll[1]))  # displays the actual TV image/Surface

        if tv[2].colliderect(character_feet_hitbox) and tv[5]:  # if the tv hitbox collides with the character's feet hitbox, and the tv is not destroyed
            char_alive = False  # set character to dead

        if frame_count == 59 and tv[5]:  # for every 59th frame, if the tv is not destroyed, this will execute
            tv[4] += tv[6]  # increase the tv's bullet angle by the current angle stored in tv[6]
            tv[4] = 0 if tv[4] > 360 else tv[4]  # reset angle back to 0 if angle is greater than 360, keeps numbers small
            b_loc = [tv[2].x + tv[2].w//2 + game_scroll[0], tv[2].y + tv[2].h//2 + game_scroll[1]]  # create the spawn point for the bullets
            tv[3].extend(m.create_bullet(b_loc,tv[4]))  # create_bullet returns a list of 4 bullets, each with varying angles. extend the tv's bullet list with these 4
            if len(tv[3]) >= 20:  # if the bullet list contains 20 or more bullets, delete the first 4 bullets in the list
                del tv[3][:5]

        if len(tv[3]) != 0:  # only executes if there are bullets in the tv's bullet list
            for b in tv[3]:  # for loop to iterate through each bullet
                b[0][0] += b[1][0]  # b[0] contains the bullet's location ([x,y]), b[1] contains bullet's x/y velocity ([x,y]). this line adds x velocity to the x cord
                b[0][1] -= b[1][1]  # subtract y velocity from bullet's y cord because of pygame's inverted y-axis
                b_hitbox = pygame.Rect(b[0][0] - bullet.get_width()//2 - game_scroll[0], b[0][1] - bullet.get_height()//2 - game_scroll[1], bullet.get_width(), bullet.get_height())  # create the bullet's hitbox
                screen.blit(bullet,(b[0][0] - bullet.get_width()//2 - game_scroll[0], b[0][1] - bullet.get_height()//2 - game_scroll[1]))  # draw the bullet onto the screen

                if b_hitbox.colliderect(character_hitbox):  # if the bullet hitbox collides with the character, they die
                    char_alive = False

        if not tv[5]:  # start decreasing its alpha if hit by spell
            tv[6] -= 40

        if tv[6] <= 0:  # once the alpha is 0 or less, always set the alpha to 0 and subtract from num of enemies
            tv[6] = 0
            number_of_enemies -= 1

    # making glitch effect for spell casting ----------------------------------------------#
    if spell_cast[0]:   # if player clicked mouse one (the 3x3 grid is opening)
        glitch_bg, glitch_bg_sl, glitch_bg_fl, frame_bg = e.create_glitch_effect(gsl,frame=spell_bg.copy())

        # display all glitch layers
        screen.blit(glitch_bg,(spell_cast[1][0] - glitch_bg.get_width() // 2, spell_cast[1][1] - glitch_bg.get_height() // 2))
        screen.blit(glitch_bg_sl, (spell_cast[1][0] - glitch_bg_sl.get_width() // 2, spell_cast[1][1] - glitch_bg_sl.get_height() // 2))
        screen.blit(glitch_bg_fl, (spell_cast[1][0] - glitch_bg_fl.get_width() // 2, spell_cast[1][1] - glitch_bg_fl.get_height() // 2))
        screen.blit(frame_bg,(spell_cast[1][0] - frame_bg.get_width() // 2, spell_cast[1][1] - frame_bg.get_height() // 2))

    mx, my = pygame.mouse.get_pos()  # store current mouse position
    mb = pygame.mouse.get_pressed(3)  # mousebutton // will contain a list indicating which mouse buttons from 1-3 have been pressed

    # character code -----------------------------------------------------#
    # detect collision
    for rock in rocks:  # iterate through each rock in rock list
        if rock is not None:  # if a rock exists, this will execute
            rock_hb = rock[1]  # store rock hitbox
            if not char_jump:  # if the character is not jumping, collision will occur with the character's feet hitbox
                collisions = m.check_collision(character_feet_hitbox,rock_hb)  # returns a list holding four booleans, which represent the 4 side lengths of the hitbox. one boolean will equal True, indicating the specific side length the player collided with
            else:  # if the character is jumping, collisions will occur with the character's shadow hitbox
                collisions = m.check_collision(character_feet_shadow,rock_hb)
            if collisions[0]:  # if player collided with upper side of hitbox, repel char back upwards
                char_y -= 5
            elif collisions[1]:  # if player collided with bottom, repel char downwards
                char_y += 5
            elif collisions[2]:  # if player collided with left, repel char to the left
                char_x -= 5
            elif collisions[3]:  # if player collided with right, repel char to the right
                char_x += 5

    for tree in trees:  # same exact concept as with checking rock collisions
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

    if not char_jump:  # if the character is not jumping, its shadow hitbox will depend on its current 'char_y' val
        character_feet_shadow = pygame.Rect(char_x - game_scroll[0] + 10,char_y - game_scroll[1] + 80,70,20)
    else:  # if char jumping, shadow must stay on the ground, location based on 'char_prev_ypos' which holds the y val right before the char jumps
        character_feet_shadow = pygame.Rect(char_x - game_scroll[0] + 10,char_prev_ypos - game_scroll[1] + 80,70,20)

    # character movement
    if char_alive:  # character can only move if they are alive
        if char_up:  # if character moving up, subtract from char_y
            char_y -= char_speed
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)  # set animation to 'walk' if character is moving
            if char_jump:  # if char is jumping and is moving up, move the prev_ypos up as well (so shadow is not stationary mid-jump)
                char_prev_ypos -= char_speed
        if char_down:  # same idea, if char is moving down, add to char_y
            char_y += char_speed
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)  # same idea, change animation to 'walk'
            if char_jump:  # if char is jumping but is moving down, add to prev_ypos so shadow moves down the screen
                char_prev_ypos += char_speed
        if char_left:
            char_x -= char_speed
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)
            char_animation_flip = False
        if char_right:
            char_x += char_speed
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'walk',char_animation_lock)
            char_animation_flip = True
        if char_jump:  # handle character jumping
            char_y -= char_acceleration  # subtract from char_y to move char upwards, once char_accel becomes negative the char will move downwards
            char_acceleration -= 1  # decrease char_accel to change the rate at which char_y is changing
            if char_y - game_scroll[1] + 90 > character_feet_shadow.y:  # plus 90 to detect bottom edge of character // once char_y hits the top of the char's shadow location, jump is over
                char_jump = False  # char has grounded, character is no longer jumping
                char_animation_lock = False  # set animation lock to False so character can change animations
                char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'idle',char_animation_lock)  # set animation to idle as character has landed, reset char frame number to 0

    # check if character fallen
    block_touched = False  # bool val which indicates whether or not the char is currently in contact with a block
    if not char_fall:  # if the character is not falling off the map
        for num, block_hitbox in enumerate(blocks):  # iterate through each block list, which holds each block hitbox
            if character_feet_shadow.colliderect(block_hitbox[0]):  # block_hitbox[0] is where the hitbox is located. if the character's shadow is contacting it, this conditional becomes True
                display_shadow = True  # display the shadow beneath the char
                block_touched = True
        else:  # executes once for loop has exhausted
            if not block_touched:  # if a block was not touched, do not display shadow beneath player
                display_shadow = False
            if not block_touched and not char_jump:  # if a block was not touched + the character is not currently jumping, they will fall off the map
                char_fall = True
                char_acceleration = 10  # set acceleration for when char is falling

    if char_fall:  # if character is falling, increase char_y so character moves downwards, increase accel so they move down increasingly fast
        char_y += char_acceleration
        char_acceleration += 1

    if char_acceleration >= 30:  # once the player reaches a high enough accel (from falling off map) set alive state to False
        char_alive = False

    # spell casting code ------------------------------------------------------------------------#
    if mb[0]:  # if mouse button one was pressed, this will execute
        spell_cast[0] = True  # set spell active state to True
        if spell_cast[1][0] == 0 and spell_cast[1][1] == 0:  # if no location exists in spell_cast, this will execute
            spell_cast[1] = [mx, my]  # set spell 3x3 grid location to current mouse location (this will be the exact center of the grid)
    else:  # if mouse button one is not being pressed, this will execute
        if len(spell_cast[3]) != 0:  # check if the user connected any grid points while spell grid was active
            for spell_name, spell_info in spells_dictionary.items():  # iterate through each key + value pair in spells_dict
                spell_points, spell_cost = spell_info  # unpack spell_info list into the points connected (spell_points) and the spell cost (spell_cost)
                if char_mana - spell_cost > 0:  # check if the character has enough mana to cast the spell
                    if spell_points == spell_cast[3]:  # compare the points the user connected (spell_cast[3]) to spell_points in the dictionary. if there is a match, this will execute
                        spell_cast[4][0] = spell_name  # add to spell_cast the name of the spell which is being casted
                        char_mana -= spell_cost  # subtract the mana cost of the spell
            spell_cast[4][2] = spell_cast[1].copy()  # give the current location the grid is being drawn at to the list containing the info on drawing the spell

        # everytime mb 1 is released, reset all spell-related variables
        spell_cast[0], spell_cast[2], spell_cast[3] = False, [], []
        spell_cast[1][0], spell_cast[1][1] = (0, 0)
        grid_point_diff, grid_points, active_point, gsl = 1, [], 4, 0
        grid_max = False

    if spell_cast[0]:  # if spell grid is active, this will execute
        for y in range(3):  # nested loop to draw each grid_point on the screen (3 rows, 3 columns)
            for x in range(3):
                grid_point_loc = [(spell_cast[1][0] - grid_point.get_width() // 2 - grid_point_diff * grid_scale) + x * grid_point_diff * grid_scale,(spell_cast[1][1] - grid_point.get_width() // 2 - grid_point_diff * grid_scale) + y * grid_point_diff * grid_scale]  # create location of the grid point
                if grid_max and len(grid_points) < 9:  # make sure grid_points can only contain 9 points at max
                    grid_points.append(pygame.Rect(grid_point_loc[0], grid_point_loc[1], grid_point.get_width(),grid_point.get_height()))  # append Rect object representing where the grid point is to be blitted
                screen.blit(grid_point, grid_point_loc)  # draw the actual grid point image at the created location

        if len(grid_points) != 0:  # True if there are grid points currently in the list
            pygame.draw.line(screen, (0, 0, 0), (grid_points[active_point][0] + grid_point.get_width() // 2,grid_points[active_point][1] + grid_point.get_height() // 2),(mx, my), 10)  # draw line from current active point to mouse position
            for num, rect in enumerate(grid_points):  # iterate through each grid point (which is actually a Rect obj) in the list, use enumerate to keep track of the grid point's associated number
                if rect.collidepoint(mx, my) and num != active_point:  # check if the Rect obj collides with the current mouse position, as long as the Rect obj is not the one currently active
                    spell_cast[2].append([(grid_points[active_point][0] + grid_point.get_width() // 2,grid_points[active_point][1] + grid_point.get_height() // 2),(rect.x + rect.w // 2, rect.y + rect.h // 2)])  # append the center of the grid point which is currently active, and the center of the grid point the mouse collided with
                    spell_cast[3].append(num)  # append the grid point which was contacted to point history
                    active_point = num  # active point now becomes the grid point which was just contacted

        if len(spell_cast[2]) != 0:  # drawing the existing line connections
            for points in spell_cast[2]:  # iterate through each list of points in line history, to draw the lines
                x1, y1 = points[0]  # represents location of the active grid point
                x2, y2 = points[1]  # represents location of the point the active grid point connected with
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 10)  # draw a line between these two points

        if grid_point_diff < 50:  # this is used to scale the difference between grid points, once it is 50 or more, grid has reached its max size
            grid_point_diff += 5
        else:  # stop increasing grid_point_diff
            grid_max = True  # set grid_max to True to indicate grid has reached max size

        if gsl < 170:  # grid side length // used to scale overall size of the grid
            gsl += 15  # increment by 15 if under 170

    # spell animation handling
    if spell_cast[4][0] != '':  # check if a spell is currently stored, if one was cast
        current_spell_frame = animations_dictionary[spell_cast[4][0]][spell_cast[4][1]]  # store the name of the frame to be displayed in the animation
        csf_surf = animation_frame_surfaces[current_spell_frame]  # current spell frame surface // store the actual Surface/image to be displayed given the current frame name
        if spell_cast[4][0] == 'slash':  # if user casted a 'slash' attack
            csf_center = (spell_cast[4][2][0] - csf_surf.get_width()//2, spell_cast[4][2][1] - csf_surf.get_height()//2)  # create location for the current spell frame to be displayed at, will be the center of the grid
            csf_hitbox = pygame.Rect(csf_center[0], csf_center[1], csf_surf.get_width(), csf_surf.get_height())  # create the hitbox of the frame being displayed
        elif spell_cast[4][0] == 'thunder':  # if user casted a 'thunder' attack
            csf_center = (spell_cast[4][2][0] - csf_surf.get_width()//2, spell_cast[4][2][1] - csf_surf.get_height() + 50)  # create center of frame
            csf_hitbox = pygame.Rect(csf_center[0], csf_center[1] + 350, csf_surf.get_width(), csf_surf.get_height()-400)  # create hitbox
        screen.blit(csf_surf, csf_center)  # draw the actual frame of the spell at the center of the grid
        spell_cast[4][1] += 1  # increase spell's frame count by 1 so new frames in the animation are played
        if spell_cast[4][1] >= len(animations_dictionary[spell_cast[4][0]]):  # once the animation is finished (frame count reached its max), reset the list holding all spell animation info
            spell_cast[4] = ['', 0, [0, 0]]

    # code for combat detection-----------------------------------------------------------------------#

        for enemy in active_enemies:  # iterate through each enemy in enemy list
            if enemy[5].colliderect(csf_hitbox) and spell_cast[4][1] == 1 and char_alive:  # check if enemy collided with spell hitbox, makes sure detection occurs once per spell cast and player is alive
                enemy[2] = 0  # set enemy current frame to 0 as new animation will play
                enemy[6] = 'hurt'  # set animation to 'hurt' as the enemy is being hit by a spell
                enemy[7] = True  # display the enemy's HP bar
                if spell_cast[4][0] == 'slash':  # if user casted a slash attack, subtract 1 HP
                    enemy[8] -= 1
                elif spell_cast[4][0] == 'thunder':  # if user casted a slash attack, subtract 2 HP
                    enemy[8] -= 2

        for tv in active_tvs:  # iterate through each tv in tv list
            if tv[2].colliderect(csf_hitbox) and spell_cast[4][1] == 1:  # if the spell hitbox collides with the tv hitbox, this will execute
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

    if not char_alive:  # check if player is not alive
        if animations_dictionary['death'] == '':  # only executes when no animation is loaded in under the key 'death'
            if save_screen is None:  # store value in save_screen only once
                save_screen = screen.copy()  # save_screen holds a copy of the screen once the player dies, used to create a glitchy bg
            animations_dictionary['death'] = e.create_death_screen(10,pygame.transform.flip(char_frame_to_display,char_animation_flip,False))  # func returns a death animation list given the char's current frame
            char_current_animation, char_current_frame = change_animation(char_current_animation,char_current_frame,'death',False)  # change animation to 'death' so this death animation plays out, change frame number to 0
            char_animation_lock = True  # character can no longer change animation once they die

    char_shadow = pygame.transform.scale(char_shadow,(character_feet_shadow.w,character_feet_shadow.h))  # actual image of shadow, scale it to the dimensions of character_feet_shadow Rect

    if display_shadow:  # if True, the shadow will display
        screen.blit(char_shadow,character_feet_shadow)

    char_current_frame += 1  # increase character's current frame by 1

    if char_current_frame >= len(animations_dictionary[char_current_animation]) and char_current_animation != 'jump':  # if the current frame is equal to the list length, reset it to 0
        char_current_frame = 0
        if char_current_animation == 'death':  # if the character is dying, create the glitch screen animation using save_screen which holds a copy of the screen before the char died
            animations_dictionary['screen_glitch'] = e.create_glitch_screen(save_screen,20)

    if char_current_animation == 'jump' and char_current_frame >= len(animations_dictionary['jump']):  # freeze char frame number at the last index of the jump animation
        char_current_frame = len(animations_dictionary['jump']) - 1

    if char_current_animation != 'death':  # if animation is not death, display frame depending on char_frame_name
        char_frame_name = animations_dictionary[char_current_animation][char_current_frame]  # find frame name depending on char current animation and current frame
        char_frame_to_display = animation_frame_surfaces[char_frame_name]  # save the actual Surface to be displayed based on the frame name above
    else:
        char_frame_to_display = animations_dictionary['death'][char_current_frame]  # if animation is death, the Surfaces themselves are already located within the dictionary

    screen.blit(pygame.transform.flip(char_scythe,char_animation_flip, False), (char_x - game_scroll[0] - 15,char_y - game_scroll[1] - 50))  # display the scythe behind the player
    screen.blit(pygame.transform.flip(char_frame_to_display,char_animation_flip,False),(char_x - game_scroll[0],char_y - game_scroll[1]))  # display the character // flip to make the character face the right way
    char_loaded = True

    # HUD ----------------------------------------------------------------------------#
    # display pixelated border, mana bar, enemy counter, ZONE header
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
    if frame_count > 30:  # when frame count greater than/less than 30, the colour of the level header changes
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
    scroll_surf = pygame.Surface((900,600))  # create Surface which matches the size of the screen, this is where the scroll text will be drawn onto
    scroll_surf.set_colorkey((0,0,0))  # make the entire surface transparent (black transparent)
    scroll_rect = pygame.Rect(scroll_obj[0][0] + 160,scroll_obj[0][1] + 60, scroll_surf.get_width() - 600, scroll_surf.get_height())  # create Rect obj which text wraps around

    if current_level == 1:
        scroll_text = "This is how I'll be communicating with you. If you want to view/close this scroll, press 'E'. To cast your basic slash attack, hold down the mouse button and drag the following pattern. Good luck! (note: follow the rainbow.)"
        m.drawText(scroll_surf,scroll_text,(49, 52, 56),scroll_rect,scroll_font,aa=True,bkg=None)  # draw scroll text
        scroll_surf.blit(slash_pic,[scroll_obj[0][0] + 230, scroll_obj[0][1] + 330])  # display a picture of the slash pattern for the tutorial
    elif current_level == 2:
        scroll_text = "Good job on clearing those blobs. Seems as if they had mutated from some sort of chemical concoction left laying around. Keep moving onward!"
        m.drawText(scroll_surf,scroll_text,(49, 52, 56),scroll_rect,scroll_font,aa=True,bkg=None)
    elif current_level == 3:
        scroll_text = "You're moving into much more dangerous territory now. I'll show you another spell that will allow you to cast a much more powerful attack - a thunderbolt. Use it at your own discretion, however! It takes a lot of energy. "
        m.drawText(scroll_surf, scroll_text, (49, 52, 56), scroll_rect, scroll_font, aa=True, bkg=None)
        scroll_surf.blit(thunder_pic,[scroll_obj[0][0] + 230, scroll_obj[0][1] + 330])  # display a picture of the thunder pattern
    elif current_level == 4:
        scroll_text = "I've picked up some traces of another mutation... it appears to be what humans call 'televisions'. However, they're no ordinary televisions - they shoot bullets! Those bullets are indestructible, so don't even try destroying them. I'd recommend getting rid of those TVs first, because they are extremely annoying."
        m.drawText(scroll_surf, scroll_text, (49, 52, 56), scroll_rect, scroll_font, aa=True, bkg=None)
    elif current_level == 5:
        scroll_text = "This is the ultimate test. I'm sensing a significantly higher amount of enemies in this location... so give it your all! Those spells are all you're gonna get. I'll see you on the other side!"
        m.drawText(scroll_surf, scroll_text, (49, 52, 56), scroll_rect, scroll_font, aa=True, bkg=None)

    # move scroll on/off the screen
    if scroll_obj[1] and scroll_obj[0][1] >= 100: # if scroll is active and its y position is greater than 100, move it upwards on screen
        scroll_obj[0][1] -= 15
    elif not scroll_obj[1] and scroll_obj[0][1] <= 650:  # if scroll is not active and its y pos is less than 650, move it downwards
        scroll_obj[0][1] += 15

    screen.blit(scroll,scroll_obj[0])  # blit the scroll to location stored
    screen.blit(scroll_surf,(0,0))  # blit scroll_surf which has all the drawn text on it

    # increase character mana
    if char_mana <= 255 and frame_count % 5 == 0:  # increase only if mana is not maxed, and if frame count is divisble by 5 so mana doesn't replenish too fast
        char_mana += 1

    if animations_dictionary['screen_glitch'] != '':  # if no animation is currently stored under 'screen_glitch' key
        screen.blit(save_screen,(0,0))
        screen.blit(animations_dictionary['screen_glitch'][char_current_frame % 3],(0,0))  # blit the screen glitch frame. % 3 used to return a number from 0-2, as the screen_glitch ani. contains only 3 frames
        screen.blit(backdrop,(0,0))  # display a backdrop which is fairly transparent to reduce the visibility of the glitch screen
        screen.blit(game_over_txt, game_over_rect)
        screen.blit(game_over_txt_2,game_over_rect_2)

    # detect if level has been finished or level is being retried
    if number_of_enemies == 0 or level_retry:
        level_transition.set_alpha(level_transition_alpha)  # set alpha of level_transition surface
        screen.blit(level_transition,(0,0))  # level transition is a white Surface which is used for fade transition

        if level_transition_alpha < 400 and not level_fade:  # if the alpha is less than 400, increase level transition's alpha value making it more opaque
            level_transition_alpha += 10
        else:
            level_fade = True  # once alpha reaches above 400, level has faded out, set level_fade to True
            if level_timer <= 6:
                level_transition_alpha -= 50  # decrease alpha of level_transition once a little time has past, to make the game visible again
            level_timer += 1

        if not level_retry:  # if the level is not being retried, i.e all enemies have been cleared
            if level_transition_alpha > 150:
                active_bg_col,active_bg_col2 = (175, 216, 222), (220, 239, 242)  # set bg colours to 'clean' colours
                active_block,active_tree,active_rock = clean_block,clean_tree,clean_rock  # set active assets to clean assets

            if level_timer >= 300:  # wait approx 5 seconds (300 frames per 5 seconds)  before transitioning to new level
                level_transition_alpha += 30  # increase the alpha so that screen grows increasingly white
                if level_transition_alpha >= 255:  # once the screen is completely opaque with white, this will execute
                    # reset ALL level variables
                    current_level += 1
                    if current_level == 6:
                        game_running = False
                        break
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
        else:  # if level has been retried, not cleared
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

    # frame counter code
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