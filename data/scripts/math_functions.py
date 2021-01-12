import math
import pygame

def check_rect_distance(pos_one,rectangle):
    rect_mx, rect_my = (rectangle.x + rectangle.w // 2, rectangle.y + rectangle.h // 2)   # returns midx and midy
    