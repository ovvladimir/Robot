import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
'from adafruit_servokit import ServoKit'
try:
    import logging
    logging.getLogger("tensorflow").setLevel(logging.CRITICAL)
finally:
    import tensorflow as tf
    import tflearn
    from tflearn.layers.conv import conv_2d, max_pool_2d
    from tflearn.layers.core import input_data, dropout, fully_connected
    from tflearn.layers.estimator import regression

tf.reset_default_graph()
convnet = input_data(shape=[None, 89, 100, 1], name='input')
convnet = conv_2d(convnet, 32, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 128, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 256, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 256, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 128, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = fully_connected(convnet, 1000, activation='relu')
convnet = dropout(convnet, 0.75)
convnet = fully_connected(convnet, 3, activation='softmax')
convnet = regression(
    convnet, optimizer='adam', learning_rate=0.001,
    loss='categorical_crossentropy', name='regression')

model = tflearn.DNN(convnet, tensorboard_verbose=0)
model.load("TrainedModel/GestureRecogModel.tfl")

className = "None"
bg = None
predictedClass, confidence = None, 0
num_frames = 0
top, right, bottom, left = 10, 350, 225, 590

vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
cv2.waitKey(1000)

'kit = ServoKit(channels=16)'
channel = 0
block = 0
'kit.servo[channel].angle = 0'

while True:
    '''if predictedClass == 1 and block == 0:
        kit.servo[channel].angle = 0
        block = 1
    elif predictedClass == 2 and block == 1:
        kit.servo[channel].angle = 120
        block = 0'''

    frame = vs.read()
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    roi = frame[top:bottom, right:left]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    if num_frames < 30:
        if bg is None:
            bg = gray.astype("float")

        cv2.accumulateWeighted(gray, bg, 0.5)
        num_frames += 1
    else:
        diff = cv2.absdiff(bg.astype("uint8"), gray)
        thresholded = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        (cnts, _) = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        predictedClass, confidence = None, 0
        if len(cnts) != 0:
            segmented = max(cnts, key=cv2.contourArea)

            cv2.drawContours(frame, [segmented + (right, top)], -1, (0, 100, 250))
            wsize = 100
            hsize = int(thresholded.shape[0] * (wsize / float(thresholded.shape[1])))
            thresholded_ = cv2.resize(thresholded, (wsize, hsize), interpolation=cv2.INTER_AREA)
            prediction = model.predict([thresholded_.reshape(89, 100, 1)])

            predictedClass, confidence = np.argmax(prediction), (np.amax(prediction) / (prediction[0][0] + prediction[0][1] + prediction[0][2]))
            # cv2.imshow("Thesholded", thresholded)

    if confidence < 0.9:
        className = "None"
    else:
        if predictedClass == 1:
            className = "Open hand"
        elif predictedClass == 2:
            className = "Closed hand"

    cv2.putText(
        frame, f"Pedicted Class : {className}",
        (30, 455), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(
        frame, f"Confidence : {round(confidence * 100, 2)} %",
        (30, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(
        frame, 'wait' if num_frames < 30 else 'start',
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
        (0, 0, 255) if num_frames < 30 else (0, 255, 0), 2)

    cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

    cv2.imshow("PiCamera", frame)
    if cv2.waitKey(100) == 27:
        break

vs.stop()
cv2.destroyAllWindows()
