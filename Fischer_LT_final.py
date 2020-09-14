class LED:
    """
    Just an ED-Class
    """
    def __init__(self, iLEDPin):
        """
        Constructor for LED
        :param iLEDPin: INTEGER
        :param bLEDMode: bool
        """
        self.__iLEDPin = iLEDPin
        self.bLEDMode = False
        GPIO.setup(self.__iLEDPin, GPIO.OUT, initial=GPIO.LOW)

    def LEDswitch(self):
        """
        A function where the LED switchs the state (False = GPIO.LOW,
                                                    True = GPIO.High)
        So if it is True, switch it to False.
        If it is not True, switch it to True.

        In the end configurate the output with the boolish value which got set.
        :return: void
        """
        if self.bLEDMode:
            self.bLEDMode = False
        else:
            self.bLEDMode = True
        self.LEDoutput()

    def LEDoutput(self):
        """
        Configuration of the LED-Output
        __iLEDPin = Pin number of LED
        bLEDMode = True or False (-> HIGH / LOW)
        :return: void
        """
        GPIO.output(self.__iLEDPin, self.bLEDMode)


class Pushbutton:
    """
    Just an Class for a Button
    """
    def __init__(self, iPushbuttonPin):
        """
        Constructor for Button
        :param iPushbuttonPin: INTEGER
        """
        self.__iPushbuttonPin = iPushbuttonPin
        GPIO.setup(self.__iPushbuttonPin, GPIO.IN)

    def pushbuttonPushed(self):
        """
        Function which just returns a True or False if the button is pushed or not.
                                                                  (gets power)
        :return: bool
        """
        return GPIO.input(self.__iPushbuttonPin)


class Database:
    """
    Class for a sqlite3 Database
    """
    def __init__(self):
        """
        Constructor for the Database
        :param cConnection = connect
        :param cCursor = cursor
        """
        self.__cConnection = sqlite3.connect(os.path.join(os.path.dirname(__file__), "Fischer_DB.sqlite3"))
        self.cCursor = self.__cConnection.cursor()

    def createTable(self):
        """
        This function just generates a table, but only when there isnt already a table.
        In the end it gets commmited.
        :return: void
        """
        self.cCursor.execute("CREATE TABLE IF NOT EXISTS tblLEDData"
                            "(ldID INTEGER PRIMARY KEY,"
                            "Zeitstempel CHAR(50) NOT NULL,"
                            "LEDStatus INTEGER NOT NULL)")
        self.__cConnection.commit()


    def saveState(self, cTimestamp, iLEDState):
        """
        Saves the timestamp and the state of the current LEDmode into the database
        :param cTimestamp: CHAR
        :param iLEDState: INT
        :return:
        """
        self.cCursor.execute("""INSERT INTO tblLEDData (Zeitstempel, LEDStatus) VALUES (?,?);""",
                            (cTimestamp, iLEDState))
        self.__cConnection.commit()

    def closeConnection(self):
        """
        closes safely the connection to the database
        :return: void
        """
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
                oDB.saveState(cTimestamp=time.ctime(), iLEDState=int(oLED.bLEDMode))
                print("Safed: ", time.ctime(), oLED.bLEDMode)
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
