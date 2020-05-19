MODULE_ADDRESS = 1
PORT = "COM3"
PORT_2 = "COM5"
PORT_VACUUM = "COM6"
STALLGUARD_THRESHOLD = 0
STIRRING_VELOCITY=1050000


from tkinter import *
from serial import *
from time import sleep
import TMCL
from Vacuum import *
from cycles import *
from thermometre import *
#from thermalCamera import *
from arduinoControl import *



class HardWare(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.firstCard=0
        self.secondCard=0
        self.vacuumController=0
        self.arduino=0
        self.thermalCam=0   #Will impact rightFrame in guitab1

        if self.firstCard :
            #try:
                serial_port = Serial(PORT,9600)
                self.bus = TMCL.connect(serial_port)

                self.xMotor = self.bus.get_motor(MODULE_ADDRESS, 1)
                self.xMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.xMotor)

                self.yMotor = self.bus.get_motor(MODULE_ADDRESS, 2)
                self.yMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.yMotor)

                self.zMotor = self.bus.get_motor(MODULE_ADDRESS, 0)
                self.zMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.zMotor)

                stallguard_value = 30  # -64..+63
                stallguard_minimum_speed = 5000  # 0...7999774
                current_max = [100, 100, 30, 255, 60]  # 0..255
                current_standby = [25, 100, 8, 25, 8]  # 0..255
                acceleration_max = [1000000, 100000000, 20000000, 400000, 500000]  # 0...7629278
                deceleration_max = acceleration_max  # 0...7629278
                reference_type = [1, 1, 65, 1, 65]
                swap_switches = [0, 1, 1, 0, 0]
                right_limit_switch_polarity = [0, 0, 0, 0, 1]
                left_limit_switch_polarity = [0, 0, 0, 0, 0]
                reference_search_velocity = [50000, 50000, 150000, 100000, 100000]
                precise_reference_search_velocity = [5000, 5000, 5000, 15000, 5000]
                velocity_max = [400000, 400000, 2000000, STIRRING_VELOCITY, 300000]  # 0...7999774
                velocity_V1 = 0  # the target velocity to attain before going to a second phase of velocity
                # Disables the feature if set to 0

                motors = [self.xMotor, self.yMotor, self.zMotor]
                motorsParametersInterface = [self.xMotorParametersInterface, self.yMotorParametersInterface,
                                             self.zMotorParametersInterface]

                for motor in motorsParametersInterface:
                    motor.set(4, velocity_max[motorsParametersInterface.index(motor)])
                    motor.set(5, acceleration_max[motorsParametersInterface.index(motor)])
                    motor.set(6, current_max[motorsParametersInterface.index(motor)])
                    motor.set(7, current_standby[motorsParametersInterface.index(motor)])
                    motor.set(17, deceleration_max[motorsParametersInterface.index(motor)])
                    motor.set(16, velocity_V1)
                    motor.set(14, swap_switches[motorsParametersInterface.index(motor)])
                    motor.set(24, right_limit_switch_polarity[motorsParametersInterface.index(motor)])
                    motor.set(25, left_limit_switch_polarity[motorsParametersInterface.index(motor)])

                    motor.set(193, reference_type[motorsParametersInterface.index(motor)])
                    motor.set(194, reference_search_velocity[motorsParametersInterface.index(motor)])
                    motor.set(195, precise_reference_search_velocity[motorsParametersInterface.index(motor)])

                    digitalOutputsNb2 = 8
                    for i in range(digitalOutputsNb2):
                        self.set_output(i, 0)


            #except  SerialException:
             #   print ("Port " + PORT + " not Found")
              #  sys.exit(1)


        if self.secondCard :
            #try:
                serial_port_2 = Serial(PORT_2,9600)
                self.bus_stirrer = TMCL.connect(serial_port_2)

                digitalOutputsNb2 = 8
                for i in range(digitalOutputsNb2):
                    self.set_output2(i, 0)

                self.vacValveOpen()
            #except  SerialException:
             #   print("Port " + PORT_2 + " not Found")
              #  sys.exit(1)

        if self.vacuumController :
            try:
                ser = Serial(PORT_VACUUM , baudrate=57600)
                self.vacuum = Vacuum(self,ser)

            except  SerialException:
                print ("Port " + PORT_VACUUM + " not Found")
                sys.exit(1)


        if self.arduino:
            self.arduinoControl=ArduinoControl(self)
            self.arduinoControl.stopShaking()


    def initialisation(self):

        self.parent.directCommand.initialisationLed.configure(bg='red')

        #initialiseMotorList(self, [self.zMotor,self.magnetMotor])
        #self.zMotor.move_absolute_wait(self,9149)
        initialiseMotorList(self, [self.xMotor,self.yMotor])
        self.arduinoControl.stopShaking()

        self.parent.directCommand.initialisationLed.configure(bg='green')

    def give_positions(self):
        # Returns the positions of all motors
        names=['xMotor','yMotor','zMotor','stirrerMotor','magnetMotor']
        motorsParametersInterface = [self.xMotorParametersInterface, self.yMotorParametersInterface, self.zMotorParametersInterface, self.stirrerMotorParametersInterface, self.magnetMotorParametersInterface]
        for motorInterface in motorsParametersInterface:
            print (names[motorsParametersInterface.index(motorInterface)] + ' position is ' + str(motorInterface.actual_position))


    def set_output(self, output, value):
        # Sets the digital output i to high or low depending on the value
        self.bus.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def set_output2(self, output, value):
        # Sets the digital output i to high or low depending on the value on the second card
        self.bus_stirrer.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def vacValveOpen(self):
        self.set_output2(6,1)

    def vacValveClose(self):
        self.set_output2(6, 0)


