import spidev

class SPITEST:
    def __init__(self, busnumber):
        assert busnumber in [0, 1]
        self.spi = spidev.SpiDev()
        self.spi.open(busnumber, 0)
        self.spi.max_speed_hz=10000000

    def test(self, value):
        print("Sende :", value)
        output = self.spi.xfer([value])[0]
        print("Empfange :", output)
        if value == output:
            print("Test erfolgreich")
        else:
            print("Gegenteil von Test erfolgreich")

if __name__ == "__main__":
    t = SPITEST(0)
    t.test(100)
