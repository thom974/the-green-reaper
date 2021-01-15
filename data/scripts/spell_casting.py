import math
import pygame
import sys
import random
from main import load_animation, animations_dictionary,animation_frame_surfaces

pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

grid_point = pygame.image.load('grid_point.png').convert()
spell_bg = pygame.image.load('spell_bg.png').convert()
grid_point.set_colorkey((255,255,255))
spell_bg.set_colorkey((255,255,255))
grid_point = pygame.transform.scale(grid_point,(30,30))
grid_scale = 1.3
grid_point_diff = 1
grid_points = []
grid_max = False
active_point = 4

spell_cast = [False,[0,0],[],[]]  # spell active, grid location, line points, points touched

# glitch colours
glitch_bg = (10, 7, 44)
glitch_colours = [(16, 26, 86),(22, 45, 118),(36, 86, 196),(195, 20, 118),(51, 7, 57),(28, 93, 129),(163, 127, 241),(99, 24, 79),(69, 173, 204)]
bn = 30
sn = 100

animations_dictionary['slash'] = load_animation('animations/slash',[5,10,7])
print(animations_dictionary['slash'])

# main loop -------------------------------------------------------------#

gsl = 0

while True:
    screen.fill((109, 150, 194))
    # making glitch effect
    if spell_cast[0]:
        glitch_bg_sl = pygame.Surface((600, 600))
        glitch_bg_fl = pygame.Surface((600, 600))
        glitch_bg = pygame.Surface((600,600))
        glitch_bg.fill((10, 7, 44))
        glitch_bg.set_alpha(50)
        glitch_bg_fl.set_colorkey((0, 0, 0))
        frame_bg = spell_bg.copy()

        for _ in range(bn):
            colour = random.choice(glitch_colours)
            w, h = random.randint(300, 400), random.randint(75, 100)
            x, y = random.randint(-50, 550), random.randint(0, 550)
            pygame.draw.rect(glitch_bg_sl, colour, (x, y, w, h), 0)

        glitch_bg_sl.set_alpha(100)

        for _ in range(sn):
            colour = random.choice(glitch_colours)
            w, h = random.randint(100, 220), random.randint(4, 7)
            x, y = random.randint(-50, 550), random.randint(0, 550)
            pygame.draw.rect(glitch_bg_fl, colour, (x, y, w, h), 0)

        glitch_bg = pygame.transform.scale(glitch_bg,(gsl,gsl))
        glitch_bg_sl = pygame.transform.scale(glitch_bg_sl,(gsl,gsl))
        glitch_bg_fl = pygame.transform.scale(glitch_bg_fl,(gsl,gsl))
        frame_bg = pygame.transform.scale(frame_bg,(int(gsl*1.5),int(gsl*1.5)))

        screen.blit(glitch_bg, (spell_cast[1][0] - glitch_bg.get_width()//2, spell_cast[1][1] - glitch_bg.get_height()//2))
        screen.blit(glitch_bg_sl, (spell_cast[1][0] - glitch_bg_sl.get_width()//2, spell_cast[1][1] - glitch_bg_sl.get_height()//2))
        screen.blit(glitch_bg_fl, (spell_cast[1][0] - glitch_bg_fl.get_width()//2, spell_cast[1][1] - glitch_bg_fl.get_height()//2))
        screen.blit(frame_bg,(spell_cast[1][0] - frame_bg.get_width()//2, spell_cast[1][1] - frame_bg.get_height()//2))

    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed(3)

    if mb[0]:
        spell_cast[0] = True
        if spell_cast[1][0] == 0 and spell_cast[1][1] == 0:
            spell_cast[1] = [mx,my]
    else:
        spell_cast[0] = False
        spell_cast[1][0], spell_cast[1][1] = (0,0)
        spell_cast[2] = []
        spell_cast[3] = []
        grid_point_diff = 1
        grid_points = []
        active_point = 4
        grid_max = False
        gsl = 0

    # screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if spell_cast[0]:
        for y in range(3):
            for x in range(3):
                grid_point_loc = [(spell_cast[1][0] - grid_point.get_width()//2 - grid_point_diff * grid_scale) + x * grid_point_diff * grid_scale, (spell_cast[1][1] - grid_point.get_width()//2 - grid_point_diff * grid_scale) + y * grid_point_diff * grid_scale]
                if grid_max and len(grid_points) < 9:
                    grid_points.append(pygame.Rect(grid_point_loc[0], grid_point_loc[1], grid_point.get_width(),grid_point.get_height()))
                screen.blit(grid_point,grid_point_loc)

        if len(grid_points) != 0:
            pygame.draw.line(screen, (0, 0, 0), (grid_points[active_point][0] + grid_point.get_width() // 2,grid_points[active_point][1] + grid_point.get_height() // 2), (mx, my),10)
            for num, rect in enumerate(grid_points):
                if rect.collidepoint(mx,my) and num != active_point:
                    spell_cast[2].append([(grid_points[active_point][0] + grid_point.get_width() // 2,grid_points[active_point][1] + grid_point.get_height() // 2),(rect.x + rect.w//2, rect.y + rect.h//2)])
                    spell_cast[3].append(num)
                    active_point = num

        if len(spell_cast[2]) != 0:  # drawing the existing line connections
            for points in spell_cast[2]:
                x1, y1 = points[0]
                x2, y2 = points[1]
                pygame.draw.line(screen,(0,0,0),(x1,y1),(x2,y2),10)

        if grid_point_diff < 50:
            grid_point_diff += 5
        else:
            grid_max = True
        if gsl < 200:
            gsl += 15

    pygame.display.flip()
    clock.tick(60)

