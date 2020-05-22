from threading import Thread
import cv2
import os


class USBCamVideoStream:
    def __init__(self, src=0, name="USBThread"):
        self.stream = cv2.VideoCapture(src)  # cv2.CAP_DSHOW (для Windows)
        cv2.waitKey(1000)
        # self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if os.name != 'nt':
            self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.ret, self.frame = self.stream.read()
        self.name = name
        self.stopped = False

    def start(self):
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            self.ret, self.frame = self.stream.read()

    def retrieves(self):
        return self.frame

    def stop(self):
        self.stopped = True
