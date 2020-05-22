# http://edurobots.ru/2020/02/encoder-arduino/
# ТОЛЬКО ДЛЯ LINUX !!!
import RPi.GPIO as GPIO
import time
import curses
import sys
import os

GPIO_Back_Left_Motor = (12, 16)
GPIO_Back_Right_Motor = (20, 21)
GPIO_Front_Left_Motor = (26, 19)
GPIO_Front_Right_Motor = (6, 13)

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_Back_Left_Motor[0], GPIO.IN)
GPIO.setup(GPIO_Back_Left_Motor[1], GPIO.IN)
GPIO.setup(GPIO_Front_Right_Motor[0], GPIO.IN)
GPIO.setup(GPIO_Front_Right_Motor[1], GPIO.IN)
GPIO.setup(GPIO_Back_Right_Motor[0], GPIO.IN)
GPIO.setup(GPIO_Back_Right_Motor[1], GPIO.IN)
GPIO.setup(GPIO_Front_Left_Motor[0], GPIO.IN)
GPIO.setup(GPIO_Front_Left_Motor[1], GPIO.IN)

outcome = [0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0]
run = True

# обработка клавиатуры и вывод в терминал
print('\x1b[?25l')
stdscr = curses.initscr()
curses.cbreak()
stdscr.nodelay(1)
stdscr.refresh()


class Motor():
    def __init__(self, GPIO_a, GPIO_b, text):
        self.last_AB = 0b00  # int('0b00', 0)
        self.meter = 0
        self.GPIO_a = GPIO_a
        self.GPIO_b = GPIO_b
        self.text = text
        self.start = 0

    def update(self):
        A = GPIO.input(self.GPIO_a)
        B = GPIO.input(self.GPIO_b)
        current_AB = (A << 1) | B
        position = (self.last_AB << 2) | current_AB
        self.meter += outcome[position]
        self.last_AB = current_AB

        self.start += 0.1
        if self.start > 100:
            print(f'\r\x1b[K{self.text}{self.meter}')
            self.start = 0


blm = Motor(GPIO_Back_Left_Motor[0], GPIO_Back_Left_Motor[1],
            'Back_Left_Motor: ')
brm = Motor(GPIO_Back_Right_Motor[0], GPIO_Back_Right_Motor[1],
            'Back_Right_Motor: ')
flm = Motor(GPIO_Front_Left_Motor[0], GPIO_Front_Left_Motor[1],
            'Front_Left_Motor: ')
frm = Motor(GPIO_Front_Right_Motor[0], GPIO_Front_Right_Motor[1],
            'Front_Right_Motor: ')

while run:
    blm.update()
    brm.update()
    flm.update()
    frm.update()
    if frm.start == 0:
        print('\x1b[5F\x1b[K')

    key = stdscr.getch()
    if key != -1:
        if key == 27:
            break

# Очистка и выход
print('\r\x1b[?25h\x1b[0m')
stdscr.refresh()
curses.echo()
curses.endwin()
os.system('clear')
sys.exit(0)
