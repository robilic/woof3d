
import pygame
import math
import time

world = [
    1, 2, 1, 2, 1, 2, 1, 2, 2, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 4, 4, 4, 4, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 3, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 3, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 3, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 4,
    1, 1, 1, 1, 1, 1, 1, 1, 4, 4
]
wx = wy = 10 # world dimensions

block_size = 64 # size of each block
p_x = (block_size * 2) + 10
p_y = (block_size * 5)
p_dx = 0 # player horiz direction
p_dy = 0 # player vert direction 
p_heading = 180   # 0 is directly right
md = 3 # movement amount each frame

fov = 60

keystates = {
    'w': False,
    'a': False,
    'd': False,
    's': False,
}

def p2m_coords(x, y):
    # change the players floating point coordinates to map coordinates
    map_x = math.floor(x/block_size)
    map_y = math.floor(y/block_size)
    return map_x, map_y

def one_shade_darker(color_tuple):
    if color_tuple[0] > 25:
        new_red = color_tuple[0] - 25
    else:
        new_red = color_tuple[0]
    if color_tuple[1] > 25:
        new_green = color_tuple[1] - 25
    else:
        new_green = color_tuple[1]
    if color_tuple[2] > 25:
        new_blue = color_tuple[2] - 25
    else:
        new_blue = color_tuple[2]
    return (new_red, new_green, new_blue)

screen = pygame.display.set_mode((1280, 640))
running = 1
clock = pygame.time.Clock()

wall_colors = {
    '0': (220,220,220),
    '1': (150,150,150),
    '2': (0,0,200),
    '3': (200,0,0),
    '4': (25,200,25)
}

while running:
    # draw map on left side
    screen.fill((0, 0, 0))
    grid_size = block_size
    for x in range(0, wx):
        for y in range(0, wy):
            rect_color = wall_colors[str(world[(y*10)+x])]
            pygame.draw.rect(screen, rect_color, (x*grid_size, y*grid_size, grid_size, grid_size), 1)

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
        if event.key == pygame.K_q:
            exit()

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

    # draw the 3D part
    # background
    pygame.draw.rect(screen, (50, 50, 50), (640, 0, 640, 320))
    pygame.draw.rect(screen, (90, 90, 90), (640, 320, 640, 320))
    s = 0 # strip index
    strip_width = 640/(fov)

    for i in range(p_heading - int(fov/2), p_heading + int(fov/2), 1):
        # fix i
        if i > 360:
            i = i - 360
        if i < 0:
            i = 360 - i

        ray_dx = (math.cos(math.radians(i)))
        ray_dy = (math.sin(math.radians(i)))
        ray_x = p_x
        ray_y = p_y

        hit = False

        while (hit is False):
            ray_y = ray_y + ray_dy
            ray_point = p2m_coords(ray_x, ray_y)
            if world[(ray_point[1] * wy) + ray_point[0]] > 0:
                ray_length = math.sqrt(((p_x - ray_x)**2) + ((p_y - ray_y)**2))
                ray_length = ray_length * math.cos(math.radians(p_heading-i))
# int lineH = (mapS*320)/(disH); if(lineH>320){ lineH=320;}                     //line height and limit
# int lineOff = 160 - (lineH>>1);                                               //line offset
                strip_height = (block_size*640) / ray_length
                if strip_height > 640:
                    strip_height = 640
                strip_top = 320 - (strip_height / 2)
                hit = True
                strip_color = wall_colors[str(world[(ray_point[1] * wy) + ray_point[0]])]
                pygame.draw.rect(screen, strip_color, (640+(s*strip_width), strip_top, strip_width, strip_height))
                break
            # color horizontal walls different color than vertical
            ray_x = ray_x + ray_dx
            ray_point = p2m_coords(ray_x, ray_y)
            if world[(ray_point[1] * wy) + ray_point[0]] > 0:
                ray_length = math.sqrt(((p_x - ray_x)**2) + ((p_y - ray_y)**2))
                ray_length = ray_length * math.cos(math.radians(p_heading-i))
                strip_height = (block_size*640) / ray_length
                if strip_height > 640:
                    strip_height = 640
                strip_top = 320 - (strip_height / 2)
                hit = True
                strip_color = wall_colors[str(world[(ray_point[1] * wy) + ray_point[0]])]
                pygame.draw.rect(screen, one_shade_darker(strip_color), (640+(s*strip_width), strip_top, strip_width, strip_height))
                break

        # draw the ray
        pygame.draw.line(screen, (50, 255, 50), (p_x, p_y), (ray_x, ray_y), 2)
        s = s + 1

    pygame.display.flip()
    clock.tick(30)


pygame.quit()

