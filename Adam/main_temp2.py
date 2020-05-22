import pygame as pg
import sys
import time
# from threading import Thread


WIN_WIDTH, WIN_HEIGHT = 640, 480
BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 30
clock = pg.time.Clock()
counts = 0
speed = 0
angle = 0
SPEED_STEP = 1000

pg.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Adam")

image = pg.image.load('robot.jpeg')
image_rect = image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
rotated_image = pg.transform.rotate(image, 0)


def stop():
    return 0


run = True
# Thread(target=dy).start()
while run:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            speed = stop()
            run = False
        elif e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            speed = stop()

    keys = pg.key.get_pressed()
    if keys[273] or keys[274] or keys[275] or keys[276]:
        speed += SPEED_STEP if speed < 65000 else 0
        if keys[pg.K_RIGHT] and keys[pg.K_UP]:
            angle = -45
        elif keys[pg.K_LEFT] and keys[pg.K_UP]:
            angle = 45
        elif keys[pg.K_RIGHT] and keys[pg.K_DOWN]:
            angle -= 2
        elif keys[pg.K_LEFT] and keys[pg.K_DOWN]:
            angle += 2
        elif keys[pg.K_LEFT]:
            angle = 90
        elif keys[pg.K_RIGHT]:
            angle = -90
        elif keys[pg.K_UP]:
            angle = 0
        elif keys[pg.K_DOWN]:
            angle = 180

    elif keys[97] or keys[100] or keys[115] or keys[119]:
        speed += SPEED_STEP if speed < 65000 else 0
        if keys[pg.K_a] and not keys[pg.K_w] and not keys[pg.K_d] and not keys[pg.K_s]:
            angle = 45
        if keys[pg.K_w] and not keys[pg.K_d] and not keys[pg.K_a] and not keys[pg.K_s]:
            angle = -45
        if keys[pg.K_s] and not keys[pg.K_a] and not keys[pg.K_d] and not keys[pg.K_w]:
            angle = 135
        if keys[pg.K_d] and not keys[pg.K_s] and not keys[pg.K_a] and not keys[pg.K_w]:
            angle = -135

    print(speed)
    screen.fill(BACKGROUND_COLOR)
    rotated_image = pg.transform.rotate(image, angle)
    image_rect = rotated_image.get_rect(center=image_rect.center)
    screen.blit(rotated_image, image_rect)

    pg.display.update()

sys.exit(0)
