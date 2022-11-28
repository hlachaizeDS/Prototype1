import serial
from time import sleep

class DispenseUnit_Arduino():

    def __init__(self, parent,COMPORT,*args, **kwargs):
        self.parent = parent
        self.ser = serial.Serial(COMPORT, 9600)


    def wait_for_idle(self):
        self.ser.flushInput()
        self.ser.write(b'R;')
        while(1):
            r=self.ser.readline()
            #print(r)
            if (b'ready\r\n'):
                break

    def wait_for_canMove(self):
        r=self.ser.readline() #when it can move, pumps will send canMove
        #print(r)


    def dispense(self,volume):
        self.wait_for_idle()
        command="U"+str(volume)+";"
        self.ser.write(bytes(command,'utf-8'))

    def init(self):
        self.wait_for_idle()
        self.ser.write(b'I;')

