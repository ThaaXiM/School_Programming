
class MCP23S17:
    def __init__(self, slave_address, busnumber, chipnumber):
        assert busnumber in [0, 1]  # It will be checked, if the busnumber is 0 or 1 (We are using 0)
        assert chipnumber in [0, 1] # It will be checked, if the chipnumber is 0 or 1 (We are using 0)
        self.controlbyte_write = slave_address<<1 # Sets the write-byte (last byte is 0 -> write mode)
        self.controlbyte_read = (slave_address<<1)+1 # Sets the read-byte (last byte is 1 -> read mode)
        self.spi = spidev.SpiDev() # Instantiate SpiDev for usage of spi-interface
        self.spi.open(busnumber, chipnumber) # Opens the busnumber and chipnumber out of the spi connection
        self.spi.max_speed_hz = 10000000 # Sets the max. hz
        # configure default registers
        # conf = configures if GPA(A) or GPB(B) gets selected
        # input = sets GPA(A) or GPB(B) as an input
        # output = sets GPA(A) or GPB(B) as an output
        self._regs = {'conf': {'A': 0x00, 'B': 0x01},   # 0x00 = 0  | 0x01 = 1
                      'input': {'A': 0x12, 'B': 0x13},  # 0x12 = 18 | 0x13 = 19
                      'output': {'A': 0x14, 'B': 0x15}} # 0x14 = 20 | 0x15 = 21


    def write_config(self, portab, value):
        '''
        It will be defined if port A or B (or both) is set as a input- or output pin. (I/O direction register)
        The value will stay same until the last line (30), there it will be overwritten.
        :param portab: Portarea A or B
        :param value: Value
        :return: /
        '''
        assert portab in ['A', 'B']
        reg = self._regs['conf'][portab]
        self.spi.xfer([self.controlbyte_write, reg, value])

    def read_config(self, portab):
        '''
        Basically returns how the config of port A or B is set (Input or Output)
        :param portab: Portarea A or B
        :return: Returns a list of which only the second value is beeing used.
                 The controllbyte is beeing used for the read.
        '''
        assert portab in ['A', 'B']
        reg = self._regs['conf'][portab]
        return self.spi.xfer([self.controlbyte_read, reg, 0])[2]

    def write_output(self, portab, value):
        '''
        It will be defined if a pin in port A or B (or both) is set as a output-pin.
        The old value will be immediately overwritten.
        :param portab: Portarea A or B
        :param value: Value
        :return: /
        '''
        assert portab in ['A', 'B']
        reg = self._regs['output'][portab]
        self.spi.xfer([self.controlbyte_write, reg, value])

    def read_output(self, portab):
        '''
        A byte will be returned for each pin in portarea A or B, which is set as a output pin.
        :param portab: Portarea A or B
        :return: Returns a list of which only the second valuce is beeing used.
                 The controllbyte is beeing used for the read.
        '''
        assert portab in ['A', 'B']
        reg = self._regs['output'][portab]
        return self.spi.xfer([self.controlbyte_read, reg, 0])[2]

    def read_input(self, portab):
        '''
        A byte will be returned for each pin in portarea A or B, which is set as a input pin.
        :param portab: Portarea A or B
        :return: Returns a list of which only the second valuce is beeing used.
                 The controllbyte is beeing used for the read.
        '''
        assert portab in ['A', 'B']
        reg = self._regs['input'][portab]
        return self.spi.xfer([self.controlbyte_read, reg, 0])[2]

    def set_output_pin(self, portab, pin, value):
        assert portab in ['A', 'B']     # A oder B muss als "portab"-Wert eingegeben werden
        assert 0 <= pin <= 8            # "pin" muss größer oder gleich 0- und kleiner als 8 sein
        assert value in [0, 1]          # "value" muss entweder 0 oder 1 sein
        data = self.read_output(portab) # "read_output" wird als variable "data" gespeichert
        if value == 0:                  # wenn "value" == "0" ist:
            data &= ~(1 << pin)         # 1 wird um die Anzahl von "pin" nach links geswifted und negiert (~),
                                        # anschließend mit "data" verundet
        else:                           # ansonsten:
            data |= (1 << pin)          # 1 wird um die Anzahl von "pin" nach links geswifted und anschließend mit
                                        # data verodert.

        self.write_output(portab, data) # ein bestimmer pin wird als output festgelegt

    def get_output_pin(self, portab, pin):
        assert portab in ['A', 'B']      # A oder B muss als "portab"-Wert eingegeben werden
        assert 0 <= pin <= 8             # "pin" muss größer oder gleich 0- und kleiner als 8 sein
        data = self.read_output(portab)  # "read_output" wird in der variable "data" gespeichert
        value = (data & (1 << pin)) != 0 # 1 wird um die Anzahl von pin nach links geswiftet und mit data verundet und
                                         # muss ungleich 0 sein.
        return value                     # gibt den boolishen Wert "value" zurück (Hoffentlich 0)

    def get_input_pin(self, portab, pin):
        #                   # B     # 7 (Taster)
        assert portab in ['A', 'B']      # "portab" muss entweder A oder B sein
        assert 0 <= pin <= 8             # "pin" muss größer oder gleich 0- und kleiner als 8 sein
        data = self.read_input(portab)   # "read_input" wird in der variable "data" festgehalten
        value = (data & (1 << pin)) != 0 # 1 wird um die Anzahl von pin nach links geswiftet und mit data verundet.
                                         # Value hält dann den boolischen Wert (True oder False) fest, der wert aus den
                                         # Klammern ungleich 0 ist.
        return value                     # gibt den boolischen Wert "value" zurück (Hoffentlich 1)


