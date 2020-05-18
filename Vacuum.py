import serial
from time import sleep


class Vacuum:

    def __init__(self, parent,ser, *args, **kwargs):

        self.parent=parent
        self.ser = ser

    def start(self):
        self.ser.write(b'dB\r\n')

    def stop(self):
        self.ser.write(b'dE\r\n')
        sleep(0.5) #We wait a bit so that vacuum can dissipate

    def ventOn(self):
        self.ser.write(b'dV1\r\n')

    def ventOff(self):
        self.ser.write(b'dV0\r\n')
