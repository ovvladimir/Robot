# https://www.pyimagesearch.com/2016/01/18/multiple-cameras-with-the-raspberry-pi-and-opencv/

from imutils.video import VideoStream
import imutils
from time import localtime, strftime
import cv2
import sys

left_eye = VideoStream(src=0).start()
right_eye = VideoStream(src=2).start()
cv2.waitKey(1000)

while True:
    frames = []
    for stream in (left_eye, right_eye):
        frame = stream.read()
        frame = imutils.resize(frame, width=1024)
        frames.append(frame)

    ts = strftime("%Y-%m-%d %H:%M:%S", localtime())

    for (frame, name) in zip(frames, ("Left Eye", "Right Eye")):
        cv2.putText(frame, ts, (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow(name, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
left_eye.stop()
right_eye.stop()
print('Выход')
sys.exit(0)
