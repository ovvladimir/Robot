from pca9685 import *

servo = PCA9685()
test_channel = 0  # канал на PCA9685 (от 0 до 15)


print("Servo tester...")
print("Cnannel", test_channel)
print("-------------------")
print("Unsigned servo value 0..100%")
print("-------------------")
servo.servos[test_channel].set(signed=False, reverse=False, min_=100, max_=100, trim=0, exp=0)
print("Servo to start position (0%)")
servo.setServo(test_channel, 0)
time.sleep(1)
print("Servo to end position (100%)")
servo.setServo(test_channel, 100)
time.sleep(1)
print("Servo to center (50%)")
servo.setServo(test_channel, 50)
time.sleep(1)
print("Servo to start position (0%)")
servo.setServo(test_channel, 0)
time.sleep(3)

print()

print("-------------------")
print("Signed servo value -100%..100% with Reverse and expand limits to 120%")
print("-------------------")

servo.servos[test_channel].set(signed=True, reverse=True, min_=120, max_=120, trim=0, exp=0)
print("Servo to Zero (center) position (0%)")
servo.setServo(test_channel, 0)
time.sleep(1)
print("Servo to +100%")
servo.setServo(test_channel, 100)
time.sleep(1)
print("Servo to -100%")
servo.setServo(test_channel, -100)
time.sleep(3)

print()

print("-------------------")
print("Unsigned servo value 0%..100% with curve = 100%")
print("-------------------")
servo.servos[test_channel].set(signed=False, reverse=False, min_=100, max_=100, trim=0, exp=100)
servo.setServo(test_channel, 0)
time.sleep(1)

for value in range(100):
    servo.setServo(test_channel, value)
    time.sleep(0.01)

for value in range(100):
    servo.setServo(test_channel, 100 - value)
    time.sleep(0.01)

servo.off()
print("Done.")
