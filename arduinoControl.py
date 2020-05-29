import time
import serial
import usbErrorHandling
from serial import *
from time import sleep

COMPORT='COM6'

class ArduinoControl():
    def __init__(self, parent,*args, **kwargs):
        self.parent = parent

    def startHeating(self):
        self.ser = serial.Serial(COMPORT, 115200)
        self.ser.write(b'1500\r\n')
        self.ser.close()

    def stopHeating(self):
        self.ser = serial.Serial(COMPORT, 115200)
        self.ser.write(b'2000\r\n')
        self.ser.close()

    def startShaking(self,velocity): # Velocity between 38 and 1300rpm
        # while True:
        #     try:
                self.ser = serial.Serial(COMPORT, 115200)
                command=str(velocity)+'\r\n'
                self.ser.write(bytes(command,'utf-8'))
                self.ser.close()
            #     break
            # except SerialException:
            #     usbErrorHandling.restartArduinoUSB()
            #     sleep(10)





    def stopShaking(self):
        self.ser = serial.Serial(COMPORT, 115200)
        self.ser.write(b'1\r\n')
        self.ser.read()
        self.ser.close()

if __name__ == "__main__":
    # On crée la racine de notre interface
    parent='fake parent'
    arduinoControl=ArduinoControl(parent)
    arduinoControl.startHeating()
    arduinoControl.startShaking(900)
    time.sleep(4)
    arduinoControl.stopShaking()
