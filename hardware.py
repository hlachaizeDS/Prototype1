MODULE_ADDRESS = 1
PORT_MOTORX = "COM27"
PORT_MOTORY = "COM29"

from DispenseUnit_Arduino import *
from tkinter import *
from serial import *
from time import sleep
import TMCL
from Vacuum import *
from cycles import *
from thermometre import *
#from thermalCamera import *
from arduinoControl import *
from DispenseUnit import *
from PosPressure import*



class HardWare(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.motorX=1
        self.motorY=1
        self.vacuumController=0
        self.arduino=1
        self.positive_pressure=0
        self.thermalCam=1   #Will impact rightFrame in guitab1
        self.pumps=1

        self.positioning_motors=[]
        self.positioning_motors_parameters=[]

        if self.motorX :
            serial_port = Serial(PORT_MOTORX,9600)
            self.bus_x = TMCL.connect(serial_port)

            self.xMotor = self.bus_x.get_motor(MODULE_ADDRESS, 0)
            self.xMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.xMotor)

            self.positioning_motors.append(self.xMotor)
            self.positioning_motors_parameters.append(self.xMotorParametersInterface)

        if self.motorY:
            serial_port = Serial(PORT_MOTORY, 9600)
            self.bus_y = TMCL.connect(serial_port)

            self.yMotor = self.bus_y.get_motor(MODULE_ADDRESS, 0)
            self.yMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.yMotor)

            self.positioning_motors.append(self.yMotor)
            self.positioning_motors_parameters.append(self.yMotorParametersInterface)

        stallguard_value = 30  # -64..+63
        stallguard_minimum_speed = 5000  # 0...7999774
        reverse_shaft = [1,0]  # changes the sens of rotation
        current_max = [150, 200, 120, 255, 60]  # 0..255
        current_standby = [20, 50, 8, 25, 8]  # 0..255
        acceleration_max = [3629278, 3629278, 7629278, 400000, 500000]  # 0...7629278
        deceleration_max = acceleration_max  # 0...7629278
        reference_type = [1, 1, 2, 1, 65]
        swap_switches = [0, 0, 1, 0, 0]
        right_limit_switch_polarity = [0, 0, 0, 0, 1]
        left_limit_switch_polarity = [0, 0, 0, 0, 0]
        reference_search_velocity = [50000, 50000, 150000, 100000, 100000]
        precise_reference_search_velocity = [5000, 5000, 5000, 15000, 5000]
        velocity_max = [400000, 400000, 200000]  # 0...7999774
        velocity_V1 = 0  # the target velocity to attain before going to a second phase of velocity
        microsteps = [8,8,6]
        # Disables the feature if set to 0

        for motor in self.positioning_motors_parameters:
            motor.set(4, velocity_max[self.positioning_motors_parameters.index(motor)])
            motor.set(5, acceleration_max[self.positioning_motors_parameters.index(motor)])
            motor.set(6, current_max[self.positioning_motors_parameters.index(motor)])
            motor.set(7, current_standby[self.positioning_motors_parameters.index(motor)])
            motor.set(17, deceleration_max[self.positioning_motors_parameters.index(motor)])
            motor.set(16, velocity_V1)
            motor.set(14, swap_switches[self.positioning_motors_parameters.index(motor)])
            motor.set(24, right_limit_switch_polarity[self.positioning_motors_parameters.index(motor)])
            motor.set(25, left_limit_switch_polarity[self.positioning_motors_parameters.index(motor)])

            motor.set(193, reference_type[self.positioning_motors_parameters.index(motor)])
            motor.set(194, reference_search_velocity[self.positioning_motors_parameters.index(motor)])
            motor.set(195, precise_reference_search_velocity[self.positioning_motors_parameters.index(motor)])
            motor.set(140, microsteps[self.positioning_motors_parameters.index(motor)])
            motor.set(251, reverse_shaft[self.positioning_motors_parameters.index(motor)])

        if self.pumps:

            COM_PORTS_PUMPS=[6,4,3,5,7,8,9,10,11,12,13,14]

            self.dus=[]
            for port in COM_PORTS_PUMPS:
                self.dus.append(DispenseUnit_Arduino(self,"COM" + str(port)))

        if self.arduino:
            self.arduinoControl=ArduinoControl(self)
            self.arduinoControl.stopShaking()

        if self.positive_pressure:
            self.posPressure=PosPressure(self,self.zMotor,1)


    def initialisation(self):

        self.parent.directCommand.initialisationLed.configure(bg='red')

        #initialiseMotorList(self, [self.zMotor,self.magnetMotor])
        #self.zMotor.move_absolute_wait(self,9149)
        if self.motorX and self.motorY:
            initialiseMotorList(self, [self.xMotor,self.yMotor])
        if self.arduino:
            self.arduinoControl.stopShaking()

        self.parent.directCommand.initialisationLed.configure(bg='green')

    def give_positions(self):
        # Returns the positions of all motors
        names=['xMotor','yMotor','zMotor']
        motorsParametersInterface = [self.xMotorParametersInterface, self.yMotorParametersInterface]
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

    def DBSwitchOpen(self):
        self.set_output(1,1)

    def DBSwitchClose(self):
        self.set_output(1, 0)


    def init_du(self,du_index):
        self.dus[du_index].init()

    def init_all_du(self):

        for du in range(12):
            self.dus[du].init()

    def apply_axis_parameters(self,motor_parameters_list, velocity_max, acceleration_max, current_max, current_standby,
                                  deceleration_max, velocity_V1, swap_switches, right_limit_switch_polarity,
                              left_limit_switch_polarity, reference_type,reference_search_velocity,
                              precise_reference_search_velocity, microsteps
                                  ):
        for motor in motor_parameters_list:
            motor.set(4, velocity_max[motor_parameters_list.index(motor)])
            motor.set(5, acceleration_max[motor_parameters_list.index(motor)])
            motor.set(6, current_max[motor_parameters_list.index(motor)])
            motor.set(7, current_standby[motor_parameters_list.index(motor)])
            motor.set(17, deceleration_max[motor_parameters_list.index(motor)])
            motor.set(16, velocity_V1)
            motor.set(14, swap_switches[motor_parameters_list.index(motor)])
            motor.set(24, right_limit_switch_polarity[motor_parameters_list.index(motor)])
            motor.set(25, left_limit_switch_polarity[motor_parameters_list.index(motor)])

            motor.set(193, reference_type[motor_parameters_list.index(motor)])
            motor.set(194, reference_search_velocity[motor_parameters_list.index(motor)])
            motor.set(195, precise_reference_search_velocity[motor_parameters_list.index(motor)])
            motor.set(140, microsteps[motor_parameters_list.index(motor)])
