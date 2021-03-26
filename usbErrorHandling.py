import time
import ctypes, sys

import os
import subprocess

devcon_Path='C:\\Program Files (x86)\\Windows Kits\\10\\Tools\\x64\\devcon'


def restartArduinoUSB():
    print('Restart arduino')
    subprocess.run([devcon_Path, 'disable', 'USB\VID_2341&PID_8037'])
    time.sleep(1)
    subprocess.run([devcon_Path, 'enable', 'USB\VID_2341&PID_8037'])
    time.sleep(2)

if __name__ == "__main__":

    result = subprocess.call(['C:\\Program Files (x86)\\Windows Kits\\10\\Tools\\x64\\devcon', 'hwids', '=usb'])
    subprocess.run([devcon_Path, 'disable', 'USB\VID_2341&PID_8037'])
    time.sleep(1)
    subprocess.run([devcon_Path, 'enable', 'USB\VID_2341&PID_8037'])