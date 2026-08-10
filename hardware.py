MODULE_ADDRESS = 1

from tkinter import *
from serial import *
from time import sleep
from Vacuum import *
from cycles import *
from cycles_384 import *
#from thermalCamera import *
from arduinoControl import *
from syntax_heater_shaker import *
from DispenseBlock_USB import *
from PosPressure import*
from PositioningMotors import *



class HardWare(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.instrument_name = "P4"
        self.positioning_motors_flag=1
        self.vacuumController=0
        self.arduino = 0
        self.syntax_heater_shaker = 1
        self.positive_pressure=0
        self.thermalCam=1   #Will impact rightFrame in guitab1
        self.pumps=1
        self.ventilation_valve=1

        if self.positioning_motors_flag:
            print('Connecting Positioning Motors')
            self.positioning_motors=PositioningMotors(self)

        if self.pumps:
            print('Connecting pumps')
            self.dispenseBlock=DispenseBlock_USB(self)

        if self.arduino:
            print('Connecting Arduino')
            self.arduinoControl = ArduinoControl(self)
            self.vacValveClose()
            self.arduinoControl.stopShaking()

        if self.syntax_heater_shaker:
            print('Connecting Syntax Heater Shaker')
            self.arduinoControl = Syntax_Heater_Shaker(self)
            self.vacValveClose()
            self.arduinoControl.stopShaking()


        if self.positive_pressure:
            self.posPressure=PosPressure(self,self.zMotor,1)


    def initialisation(self):

        self.parent.directCommand.initialisationLed.configure(bg='red')

        #initialiseMotorList(self, [self.zMotor,self.magnetMotor])
        #self.zMotor.move_absolute_wait(self,9149)
        if self.positioning_motors_flag:
            initialiseMotorList(self, [self.positioning_motors.xMotor,self.positioning_motors.yMotor])
        if self.arduino:
            self.arduinoControl.stopShaking()
        if self.syntax_heater_shaker:
            self.arduinoControl.stopShaking()

        self.parent.directCommand.initialisationLed.configure(bg='green')

    def give_positions(self):
        # Returns the positions of all motors
        names=['xMotor','yMotor']
        motorsParametersInterface = [self.positioning_motors.xMotor.axis, self.positioning_motors.yMotor.axis]
        for motorInterface in motorsParametersInterface:
            print (names[motorsParametersInterface.index(motorInterface)] + ' position is ' + str(motorInterface.actual_position))


    def set_output(self, output, value):
        # Sets the digital output i to high or low depending on the value
        self.positioning_motors.bus.send(MODULE_ADDRESS, pyTMCL.commands.Command.SIO, output, 2, value)

    def vacValveOpen(self):
        if self.ventilation_valve:
            self.set_output(1,1)
        self.set_output(2, 1)

    def vacValveClose(self):
        self.set_output(2,0)
        if self.ventilation_valve:
            self.set_output(1,0)

    def init_du(self,du_index):
        self.dispenseBlock.dus[du_index].init()

    def init_all_du(self):
        self.dispenseBlock.init()