class Buttongame:
    def __init__(self):
        self.__oMCP = MCP23S17(0b0100000, 0, 0)
        self.__oMCP.write_config("A", 0b0100000)


    def __buttonStatus(self):
        return self.__oMCP.get_input_pin("B", 7)

    def setAllLEDoff(self):
        self.__oMCP.write_output("A", 0b00000000)

    def mainloop(self):
        while True:
            while not self.__buttonStatus():
                self.__oMCP.set_output_pin("A", 0, True)
                self.__oMCP.set_output_pin("A", 1, False)

            while self.__buttonStatus():
                self.__oMCP.set_output_pin("A", 0, False)
                self.__oMCP.set_output_pin("A", 1, True)

            time.sleep(0.1)


class Database:
    def __init__(self):
        self.__cConnection = sqlite3.connect(os.path.join(os.path.dirname(__file__), "Fischer_DB.sqlite3"))
        self.cCursor = self.__cConnection.cursor()


    def createTable(self):
        self.cCursor.execute("CREATE TABLE IF NOT EXISTS tblHighscore"
                             "(hsID INTEGER PRIMARY KEY,"
                             "Playername VARCHAR(255) NOT NULL,"
                             "Score INTEGER)")
        self.__cConnection.commit()

    def saveState(self, sPlayername, iGameLevel):
        self.cCursor.execute("""
        INSERT INTO tblHighscore (Playername, Score) 
        VALUES('%s', %d);"""
                             % (sPlayername, iGameLevel))
        self.__cConnection.commit()

    def closeConnection(self):
        self.__cConnection.close()


