from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import pyttsx3
from threading import Thread

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru')
for voice in voices:
    if voice.name == 'Aleksandr':
        tts.setProperty('voice', voice.id)
tts.say('О-о! Привет Владимир!')
block = 0
name = None


def voice():
    print('О-о! Привет, Владимир!')
    tts.runAndWait()


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

print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())
print("[INFO] starting video stream...")

left_eye = VideoStream(src=0).start()
right_eye = VideoStream(src=1).start()  # для raspberry src=2
cv2.waitKey(1000)
fps = FPS().start()
frames = []

while True:
    frames.clear()
    for streams in (left_eye, right_eye):
        if streams.stream.grab():
            frame = streams.stream.retrieve()[1]
            frame = imutils.resize(frame, width=960)
            frames.append(frame)
        else:
            print("No frames")
            break

    (h, w) = frame.shape[:2]

    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            if fW < 20 or fH < 20:
                continue
            faceBlob = cv2.dnn.blobFromImage(
                cv2.resize(face, (96, 96)), 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]
            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)

    fps.update()
    for (frameW, nameW) in zip(frames, ("Left Eye", "Right Eye")):
        cv2.imshow(nameW, frameW)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

    if name == 'vladimir' and proba > 0.8 and block == 0:
        Thread(target=voice).start()
        block = 1

fps.stop()
print("[INFO] пройденное время: {:.2f}".format(fps.elapsed()))
print("[INFO] приблизительно FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
left_eye.stop()
right_eye.stop()
