import VL53L0X
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time
import curses
import sys

channel = [15, 14, 13, 11, 10, 9]
gpio = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36]
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 60
'''
for i in range(6):
    pca.channels[channel[i]].duty_cycle = 0xffff
    time.sleep(0.1)
    VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29).change_address(gpio[i])

time.sleep(10)
'''
for ch in channel:
    pca.channels[ch].duty_cycle = 0
    time.sleep(0.1)
