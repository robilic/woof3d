
import pygame
import math
import time

world = [
    1, 2, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 1, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1
]
wx = wy = 10 # world dimensions

ws = 50 # size of each block
p_x = (ws * 5) - 30
p_y = (ws * 5) - 20
p_dx = 0
p_dy = 0
p_heading = 70   # 0 is directly right
md = 3
ray_len = ws * 10

keystates = {
    'w': False,
    'a': False,
    'd': False,
    's': False,
}

def p2m_coords(x, y):
    # change the players floating point coordinates to map coordinates
    map_x = math.floor(x/50)
    map_y = math.floor(y/50)
    return map_x, map_y

screen = pygame.display.set_mode((500, 500))
running = 1
clock = pygame.time.Clock()

while running:
    # draw background
    screen.fill((0, 0, 0))
    for x in range(0, wx):
        for y in range(0, wy):
            if world[(x*10)+y] == 0:
                rect_color = (220,220,220)
            elif world[(x*10)+y] == 1:
                rect_color = (100,100,100)
            elif world[(x*10)+y] == 2:
                rect_color = (0,0,200)
            else:
                rect_color = (50, 50, 50)
            pygame.draw.rect(screen, rect_color, (x*ws, y*ws, ws, ws), 1)

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            keystates['w'] = False
        if event.key == pygame.K_a:
            keystates['a'] = False
        if event.key == pygame.K_d:
            keystates['d'] = False
        if event.key == pygame.K_s:
            keystates['s'] = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            keystates['w'] = True
        if event.key == pygame.K_a:
            keystates['a'] = True
        if event.key == pygame.K_d:
            keystates['d'] = True
        if event.key == pygame.K_s:
            keystates['s'] = True

    # move player if keys are down
    if keystates['w'] is True:
        p_y = p_y + p_dy
        p_x = p_x + p_dx
    if keystates['a']:
        p_heading = p_heading - 5
    if keystates['d']:
        p_heading = p_heading + 5
    if keystates['s']:
        p_y = p_y - p_dy
        p_x = p_x - p_dx

    # calc headings
    if p_heading > 360:
        p_heading = p_heading - 360
    if p_heading < 0:
        p_heading = 360 - p_heading
    
    p_hr = math.radians(p_heading) # save ourself some typing
    
    p_dx = md * math.cos(p_hr)
    p_dy = md * math.sin(p_hr)

    # draw player
    pygame.draw.circle(surface=screen, color=(200, 50, 50), center=(p_x, p_y), radius=4, width=2)

    for i in range(p_heading - 40, p_heading + 40, 2):
        i = math.radians(i)
        ray_dx = (math.cos(i))
        ray_dy = (math.sin(i))
        ray_x = p_x
        ray_y = p_y

        hit = False
        while (hit is False):
            ray_x = ray_x + ray_dx
            ray_y = ray_y + ray_dy
            ray_point = p2m_coords(ray_x, ray_y)
            if world[(ray_point[0] * wx) + ray_point[1]] > 0:
                hit = True
        pygame.draw.line(screen, (50, 255, 50), (p_x, p_y), (ray_x, ray_y), 2)
    

    # calc mini-ray inside game square
    # misc calcs
    p_xo = p_x % ws
    p_yo = p_y % ws
    print(p_x, p_y, p_heading, p_xo, p_yo, p2m_coords(p_x, p_y))

    pygame.display.flip()
    clock.tick(30)


pygame.quit()

