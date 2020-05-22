from adafruit_servokit import ServoKit
import time

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
channel = 0
pause = 1
# print(len(kit.servo))

kit.servo[channel].angle = 180
time.sleep(pause)
kit.servo[channel].angle = 0
time.sleep(pause)
