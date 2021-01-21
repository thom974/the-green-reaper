# Credits: pygame wiki for TextWrap function: https://www.pygame.org/wiki/TextWrap#:~:text=Simple%20Text%20Wrapping%20for%20pygame,make%20the%20line%20closer%20together.

import math
import pygame
# pygame.init()
# screen = pygame.display.set_mode((300,300))
# clock = pygame.time.Clock()
# bullet = pygame.image.load('bullet.png').convert()
# bullet.set_colorkey((255,255,255))
# bullet = pygame.transform.scale(bullet,(15,15))
# broken_tv = pygame.image.load('tv.png').convert()
# broken_tv.set_colorkey((255,255,255))
# broken_tv = pygame.transform.scale(broken_tv,(90,80))


def check_rect_distance(pos_one,rectangle_pos, distance):
    x1, y1 = pos_one
    # rect_mx, rect_my = (rectangle.x + rectangle.w // 2, rectangle.y + rectangle.h // 2)   # returns midx and midy
    rect_mx, rect_my = rectangle_pos
    d = math.sqrt((x1-rect_mx)**2 + (y1-rect_my)**2)

    if d <= distance:
        return True


def check_collision(player_hitbox,obj_hitbox):
    player_posx, player_posy = player_hitbox.x, player_hitbox.y
    obj_posx, obj_posy = obj_hitbox.x, obj_hitbox.y

    # check collision for each side of the obj hitbox
    if player_hitbox.colliderect(obj_hitbox):
        # upper side of obj_hitbox
        if player_hitbox.y <= obj_hitbox.y and player_hitbox.x + player_hitbox.w >= obj_hitbox.x and player_hitbox.x <= obj_hitbox.x + obj_hitbox.w:
            return [True,False,False,False]
        # bottom side of obj_hitbox
        elif player_hitbox.y + player_hitbox.h >= obj_hitbox.y + obj_hitbox.h and player_hitbox.x + player_hitbox.w >= obj_hitbox.x and player_hitbox.x <= obj_hitbox.x + obj_hitbox.w:
            return [False,True,False,False]
        # left side of obj_hitbox
        elif player_hitbox.x <= obj_hitbox.x and player_hitbox.y + player_hitbox.y + player_hitbox.h >= obj_hitbox.y and player_hitbox.y <= obj_hitbox.y + obj_hitbox.h:
            return [False,False,True,False]
        # right side of obj_hitbox
        elif player_hitbox.x <= obj_hitbox.x + obj_hitbox.w and player_hitbox.y + player_hitbox.h >= obj_hitbox.y and player_hitbox.y <= obj_hitbox.y + obj_hitbox.h:
            return [False,False,False,True]
    else:
        return [False,False,False,False]


def create_bullet(center,radians):
    x, y = center
    bullets = [[[x,y],[0,0],0] for _ in range(4)]  # create the 4 bullets // location, x + y velocity, speed
    pi_2 = math.pi / 2

    for i in range(4):
        dx = math.cos(radians+i*pi_2)
        dy = math.sin(radians+i*pi_2)
        bullets[i][1][0] = dx
        bullets[i][1][1] = dy

    return bullets


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text