class Laddergame:
    def __init__(self, pinButton, portabButton, portabLEDs):
        self.iPinButton = pinButton
        self.sPortButton = portabButton
        self.sPortLED = portabLEDs

        self.__oDB = Database()
        self.__oMCP = MCP23S17(0b0100000, 0, 0)
        self.__oMCP.write_config(self.sPortLED, 0b0000000)
        self.iGameLevel = 0
        self.bWon = False

        self.__fLEDlastBlink = time.time()
        self.fLEDblinkInterval = random.randint(5, 8)/10
        # self.fLEDblinkInterval = 1
        self.__bLEDStatus = False


    def setAllLEDoff(self):
        self.__oMCP.write_output(self.sPortLED, 0b00000000)

    def blinkLED(self, iLEDPin):
        fNow = time.time()
        if fNow - self.__fLEDlastBlink > self.fLEDblinkInterval:
            self.__bLEDStatus = not self.__bLEDStatus
            self.__fLEDlastBlink = fNow
            self.__oMCP.set_output_pin(self.sPortLED, iLEDPin, self.__bLEDStatus)

    def levelUp(self):
        if self.iGameLevel is not 7:
            self.__oMCP.set_output_pin(self.sPortLED, self.iGameLevel, True)
            self.fLEDblinkInterval -= 0.07
            self.iGameLevel += 1
        else:
            self.bWon = True

    def gameReset(self):
        self.iGameLevel = 0
        self.bWon = False
        self.fLEDblinkInterval = random.randint(5, 8)/10
        # self.fLEDblinkInterval = 1
        for iLEDPin in range(0, 8):
            self.__oMCP.set_output_pin(self.sPortLED, iLEDPin, False)
        self.mainloop()

    def gameOver(self):
        iBlinkCounter = 4
        iBlinkDelay = 0.3
        while iBlinkCounter:
            iBlinkCounter -= 1
            for iLEDPin in range(0, 8):
                self.__oMCP.set_output_pin(self.sPortLED, iLEDPin, False)
            time.sleep(iBlinkDelay)
            for iLEDPin in range(0, 8):
                self.__oMCP.set_output_pin(self.sPortLED, iLEDPin, True)
            time.sleep(iBlinkDelay)

        sUserinput = input("HAHA! You lost!\nWanna try again?\nyes = again\neverything else = no\n ").lower()
        if sUserinput == "yes":
            for iLEDPin in range(0,8):
                self.__oMCP.set_output_pin(self.sPortLED, 8-iLEDPin, False)
                time.sleep(0.1)
            self.gameReset()
        else:
            self.setAllLEDoff()
            self.__oDB.closeConnection()
            sys.exit(0)

    def gameWin(self):
        print("You won!")
        bRunner = True
        fNow = time.time()
        while bRunner == True:
            self.__oMCP.set_output_pin(self.sPortLED, random.randint(0, 8), True)
            self.__oMCP.set_output_pin(self.sPortLED, random.randint(0, 8), False)
            time.sleep(0.1)
            if time.time() >= fNow+random.randint(3, 6):
                self.setAllLEDoff()
                break

        sUserinput = input("Wanna continue?\nyes = continue\neverything else = no\n ").lower()
        if sUserinput == "yes":
            self.gameReset()
        else:
            self.setAllLEDoff()
            self.__oDB.closeConnection()
            sys.exit(0)

    def mainloop(self):
        sUserinput = str(input("Please enter your Username: "))
        if len(sUserinput) >= 1:
            print("Game will start in some seconds, get ready!")
            self.__oDB.createTable()
            time.sleep(random.randint(3, 6))

            while not self.bWon:
                bButtonState = self.__oMCP.get_input_pin(self.sPortButton, self.iPinButton)
                if bButtonState:
                    if self.__bLEDStatus:
                        self.levelUp()
                        time.sleep(0.2)
                    else:
                        self.__oDB.saveState(sPlayername=sUserinput, iGameLevel=self.iGameLevel)
                        self.__oDB.closeConnection()
                        self.gameOver()
                self.blinkLED(self.iGameLevel)
            self.gameWin()
        else:
            print("Du dulli")
            self.setAllLEDoff()
            self.__oDB.closeConnection()
            sys.exit(0)


# region Hilfe
# 1 byte = 8 bits
# 0bXXXXXXXX
#          | <- Letzer bit ist der 1. Pin
#          0 = output
#          1 = input

# Taster = 128
# endregion Hilfe

if __name__ == "__main__":

    # region Imports
    import spidev
    import time
    import random
    import sys
    import sqlite3
    import os
    # endregion Imports

    # region Buttongame
    oBG = Buttongame()
    try:
        oBG.mainloop()
    except KeyboardInterrupt:
        oBG.setAllLEDoff()
    # endregion Buttongame

    # region Laddergame
    # oLG = Laddergame(pinButton=7, portabButton="B", portabLEDs="A")
    # oDB = Database()
    # try:
    #     oLG.mainloop()
    # except KeyboardInterrupt:
    #     oDB.closeConnection()
    #     oLG.setAllLEDoff()
    # endregion Laddergame

    # region test
    '''    
    oMCP = MCP23S17(0b0100000, 0, 0)
    x = True
    while x == True:
        try:
            # print(oMCP.get_input_pin("B", 7))
            oMCP.write_config("A", 0b00000000)

            for led in range(0,8):
                oMCP.set_output_pin("A", led, True)
                print(oMCP.get_output_pin("A", led))
                time.sleep(1)

            if oMCP.get_output_pin("A", 7) == True:
                x = False
                oMCP.write_output("A", 0b00000000)

        except KeyboardInterrupt:
            oMCP.write_output("A", 0b00000000)
            x = False
            
    '''
    # endregion test

