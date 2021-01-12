import math
import pygame


def check_rect_distance(pos_one,rectangle_pos, distance):
    x1, y1 = pos_one
    # rect_mx, rect_my = (rectangle.x + rectangle.w // 2, rectangle.y + rectangle.h // 2)   # returns midx and midy
    rect_mx, rect_my = rectangle_pos
    d = math.sqrt((x1-rect_mx)**2 + (y1-rect_my)**2)

    if d <= distance:
        return True

