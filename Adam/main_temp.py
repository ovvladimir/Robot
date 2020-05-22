import pygame as pg
import sys
import math

WIN_WIDTH, WIN_HEIGHT = 640, 480
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
clock = pg.time.Clock()
counts = 0
speed = 0
max_speed = 3
angle = 0
thrust = 0
drag = 0.5
WHITE = (255, 255, 255)

pg.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Adam")

image = pg.image.load('robot.jpeg')
image_rect = image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

text = pg.font.SysFont('Arial', 16, False, False)
txt = '00 cm'
text_pos_1 = (10, 10)
text_pos_2 = (WIN_WIDTH - text.size(txt)[0] - 10, text.size(txt)[1] - 10)
text_pos_3 = (WIN_WIDTH - text.size(txt)[0] - 10, (WIN_HEIGHT - text.size(txt)[1]) // 2)
text_pos_4 = (WIN_WIDTH - text.size(txt)[0] - 10, WIN_HEIGHT - text.size(txt)[1] - 10)
text_pos_5 = (10, WIN_HEIGHT - text.size(txt)[1] - 10)
text_pos_6 = (10, (WIN_HEIGHT - text.size(txt)[1]) // 2)

tofs = [800, 810, 820, 830, 840, 850]
dist = [0, 0, 0, 0, 0, 0]


def text_rangefinder(count):
    if count == 0:
        dist[count] = tofs[count] // 10
    elif count == 1:
        dist[count] = tofs[count] // 10
    elif count == 2:
        dist[count] = tofs[count] // 10
    elif count == 3:
        dist[count] = tofs[count] // 10
    elif count == 4:
        dist[count] = tofs[count] // 10
    elif count == 5:
        dist[count] = tofs[count] // 10

    screen.blit(text.render(f'{dist[0]} cm', True, WHITE, None), text_pos_1)
    screen.blit(text.render(f'{dist[1]} cm', True, WHITE, None), text_pos_6)
    screen.blit(text.render(f'{dist[2]} cm', True, WHITE, None), text_pos_5)
    screen.blit(text.render(f'{dist[3]} cm', True, WHITE, None), text_pos_2)
    screen.blit(text.render(f'{dist[4]} cm', True, WHITE, None), text_pos_3)
    screen.blit(text.render(f'{dist[5]} cm', True, WHITE, None), text_pos_4)

    if 0 < dist[0] < 10 or 0 < dist[1] < 10 or 0 < dist[2] < 10 or \
       0 < dist[3] < 10 or 0 < dist[4] < 10 or 0 < dist[5] < 10:
        return 0


run = True
while run:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            run = False
        elif e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            speed = 0

    keys = pg.key.get_pressed()
    '''
    if keys[97] or keys[100] or keys[115] or keys[119] or \
       keys[273] or keys[274] or keys[275] or keys[276]:
        print(keys.index(1))
    '''
    if keys[pg.K_RIGHT]:
        angle -= 1
    if keys[pg.K_LEFT]:
        angle += 1
    if keys[pg.K_UP]:
        thrust = 1
    elif keys[pg.K_DOWN]:
        thrust = -1
    else:
        thrust = 0

    speed += thrust
    if speed > 0:
        speed -= drag
        if speed < 0:
            speed = 0
    if speed < 0:
        speed += drag
        if speed > 0:
            speed = 0
    if speed > max_speed:
        speed = max_speed
    if speed < -max_speed:
        speed = -max_speed
    angle_radians = -math.radians(angle)
    force_x = math.sin(angle_radians) * speed
    force_y = -math.cos(angle_radians) * speed
    image_rect.x += force_x
    image_rect.y += force_y

    rotated_image = pg.transform.rotate(image, angle)
    image_rect = rotated_image.get_rect(center=image_rect.center)
    screen.fill(BACKGROUND_COLOR)
    screen.blit(rotated_image, image_rect)

    text_rangefinder(counts)
    counts = 0 if counts > len(tofs) - 2 else counts + 1
    pg.display.update()

sys.exit(0)
