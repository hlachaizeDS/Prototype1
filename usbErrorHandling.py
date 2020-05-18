
import ctypes, sys

import os
import subprocess

def restartUSBHub():

    print('Restart USB Hub and ports')
    subprocess.call([r'C:\\Users\\Julien\\Desktop\\Prototype\\DevManView\\devmanview-x64\\disable_enable_TRINAMICS.bat'])

def restartArduinoUSB():
    print('Restart arduino')
    subprocess.call(
        [r'C:\\Users\\Prototype\\Desktop\\Prototype\\devmanview-x64\\disable_enable_Arduino.bat'])

if __name__ == "__main__":

    restartUSBHub()