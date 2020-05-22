import VL53L0X
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time
import curses
import sys
import os

channel = [15, 14, 13, 11, 10, 9]
gpio = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36]
tofs = []
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 60

for i in range(len(channel)):
    pca.channels[channel[i]].duty_cycle = 0xffff
    time.sleep(0.1)
    VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29).change_address(gpio[i])


def measuring(count, c):
    distance = tofs[count].get_distance()
    if distance > 0:
        print(f'\r\x1b[Ksensor {c} - {distance}mm, {distance / 10.0}cm')
    else:
        print(f'\r\x1b[KError {c}')


for ip in gpio:
    tof = VL53L0X.VL53L0X(i2c_address=ip)
    tof.open()
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
    tofs.append(tof)

# обработка клавиатуры и вывод в терминал
print('\x1b[?25l')
stdscr = curses.initscr()
curses.cbreak()
stdscr.nodelay(1)
stdscr.refresh()
run = True

while run:
    for count in range(len(gpio)):
        if count == 0:
            c = 'RB'
        elif count == 1:
            c = 'RM'
        elif count == 2:
            c = 'RF'
        elif count == 3:
            c = 'LB'
        elif count == 4:
            c = 'LM'
        elif count == 5:
            c = 'LF'
        measuring(count, c)
        time.sleep(.2)
    print('\x1b[7F\x1b[K')
    key = stdscr.getch()
    if key != -1:
        if key == 27:
            break

for tof in tofs:
    tof.stop_ranging()
    tof.close()
for ch in channel:
    pca.channels[ch].duty_cycle = 0
    time.sleep(0.1)
print('\r\x1b[?25h\x1b[0m')
stdscr.refresh()
curses.echo()
curses.endwin()
os.system('clear')
sys.exit(0)
