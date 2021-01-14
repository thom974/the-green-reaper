import math
import pygame


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