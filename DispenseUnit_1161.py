import pyTMCL
import math
import time
from serial import *



class DispenseUnit_1161:
    '''
    To use for pumps with TMCM-1161 card
    '''

    def __init__(self,parent,bus,address,motor_id=0,pump_type="regular"):

        self.parent=parent

        self.bus=bus
        self.address=address
        self.motor_id = motor_id # with TMCM-1161, will always be 0 since only 1 axis card

        self.Motor = self.bus.get_motor(self.address,self.motor_id)
        self.MotorParamInterface =pyTMCL.motor.AxisParameterInterface(self.Motor)

        #hardware parameters
        self.microsteps = 2 ** 4
        if pump_type == "regular":
            self.dist_per_full_step = 0.0254  # mm
            self.radius = 4.6 / 2 #mm
            self.max_disp = 200  # ul

        elif pump_type=="idex 5000":
            self.dist_per_full_step = 0.00635 # mm
            self.radius = 22.388/2  # mm
            self.max_disp = 200  # ul
            self.cylinder_volume = 5000  # ul

        elif pump_type=="idex 250 lead 635":
            #Corresponds to an idex 250 with a thread of 6.35mm lead
            self.dist_per_full_step = 0.03175 # mm
            self.radius = 5.006/2  # mm
            self.max_disp = 200  # ul
            self.cylinder_volume = 250  # ul
            #self.std_asp_speed = 950
            #self.std_disp_speed = 950

        elif pump_type=="idex 250 lead 488":
            #Corresponds to an idex 250 with a thread of 4.88mm lead
            self.dist_per_full_step = 0.0244 # mm
            self.radius = 5.006/2  # mm
            self.max_disp = 200  # ul
            self.cylinder_volume = 250  # ul
            #self.std_asp_speed = 950
            #self.std_disp_speed = 950

        elif pump_type=="idex 250 lead 400":
            #Corresponds to an idex 250 with a thread of 4.00mm lead
            self.dist_per_full_step = 0.02 # mm
            self.radius = 5.006/2  # mm
            self.max_disp = 200  # ul
            self.cylinder_volume = 250  # ul
            #self.std_asp_speed = 950
            #self.std_disp_speed = 950

    def ul_to_usteps(self,volume_ul):
        steps_nb = int(volume_ul * self.microsteps / (math.pi * (self.radius ** 2) * self.dist_per_full_step))
        #print(steps_nb)
        return steps_nb

    def run_firmware_from_line(self,line):
        self.bus.send(self.address, pyTMCL.Command.RUN_APPLICATION, 1, self.motor_id, line)

    def set_global_parameter(self,parameter_number,value):
        self.bus.send(self.address, pyTMCL.Command.SGP, parameter_number, 2, value)

    def get_status(self):
        #Status is
        # 0 for idle
        # 1 for busy
        # 2 for can_move
        while(1):
            try:
                reply = self.bus.send(self.address, pyTMCL.Command.GGP, 5, 2 , 0)
                break
            except:
                print('Could not read status of the pump')

        return reply.value

    def wait_for_canmove(self):


        while 1:
            time.sleep(0.005) # has to be before in case we just asked for movement
            status=self.get_status()
            if status == 0 or status == 2:
                break

    def wait_for_idle(self):
        while 1:
            time.sleep(0.005)  # has to be before in case we just asked for movement
            status=self.get_status()
            if status == 0:
                break

    def init(self):
        self.run_firmware_from_line(0)

    def dispense(self, volume_ul):

        self.wait_for_idle()

        full_strokes = volume_ul // self.max_disp
        additional_volume= volume_ul % self.max_disp

        if additional_volume==0 and full_strokes!=0 : #Particular case where we're a multiple of 200
            full_strokes -= 1
            additional_volume = 200

        additional_volume_usteps=self.ul_to_usteps(additional_volume)

        #print(full_strokes)
        #print(additional_volume)
        #print(additional_volume_usteps)
        self.set_global_parameter(1,full_strokes)
        self.set_global_parameter(0,additional_volume_usteps)

        self.run_firmware_from_line(1)

    def dispense_only_additional(self, volume_ul):

        self.wait_for_idle()

        full_strokes=0
        additional_volume_usteps=self.ul_to_usteps(volume_ul)

        #print(full_strokes)
        #print(additional_volume)
        #print(additional_volume_usteps)
        self.set_global_parameter(1,full_strokes)
        self.set_global_parameter(0,additional_volume_usteps)

        self.run_firmware_from_line(1)

    def multi_print(self,total_volume,stroke):

        start=time.time()
        for i in range(int(total_volume//stroke)):
            print((i+1)*stroke)
            self.dispense(stroke)
            self.wait_for_idle()

        print(time.time() - start)


if __name__ == "__main__":


    serial_port = Serial('COM10', 115200)
    bus = pyTMCL.connect(serial_port)

    pump_1=DispenseUnit_1161("fakeparent",bus,1,0,'idex 250 lead 400')

    #pump_1.init()
    #pump_1.dispense(200)

    pump_1.multi_print(30000,200)
    serial_port.close()