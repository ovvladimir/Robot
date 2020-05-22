import numpy as np
import argparse
import pickle
import cv2
import os
from threading import Thread
import pyttsx3

from usbcamvideostream import USBCamVideoStream
from fps import FPS

fps = FPS().start()
block = True
name = None
frames = []


def voice():
    if os.name == 'nt':
        engine = pyttsx3.init(driverName='sapi5')
        engine.say('О-о! Привет, Владимир!')
        engine.runAndWait()
    else:
        # os.system("echo 'О! Привет Владимир!' | RHVoice-test -p Aleksandr")
        os.system("spd-say -o rhvoice -y Aleksandr -r 30 -w 'О-о! Привет, Владимир!'")


ap = argparse.ArgumentParser()
ap.add_argument(
    "-d", "--detector",  # required=True,
    default='face_detection_model',
    help="path to OpenCV's deep learning face detector")
ap.add_argument(
    "-m", "--embedding-model",  # required=True,
    default='face_embedding_model/openface_nn4.small2.v1.t7',
    help="path to OpenCV's deep learning face embedding model")
ap.add_argument(
    "-r", "--recognizer",  # required=True,
    default='output/recognizer.pickle',
    help="path to model trained to recognize faces")
ap.add_argument(
    "-l", "--le",  # required=True,
    default='output/le.pickle',
    help="path to label encoder")
ap.add_argument(
    "-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

confidence_ = args["confidence"]
print("[INFO] загрузка детектора лица...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
print("[INFO] загрузка распознавателя лица...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())
print("[INFO] запуск видео потока...")

left_eye = USBCamVideoStream(src=0).start()
right_eye = USBCamVideoStream(src=1).start()  # для raspberry src=2
cv2.waitKey(1000)

run = True
'''
if not right_eye.stream.isOpened():
    print('[ERROR] не работает правая камера')
    run = False
if not left_eye.stream.isOpened():
    print('[ERROR] не работает левая камера')
    run = False
'''
width = 960
h, w = 480, 640
# h, w = left_eye.frame.shape[:2]
w, h = (width, int(h * width / float(w)))

while run:
    frames.clear()
    for streams in (left_eye, right_eye):
        if not streams.ret:
            break
        frame = streams.retrieves()
        frame = cv2.resize(frame, (w, h))  # interpolation=cv2.INTER_AREA
        frames.append(frame)

    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            if fW < 20 or fH < 20:
                continue
            faceBlob = cv2.dnn.blobFromImage(cv2.resize(
                face, (96, 96)), 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]
            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            # cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            # cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)

    fps.update()
    for (frameW, nameW) in zip(frames, ("Left Eye", "Right Eye")):
        cv2.imshow(nameW, frameW)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

    if name == 'vladimir' and proba > 0.8 and block:
        Thread(target=voice, name='voice').start()
        block = False

fps.stop()
print("[INFO] пройденное время: {:.2f}".format(fps.elapsed()))
print("[INFO] приблизительно FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
left_eye.stop()
right_eye.stop()
