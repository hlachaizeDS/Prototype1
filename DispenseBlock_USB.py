from serial import rs485
import COM_port
from DispenseUnit_1161 import *

class DispenseBlock_USB:
    '''
    Represents a collective of pumps connected via USB
    '''

    def __init__(self,parent):

        self.parent = parent
        #self.serial_port = Serial("COM6", 115200)
        #self.bus = pyTMCL.connect(self.serial_port)

        self.dus=[]
        comport_dictionnaries = COM_port.list_1161_coms_by_adress()

        for adress in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            bus = pyTMCL.connect(Serial(comport_dictionnaries[adress], 115200, timeout=5))

            if adress in [9, 10]:
                self.dus.append(DispenseUnit_1161(self, bus, 1, 0, pump_type="idex 5000"))
            else:
                self.dus.append(DispenseUnit_1161(self, bus, 1, 0))

    def multi_dispense(self,volumes):
        #if list of volumes not at the same length as dus, we add 0s
        #start=time.time()
        volumes=volumes + [0]*(len(self.dus)-len(volumes))

        for index in range(len(self.dus)):
            if volumes[index]!=0:
                self.dus[index].dispense(volumes[index])

        for index in range(len(self.dus)):
            if volumes[index] != 0:
                self.dus[index].wait_for_canmove()

        #time.sleep(0.2)

    def wait_for_move(self):

        # Status is
        # 0 for idle
        # 1 for busy
        # 2 for can_move

        pumps_nb=len(self.dus)
        is_ok_to_move=[0]*pumps_nb

        #time.sleep(0.01) #in case we just sent the command to move

        while any(is_ok_to_move)==0:
            for index in range(pumps_nb):
                if is_ok_to_move[index]==0:
                    pump_status=self.dus[index].get_status()
                    if pump_status==0 or pump_status==2:
                        is_ok_to_move[index]=1
            time.sleep(0.005)

    def wait_for_idle(self):

        #self.serial_port.flushInput()
        pumps_nb=len(self.dus)
        is_idle=[0]*pumps_nb

        #time.sleep(0.01) #in case we just sent the command to move

        while any(is_idle)==0:
            for index in range(pumps_nb):
                if is_idle[index]==0:
                    pump_status=self.dus[index].get_status()
                    if pump_status==0:
                        is_idle[index]=1
            time.sleep(0.005)

    def init(self):

        self.wait_for_idle()

        for index in range(len(self.dus)):
            self.dus[index].init()

        #self.wait_for_move()

if __name__ == "__main__":

    disp_block = DispenseBlock_USB("FP")
    #disp_block.dus[6].dispense(0)
    #disp_block.dus[1].init()
    start=time.time()
    for i in range(int(10000 / 25)):
        print((i + 1) * 25)
        #disp_block.multi_dispense([0,0,25,0,0,0,0])
        disp_block.multi_dispense([25, 0, 0, 0, 0, 25, 0,25])
    end=time.time()
    print(start-end)
    #disp_block.init()
    #disp_block.multi_dispense([200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200])