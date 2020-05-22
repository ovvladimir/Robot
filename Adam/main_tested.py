import pygame as pg
import sys
import board
import busio
import adafruit_pca9685
import VL53L0X
import time
# from threading import Thread

channel = [9, 10, 11, 13, 14, 15]
gpio = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36]
tofs = []
dist = [0, 0, 0, 0, 0, 0]
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50

WIN_WIDTH, WIN_HEIGHT = 640, 480
BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 30
clock = pg.time.Clock()
counts = 0
speed = 0
angle = 0
SPEED_STEP = 1000

for i in range(len(channel)):
    pca.channels[channel[i]].duty_cycle = 0xffff
    time.sleep(0.1)
    VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29).change_address(gpio[i])

for ip in gpio:
    tof = VL53L0X.VL53L0X(i2c_address=ip)
    tof.open()
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
    tofs.append(tof)

pg.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Adam")

image = pg.image.load('robot.jpeg')
image_rect = image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
rotated_image = pg.transform.rotate(image, 0)

text = pg.font.SysFont('Arial', 16)
txt = '00 cm'
text_pos_1 = (10, 10)
text_pos_2 = (WIN_WIDTH - text.size(txt)[0] - 10, text.size(txt)[1] - 10)
text_pos_3 = (
    WIN_WIDTH - text.size(txt)[0] - 10,
    (WIN_HEIGHT - text.size(txt)[1]) // 2)
text_pos_4 = (
    WIN_WIDTH - text.size(txt)[0] - 10,
    WIN_HEIGHT - text.size(txt)[1] - 10)
text_pos_5 = (10, WIN_HEIGHT - text.size(txt)[1] - 10)
text_pos_6 = (10, (WIN_HEIGHT - text.size(txt)[1]) // 2)


def text_rangefinder(count):
    if count == 0:
        dist[count] = tofs[count].get_distance() // 10
    elif count == 1:
        dist[count] = tofs[count].get_distance() // 10
    elif count == 2:
        dist[count] = tofs[count].get_distance() // 10
    elif count == 3:
        dist[count] = tofs[count].get_distance() // 10
    elif count == 4:
        dist[count] = tofs[count].get_distance() // 10
    elif count == 5:
        dist[count] = tofs[count].get_distance() // 10

    screen.blit(text.render(f'{dist[0]} cm', True, WHITE, None), text_pos_1)
    screen.blit(text.render(f'{dist[1]} cm', True, WHITE, None), text_pos_6)
    screen.blit(text.render(f'{dist[2]} cm', True, WHITE, None), text_pos_5)
    screen.blit(text.render(f'{dist[3]} cm', True, WHITE, None), text_pos_2)
    screen.blit(text.render(f'{dist[4]} cm', True, WHITE, None), text_pos_3)
    screen.blit(text.render(f'{dist[5]} cm', True, WHITE, None), text_pos_4)

    if 0 < dist[0] < 10 or 0 < dist[1] < 10 or 0 < dist[2] < 10 or \
       0 < dist[3] < 10 or 0 < dist[4] < 10 or 0 < dist[5] < 10:
        return 0


def stop():
    pca.channels[0].duty_cycle = 0
    pca.channels[1].duty_cycle = 0
    pca.channels[2].duty_cycle = 0
    pca.channels[3].duty_cycle = 0
    pca.channels[4].duty_cycle = 0
    pca.channels[5].duty_cycle = 0
    pca.channels[6].duty_cycle = 0
    pca.channels[7].duty_cycle = 0
    return 0


run = True
# Thread(target=dy).start()
while run:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            speed = stop()
            for tof in tofs:
                tof.stop_ranging()
                tof.close()
            for ch in channel:
                pca.channels[ch].duty_cycle = 0
                time.sleep(0.1)
            run = False
        elif e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            speed = stop()

    keys = pg.key.get_pressed()
    if keys[273] or keys[274] or keys[275] or keys[276]:
        speed += SPEED_STEP if speed < 65000 else 0
        if keys[pg.K_RIGHT]:
            angle = -90
            pca.channels[0].duty_cycle = speed
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = speed
            pca.channels[4].duty_cycle = speed // 4
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = speed // 4
        if keys[pg.K_LEFT]:
            angle = 90
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = speed // 4
            pca.channels[2].duty_cycle = speed // 4
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = speed
            pca.channels[6].duty_cycle = speed
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_UP]:
            angle = 0
            pca.channels[0].duty_cycle = speed
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = speed
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = speed
            pca.channels[6].duty_cycle = speed
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_DOWN]:
            angle = 180
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = speed
            pca.channels[2].duty_cycle = speed
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = speed
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = speed

    elif keys[97] or keys[100] or keys[115] or keys[119]:
        speed += SPEED_STEP if speed < 65000 else 0
        if keys[pg.K_a] and not keys[pg.K_d] and not keys[pg.K_w] and not keys[pg.K_s]:
            angle = 90
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = speed
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = speed
            pca.channels[4].duty_cycle = speed
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = speed
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_d] and not keys[pg.K_a] and not keys[pg.K_w] and not keys[pg.K_s]:
            angle = -90
            pca.channels[0].duty_cycle = speed
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = speed
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = speed
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = speed
        if keys[pg.K_a] and keys[pg.K_w] and not keys[pg.K_d] and not keys[pg.K_s]:
            angle = 45
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = speed
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = speed
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_d] and keys[pg.K_w] and not keys[pg.K_a] and not keys[pg.K_s]:
            angle = -45
            pca.channels[0].duty_cycle = speed
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = speed
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_a] and keys[pg.K_s] and not keys[pg.K_d] and not keys[pg.K_w]:
            angle = 135
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = speed
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = speed
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_d] and keys[pg.K_s] and not keys[pg.K_a] and not keys[pg.K_w]:
            angle = -135
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = speed
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = speed
        if keys[pg.K_w] and not keys[pg.K_s] and not keys[pg.K_a] and not keys[pg.K_d]:
            angle -= 2
            pca.channels[0].duty_cycle = 0
            pca.channels[1].duty_cycle = speed
            pca.channels[2].duty_cycle = speed
            pca.channels[3].duty_cycle = 0
            pca.channels[4].duty_cycle = 0
            pca.channels[5].duty_cycle = speed
            pca.channels[6].duty_cycle = speed
            pca.channels[7].duty_cycle = 0
        if keys[pg.K_s] and not keys[pg.K_w] and not keys[pg.K_a] and not keys[pg.K_d]:
            angle += 2
            pca.channels[0].duty_cycle = speed
            pca.channels[1].duty_cycle = 0
            pca.channels[2].duty_cycle = 0
            pca.channels[3].duty_cycle = speed
            pca.channels[4].duty_cycle = speed
            pca.channels[5].duty_cycle = 0
            pca.channels[6].duty_cycle = 0
            pca.channels[7].duty_cycle = speed

    screen.fill(BACKGROUND_COLOR)
    rotated_image = pg.transform.rotate(image, angle)
    image_rect = rotated_image.get_rect(center=image_rect.center)
    screen.blit(rotated_image, image_rect)

    stoped = text_rangefinder(counts)
    counts = 0 if counts > len(tofs) - 2 else counts + 1
    if stoped == 0:
        speed = stop()

    pg.display.update()

sys.exit(0)
