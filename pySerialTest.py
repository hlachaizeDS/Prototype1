import serial
import time
import struct

ser = serial.Serial('COM12',baudrate=57600)

ser.write(b'dV0\r\n')
'''
ser.write(b'\x01\x0e\x02\x02\x00\x00\x00\x01\x14')

time.sleep(2)

ser.write(b'\x01\x0e\x02\x02\x00\x00\x00\x00\x13')
'''


ser.close()





#ser = serial.Serial('COM2', 19200)

#CapA nach Col1 in waste

#for i in range(20):
#	ser.write(b'\x42\x56\x20\x20\x32\x33\x20\x20\x31\x34\x20\x20\x34\x37\x20\x76\x20\x20\x65')
#	time.sleep(0.05)
#	ser.write(b'\x42\x56\x41\x65')
#
#	ser.write(b'\x42\x56\x20\x20\x39\x20\x20\x31\x34\x20\x20\x34\x37\x20\x76\x20\x20\x65')
#	time.sleep(0.05)
#	ser.write(b'\x42\x56\x41\x65')

#ser.close()