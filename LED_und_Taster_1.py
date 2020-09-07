class LED:
    def __init__(self, iLEDPin):

        self.__iLEDPin = iLEDPin
        self.bLEDMode = False
        GPIO.setup(self.__iLEDPin, GPIO.OUT, initial=GPIO.LOW)

    """
    def LEDturnon(self):
        self.bLEDState = True
        self.__LEDoutput()

    def LEDturnoff(self):
        self.bLEDState = False
        self.__LEDoutput()

    def LEDcheckState(self):
        if self.bLEDState:
            return True
        else:
            return False
    """

    def LEDstay(self):
        if self.bLEDMode:
            self.__LEDoutput()
        else:
            self.__LEDoutput()

    def LEDswitch(self):
        if self.bLEDMode:
            self.bLEDMode = False
        else:
            self.bLEDMode = True
        self.__LEDoutput()

    def __LEDoutput(self):
        GPIO.output(self.__iLEDPin, self.bLEDMode)


class Pushbutton:
    def __init__(self, iPushbuttonPin):
        self.__iPushbuttonPin = iPushbuttonPin
        GPIO.setup(self.__iPushbuttonPin, GPIO.IN)

    def pushbuttonPushed(self):
        return GPIO.input(self.__iPushbuttonPin)

class Database:
    def __init__(self):
        pass


def main(iLEDPin, iPushbuttonPin):
    try:
        oLED = LED(iLEDPin)
        oButton = Pushbutton(iPushbuttonPin)

        """
        sTimestamp = str(time.ctime())
        while True:
            if oButton.pushbuttonPushed() == True:
                if oLED.LEDcheckState() == True:
                    oLED.LEDturnoff()
                    print("LED turned off\t |", sTimestamp)
                    time.sleep(0.2)
                elif oLED.LEDcheckState() == False:
                    oLED.LEDturnon()
                    print("LED turned on\t |", sTimestamp)
                    time.sleep(0.2)
            time.sleep(0.1)
        """

        """
        iCounter = 0
        while True:
            if oButton.pushbuttonPushed() == True and oLED.LEDcheckState() == False and iCounter % 2 == 0:
                oLED.LEDturnon()
                iCounter += 1
                print("LED on\t", iCounter)
            elif oButton.pushbuttonPushed() == True and oLED.LEDcheckState() == True and not iCounter % 2 == 0:
                oLED.LEDturnoff()
                iCounter += 1
                print("LED off\t", iCounter)
            time.sleep(0.1)
        """

        iPresstime= 0
        while True:
            while oButton.pushbuttonPushed():
                iPresstime += 1
                print(iPresstime)

            if 1 <= iPresstime <= 5000:
                oLED.LEDswitch()
                iPresstime = 0

            elif iPresstime >= 5000:
                oLED.LEDstay()
                iPresstime = 0

            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    import RPi.GPIO as GPIO
    import time
    import sqlite3

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    main(iLEDPin=23, iPushbuttonPin=24)
