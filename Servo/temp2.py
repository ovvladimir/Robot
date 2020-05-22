import time
import RPi.GPIO as GPIO

# GPIO_List = [21, 20, 16, 12, 19, 26, 6, 13]
# GPIO_FR = [6, 13]
# GPIO_BL = [12, 16]
# GPIO_BR = [20, 21]
# GPIO_FL = [19, 26]
speed = [0]


def GPIO_FR():
    RCpin = (6, 13)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RCpin[1], GPIO.IN)
    # GPIO.setup(RCpin[0], GPIO.IN)
    # GPIO.wait_for_edge(RCpin[1], GPIO.FALLING)
    GPIO.wait_for_edge(RCpin[1], GPIO.RISING)
    # GPIO.wait_for_edge(RCpin[0], GPIO.BOTH)
    signal_1 = GPIO.input(RCpin[1])
    speed[0] += signal_1
    # signal_2 = GPIO.input(RCpin[1])
    # speed[0] -= signal_2
    print(f'Front Right: {speed[0]} {signal_1}', end='\r', flush=True)


while True:
    GPIO_FR()
    time.sleep(0.1)

'''
GPIO.setmode(GPIO.BCM)
buttons = (6, 13)
GPIO.setup(buttons, GPIO.IN)# pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(6, GPIO.RISING)  # add rising edge detection on a channel
GPIO.add_event_detect(13, GPIO.RISING)  #for both buttons
while True:
    if GPIO.event_detected(6):
        print('Вперед')
    if GPIO.event_detected(13):
        print('Назад')
    time.sleep(0.1)
'''
