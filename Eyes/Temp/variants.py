'''
import cv2
from imutils.video import VideoStream
import imutils

usingPiCamera = False  # Pi Camera -> True
frameSize = 800

vs = VideoStream(src=0, usePiCamera=usingPiCamera).start()

while True:
    frame = vs.read()
    if not usingPiCamera:
        frame = imutils.resize(frame, width=frameSize)

    cv2.imshow('Camera', frame)
    key = cv2.waitKey(100) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
vs.stop()
'''

'---------------------------------------------------------------------------'
'''
import cv2
import threading


class camThread(threading.Thread):
    def __init__(self, name, camID):
        threading.Thread.__init__(self)
        self.name = name
        self.camID = camID

    def run(self):
        print(f"Starting {self.name}", sep='\n')
        camPreview(self.name, self.camID)


def camPreview(name, camID):
    cv2.namedWindow(name)
    cam = cv2.VideoCapture(camID)

    while cam.isOpened():
        frame = cam.read()[1]
        frame = cv2.resize(frame, (800, 600))
        cv2.imshow(name, frame)
        key = cv2.waitKey(10)
        if key == 27:
            break
    cv2.destroyWindow(name)


thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread1.start()
thread2.start()
'''

'-------------------------------------------------------------------'

import cv2

left = cv2.VideoCapture(0)
right = cv2.VideoCapture(1)

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
# left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
# right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
# right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
# left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
# right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    if not left.grab() or not right.grab():
        print("No more frames")
        break

    leftFrame = left.retrieve()[1]
    rightFrame = right.retrieve()[1]

    cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

left.release()
right.release()
cv2.destroyAllWindows()

'-------------------------------------------------------------'
'''
import cv2
from multiprocessing import Process


def camThread(name, camID):
    cv2.namedWindow(name)
    cam = cv2.VideoCapture(camID)

    while cam.isOpened():
        _, frame = cam.read()
        frame = cv2.resize(frame, (800, 600))
        cv2.imshow(name, frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cam.release()
    cv2.destroyWindow(name)


if __name__ == '__main__':
    thread1 = Process(target=camThread, args=('left', 0))
    thread2 = Process(target=camThread, args=('right', 1))
    threads = [thread1, thread2]
    thread1.start()
    thread2.start()
    for thread in threads:
        thread.join()
'''
'-------------------------------------------------------------'
'''
import cv2
# from multiprocessing import Process
import threading


def f(camID):
    vc = cv2.VideoCapture(camID)
    name = f'preview {camID}'
    cv2.namedWindow(name)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow(name, frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:
            break
    cv2.destroyWindow(name)


if __name__ == '__main__':
    t0 = threading.Thread(target=f, args=(0,))
    t0.start()
    t1 = threading.Thread(target=f, args=(1,))
    t1.start()
    """
    p0 = Process(target=f, args=(0,))
    p0.start()
    p1 = Process(target=f, args=(1,))
    p1.start()
    """
'''
