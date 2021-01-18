import pygame
import random
#
pygame.init()
# screen = pygame.display.set_mode((500,500))
# char = pygame.image.load('char.png').convert()
# char.set_colorkey((255,255,255))
# char = pygame.transform.scale(char,(100,100))


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


def create_death_screen(num,char):
    # set up base frame
    s1, s2, s3 = create_glitch_effect(100)
    s1.set_alpha(255)
    s1.blit(s2,(0,0))
    s1.blit(char, (0, 0))
    s1.blit(s3,(0,0))

    # code for enhanced glitch effect
    glitch_frames = []
    char_frames = []

    for _ in range(3):
        temp = []
        for i in range(num):
            new_rect = pygame.Rect(0,i*100/num,100,100/num)
            new_surf = pygame.Surface((100,100/num))
            new_surf.blit(s1,(0,0),new_rect)
            temp.append(new_surf)
        glitch_frames.append(temp)

    # for _ in range(2):
    #     temp = []
    #     for i in range(cs_num):
    #         new_rect = pygame.Rect(0, i * cs.get_height() / num, cs.get_width(), cs.get_height() / num)
    #         new_surf = pygame.Surface((cs.get_width(), cs.get_height() / num))
    #         new_surf.blit(s1, (0, 0), new_rect)
    #         temp.append(new_surf)
    #     glitch_frames.append(temp)

    for glitch_frame_list in glitch_frames:
        char_surf = pygame.Surface((100,100))
        char_surf.fill((255,255,255))
        char_surf.set_colorkey((255,255,255))
        for j, glitch_frame in enumerate(glitch_frame_list):
            offset = random.randint(-20,20)
            char_surf.blit(glitch_frame,(0 + offset,0+j*100/10))
        for _ in range(50):
            char_frames.append(char_surf)

    return char_frames


def create_glitch_screen(current_screen,num):
    screen_frames = []

    for _ in range(3):
        cs_frame = pygame.Surface((current_screen.get_width(),current_screen.get_height()))
        for i in range(current_screen.get_height()//num):
            offset = random.randint(-100,100)
            new_rect = pygame.Rect(0 + offset, i * current_screen.get_height() / num, current_screen.get_width(), current_screen.get_height() / num)
            cs_frame.blit(current_screen, (0, i * current_screen.get_height() // num), new_rect)
        screen_frames.append(cs_frame)

    return screen_frames


