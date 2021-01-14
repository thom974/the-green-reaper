import math
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

grid_point = pygame.image.load('grid_point.png').convert()
grid_point.set_colorkey((255,255,255))
grid_point = pygame.transform.scale(grid_point,(30,30))
grid_scale = 1.3
grid_point_diff = 1
grid_points = []
grid_max = False
active_point = 4

spell_cast = [False,[0,0],[]]  # spell active, grid location, lines created


# main loop -------------------------------------------------------------#

while True:
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
        grid_point_diff = 1
        grid_points = []
        active_point = 4
        grid_max = False

    screen.fill((255,255,255))

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

    pygame.display.flip()
    clock.tick(60)

