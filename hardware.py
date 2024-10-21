MODULE_ADDRESS = 1

from DispenseUnit_Arduino import *
from tkinter import *
from serial import *
from time import sleep
from Vacuum import *
from cycles import *
#from thermalCamera import *
from arduinoControl import *
from DispenseBlock_USB import *
from PositioningMotors import *



class HardWare(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.positioning_motors_flag=1
        self.vacuumController=0
        self.arduino=1
        self.positive_pressure=0
        self.thermalCam=1   #Will impact rightFrame in guitab1
        self.pumps=1

        if self.positioning_motors_flag:
            self.positioning_motors=PositioningMotors(self)

        if self.pumps:

            self.dispenseBlock=DispenseBlock_USB(self)

        if self.arduino:
            self.arduinoControl=ArduinoControl(self)
            self.arduinoControl.close_vac()
            self.arduinoControl.stopShaking()


    def initialisation(self):

        self.parent.directCommand.initialisationLed.configure(bg='red')

        #initialiseMotorList(self, [self.zMotor,self.magnetMotor])
        #self.zMotor.move_absolute_wait(self,9149)
        if self.positioning_motors_flag:
            initialiseMotorList(self, [self.positioning_motors.xMotor,self.positioning_motors.yMotor])
        if self.arduino:
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
        self.bus.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def set_output2(self, output, value):
        # Sets the digital output i to high or low depending on the value on the second card
        self.bus_stirrer.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def vacValveOpen(self):
        self.arduinoControl.open_vac()

    def vacValveClose(self):
        self.arduinoControl.close_vac()

    def init_du(self,du_index):
        self.dispenseBlock.dus[du_index].init()

    def init_all_du(self):
        self.dispenseBlock.init()

