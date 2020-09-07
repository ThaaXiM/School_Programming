class LED:
    def __init__(self, iLEDPin):
        self.__iLEDPin = iLEDPin
        self.bLEDMode = False
        GPIO.setup(self.__iLEDPin, GPIO.OUT, initial=GPIO.LOW)

    def LEDswitch(self):
        if self.bLEDMode:
            self.bLEDMode = False
        else:
            self.bLEDMode = True
        self.LEDoutput()

    def LEDoutput(self):
        GPIO.output(self.__iLEDPin, self.bLEDMode)


class Pushbutton:
    def __init__(self, iPushbuttonPin):
        self.__iPushbuttonPin = iPushbuttonPin
        GPIO.setup(self.__iPushbuttonPin, GPIO.IN)

    def pushbuttonPushed(self):
        return GPIO.input(self.__iPushbuttonPin)


class Database:
    def __init__(self):
        self.__cConnection = sqlite3.connect(os.path.join(os.path.dirname(__file__), "Fischer_DB.sqlite3"))
        self.cCursor = self.__cConnection.cursor()

    def createTable(self):
        self.cCursor.execute("CREATE TABLE IF NOT EXISTS tblLEDData"
                            "(ldID INTEGER PRIMARY KEY,"
                            "Zeitstempel CHAR(50) NOT NULL,"
                            "LEDStatus INTEGER NOT NULL)")
        self.__cConnection.commit()


    def saveState(self, iTimestamp, iLEDState):
        self.cCursor.execute("""INSERT INTO tblLEDData (Zeitstempel, LEDStatus) VALUES (?,?);""",
                            (iTimestamp, iLEDState))

    def closeConnection(self):
        self.__cConnection.close()


def main(iLEDPin, iPushbuttonPin):
    oLED = LED(iLEDPin)
    oButton = Pushbutton(iPushbuttonPin)
    oDB = Database()
    try:
        oDB.createTable()
        iPresstime= 0
        while True:
            while oButton.pushbuttonPushed():
                iPresstime += 1
                print(iPresstime)

            if 1 <= iPresstime <= 5000:
                oLED.LEDswitch()
                oDB.saveState(iTimestamp=time.ctime(), iLEDState=oLED.LEDoutput())
                print("Saved into DB: ", time.ctime(), oLED.LEDoutput())
                iPresstime = 0

            elif iPresstime >= 5000:
                oLED.LEDoutput()
                iPresstime = 0

            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        oDB.closeConnection()


if __name__ == "__main__":
    import RPi.GPIO as GPIO
    import time
    import sqlite3
    import os

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    main(iLEDPin=23, iPushbuttonPin=24)
