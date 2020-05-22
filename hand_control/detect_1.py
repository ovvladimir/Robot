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


class Detection(object):
    def __init__(self):
        self.bg = None

        # Model defined
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
        convnet = regression(convnet, optimizer='adam', learning_rate=0.001,
                             loss='categorical_crossentropy', name='regression')

        self.model = tflearn.DNN(convnet, tensorboard_verbose=0)
        # Load Saved Model
        self.model.load("TrainedModel/GestureRecogModel.tfl")

        # initialize num of frames
        self.num_frames = 0
        self.predictedClass = None
        self.confidence = 0
        # initialize weight for running average
        self.aWeight = 0.5
        # region of interest (ROI) coordinates
        self.top, self.right, self.bottom, self.left = 10, 350, 225, 590

        # start camera
        self.vs = VideoStream(src=0).start()
        # self.vs = VideoStream(usePiCamera=True).start()

        # control servo
        # Set channels to the number of servo channels on your kit.
        # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
        'kit = ServoKit(channels=16)'
        channel = 0
        block = 0

        self.run = True
        while self.run:
            frame = self.vs.read()
            result = self.main_(frame.copy())
            '''if result == 1 and block == 0:
                kit.servo[channel].angle = 180
                block = 1
            elif result == 2 and block == 1:
                kit.servo[channel].angle = 0
                block = 0'''

    def run_avg(self, image):
        # initialize the background
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(image, self.bg, self.aWeight)

    def segment(self, image, threshold=25):
        # find the absolute difference between background and current frame
        diff = cv2.absdiff(self.bg.astype("uint8"), image)

        # threshold the diff image so that we get the foreground
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

        # get the contours in the thresholded image
        (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # return None, if no contours detected
        if len(cnts) == 0:
            return
        else:
            # based on contour area, get the maximum contour which is the hand
            segmented = max(cnts, key=cv2.contourArea)
            return (thresholded, segmented)

    def main_(self, img):
        # resize the frame
        frame1 = imutils.resize(img, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame1, 1)

        # clone the frame
        self.clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[self.top:self.bottom, self.right:self.left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if self.num_frames < 30:
            self.run_avg(gray)
            cv2.waitKey(100)
            self.num_frames += 1
        else:
            # segment the hand region
            hand = self.segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand
                # draw the segmented region and display the frame
                cv2.drawContours(self.clone, [segmented + (self.right, self.top)], -1, (0, 0, 255))
                wsize = 100
                hsize = int(thresholded.shape[0] * (wsize / float(thresholded.shape[1])))
                thresholded_ = cv2.resize(thresholded, (wsize, hsize), interpolation=cv2.INTER_AREA)
                prediction = self.model.predict([thresholded_.reshape(89, 100, 1)])

                self.predictedClass = None
                self.predictedClass, self.confidence = np.argmax(prediction), (np.amax(prediction) / (prediction[0][0] + prediction[0][1] + prediction[0][2]))
                # cv2.imshow("Thesholded", thresholded)

        # draw text
        self.showStatistics()
        # draw the segmented hand
        cv2.rectangle(self.clone, (self.left, self.top), (self.right, self.bottom), (255, 0, 0), 2)

        # display the frame with segmented hand
        cv2.imshow("PiCamera", self.clone)
        if cv2.waitKey(1) == 27:
            self.run = False
            self.vs.stop()
            cv2.destroyAllWindows()

        return self.predictedClass

    def showStatistics(self):
        # textImage = np.zeros((300, 512, 3), np.uint8)
        className = "None"

        if self.predictedClass == 1 and self.confidence > 0.9:
            className = "Palm"
        elif self.predictedClass == 2 and self.confidence > 0.9:
            className = "Fist"
        else:
            className = "None"

        cv2.putText(
            self.clone, f"Pedicted Class : {className}",
            (30, 455), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(
            self.clone, f"Confidence : {round(self.confidence * 100, 2)} %",
            (30, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(
            self.clone, 'wait' if self.num_frames < 30 else 'start',
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255) if self.num_frames < 30 else (0, 255, 0), 2)
        # cv2.imshow("Statistics", textImage)


detection = Detection()
