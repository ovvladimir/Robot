import threading
import queue
import time
import logging
logger = logging.getLogger(__name__)


class Send():
    """base class for a sender"""

    def __init__(self, name, sQueue):
        self.name = name
        self.sQueue = sQueue

        self.thread = threading.Thread(target=self.run, name=name)
        self.thread.start()

    def run(self):
        """ no runner so far """
        pass


class Receive():
    """base class for a receiver"""

    def __init__(self, name, rQueue):
        self.name = name
        self.rQueue = rQueue

        self.thread = threading.Thread(target=self.run, name=name)
        self.thread.start()

    def run(self):
        """ no runner so far """
        while True:
            try:
                s = self.rQueue.get(block=True, timeout=0.1)
            except queue.Empty:
                continue
            self.processMessage(s)

    def processMessage(self, s):
        pass


class TestSend(Send):
    def __init__(self, name, sQueue):
        Send.__init__(self, name, sQueue)

    def run(self):
        while True:
            """simulate some event"""
            time.sleep(1)
            logger.info(
                "{name:s}: push event 'sendEvent'".format(
                    name=self.name))
            self.sQueue.put('event')


class PushbuttonSimulateSend(Send):
    def __init__(self, name, sQueue):
        Send.__init__(self, name, sQueue)

    def run(self):
        while True:
            """simulate some event"""
            time.sleep(30)
            logger.info(
                "{name:s}: push event 'emergency'".format(
                    name=self.name))
            self.sQueue.put('emergency')

            time.sleep(30)
            logger.info("{name:s}: push event 'normal'".format(name=self.name))
            self.sQueue.put('normal')


class MotorReceive(Receive):
    def __init__(self, name, rQueue):
        Receive.__init__(self, name, rQueue)

    def processMessage(self, s):
        if 'on' == s:
            logger.info("{name:s}: Motor on".format(name=self.name))
        elif 'off' == s:
            logger.info("{name:s}: Motor off".format(name=self.name))
        else:
            logger.error(
                "{name:s}: Unknown message '{msg:s}'".format(
                    name=self.name, msg=s))


class Controller():
    def __init__(self, name, inQueue, motor_front_left):
        self.name = name
        self.inQueue = inQueue
        self.motor_front_left = motor_front_left
        # controller has state
        self.state = 'stateStart'

        self.thread = threading.Thread(target=self.run, name=name)
        self.thread.start()

    def run(self):
        countFailedStartAttempts = 0
        while True:
            try:
                s = self.inQueue.get(block=True, timeout=0.1)
            except queue.Empty:
                continue

            if self.state == 'stateStart':
                if s == 'emergency':
                    self.motor_front_left.put("off")
                    self.state = 'stateEmergency'
                elif s == 'event':
                    self.motor_front_left.put("on")
                    self.state = 'stateStarted'

            elif self.state == 'stateStarted':
                if s == 'emergency':
                    self.motor_front_left.put("off")
                    self.state = 'stateEmergency'
                elif s == 'event':
                    countFailedStartAttempts += 1
                    if countFailedStartAttempts > 10:
                        countFailedStartAttempts = 0
                        logger.error(
                            "{name:s}: Motor already started, event ignored".format(
                                name=self.name))

            elif self.state == 'stateEmergency':
                if s == 'emergency':
                    self.motor_front_left.put("off")

                elif s == 'normal':
                    self.state = 'stateStart'


logging.basicConfig(level=logging.DEBUG)
logger.info("Start")

sQueue = queue.Queue()
testSend = TestSend("simulate_send", sQueue)
emergency = PushbuttonSimulateSend("emergencyButton", sQueue)

rQueue = queue.Queue()
motor = MotorReceive("front_left", rQueue)


logger.info("Some test ---")
rQueue.put("off")
rQueue.put("unqrqrqrq")

controller = Controller('controller', sQueue, rQueue)

while True:
    time.sleep(0.1)
