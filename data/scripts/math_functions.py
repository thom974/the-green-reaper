import math
import pygame
pygame.init()
screen = pygame.display.set_mode((300,300))


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
    bullets = [[center,[0,0],0] for _ in range(4)]  # create the 4 bullets // location, x + y velocity, speed
    pi_2 = math.pi / 2

    for i in range(4):
        dx = math.cos(radians+i*pi_2) / 50
        dy = math.sin(radians+i*pi_2) / 50
        bullets[i][1][0] = dx
        bullets[i][1][1] = dy

    return bullets


fc = 0
tv = [[150,100],[]]  # tv[1] = bullet list
tv[1] = create_bullet([150,150],45)
tv[1][0][0][0] = 160
print(tv[1][0])
print(tv[1][1])
print(tv[1])
# while True:
#     screen.fill((128,128,128))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#
#     tv[1][0][0][0] += tv[1][0][1][0]
#     tv[1][0][0][1] -= tv[1][0][1][1]
#
#     # print("before",tv[1][0])
#
#     tv[1][1][0][0] += tv[1][1][1][0]
#     tv[1][1][0][1] -= tv[1][1][1][1]
#
#     # print("after",tv[1][0])
#
#     pygame.draw.circle(screen,(255,0,0),tv[1][0][0],7,0)
#     # pygame.draw.circle(screen,(255,0,0),tv[1][1][0],7,0)
#
#     pygame.display.flip()
