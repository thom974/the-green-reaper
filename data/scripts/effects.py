import pygame
import random


def create_glitch_effect(size_len,**kwargs):
    glitch_colours = [(16, 26, 86), (22, 45, 118), (36, 86, 196), (195, 20, 118), (51, 7, 57), (28, 93, 129),(163, 127, 241), (99, 24, 79), (69, 173, 204)]
    bn = 30
    sn = 100
    height = size_len
    glitch_bg_sl = pygame.Surface((600, 600))
    glitch_bg_fl = pygame.Surface((600, 600))
    glitch_bg = pygame.Surface((600, 600))
    glitch_bg.fill((10, 7, 44))
    glitch_bg.set_alpha(50)
    glitch_bg_fl.set_colorkey((0, 0, 0))
    frame_bg = None

    if 'frame' in kwargs:
        frame_bg = kwargs['frame']
        frame_bg = pygame.transform.scale(frame_bg, (int(size_len * 1.5), int(size_len * 1.5)))

    for _ in range(bn):
        colour = random.choice(glitch_colours)
        w, h = random.randint(300, 400), random.randint(75, 100)
        x, y = random.randint(-50, 550), random.randint(0, 550)
        pygame.draw.rect(glitch_bg_sl, colour, (x, y, w, h), 0)

    for _ in range(sn):
        colour = random.choice(glitch_colours)
        w, h = random.randint(100, 220), random.randint(4, 7)
        x, y = random.randint(-50, 550), random.randint(0, 550)
        pygame.draw.rect(glitch_bg_fl, colour, (x, y, w, h), 0)

    if 'height' in kwargs:
        height = kwargs['height']

    glitch_bg = pygame.transform.scale(glitch_bg, (size_len,height))
    glitch_bg_sl = pygame.transform.scale(glitch_bg_sl, (size_len, height))
    glitch_bg_fl = pygame.transform.scale(glitch_bg_fl, (size_len, height))

    if frame_bg is not None:
        return [glitch_bg,glitch_bg_sl,glitch_bg_fl,frame_bg]
    else:
        return [glitch_bg,glitch_bg_sl,glitch_bg_fl]

