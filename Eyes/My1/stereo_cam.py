from usbcamvideostream import USBCamVideoStream
from time import localtime, strftime
import cv2

width = 960
W, H = 640, 480
dim = (width, int(H * width / float(W)))

left_eye = USBCamVideoStream(src=0).start()
right_eye = USBCamVideoStream(src=2).start()
cv2.waitKey(1000)
frames = []

while True:
    frames.clear()
    for streams in (left_eye, right_eye):
        if streams.stream.grab():
            frame = streams.retrieves()
            frame = cv2.resize(frame, dim)  # interpolation=cv2.INTER_AREA
            frames.append(frame)
        else:
            break

    ts = strftime("%Y-%m-%d %H:%M:%S", localtime())

    for (frame, name) in zip(frames, ("Left Eye", "Right Eye")):
        cv2.putText(frame, ts, (10, dim[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow(name, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
left_eye.stop()
right_eye.stop()
