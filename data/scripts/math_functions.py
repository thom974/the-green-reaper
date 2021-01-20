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

#
# fc = 0
# tv = [[150,100],[],45]  # tv location, bullets, angle
#
# while True:
#     screen.fill((255,255,255))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#
#     if fc % 60 == 0:
#         tv[2] += 23
#         tv[1].extend(create_bullet([150,150],tv[2]))
#
#     remove_bullets = []
#     for b in tv[1]:
#         b[0][0] += b[1][0]
#         b[0][1] -= b[1][1]
#         pygame.draw.circle(screen,(255,0,0),b[0],5,0)
#         screen.blit(bullet,(b[0][0] - bullet.get_width()//2, b[0][1] - bullet.get_height()//2))
#
#     screen.blit(broken_tv,(150 - broken_tv.get_width()//2, 150 - broken_tv.get_height()//2))
#
#     fc += 1
#     clock.tick(60)
#     pygame.display.flip()
