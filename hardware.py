MODULE_ADDRESS = 1
PORT = "COM3"
PORT_2 = "COM5"
PORT_VACUUM = "COM6"
PORT_PUMP_1="COM4"
PORT_PUMP_2="COM5"
PORT_PUMP_3="COM6"
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
from DispenseUnit import *
from PosPressure import*



class HardWare(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        self.firstCard=1
        self.secondCard=0
        self.vacuumController=0
        self.arduino=1
        self.positive_pressure=0
        self.thermalCam=1   #Will impact rightFrame in guitab1
        self.pump_card_1 = 1
        self.pump_card_2 = 1
        self.pump_card_3 = 1

        if self.firstCard :
            #try:
                serial_port = Serial(PORT,9600)
                self.bus = TMCL.connect(serial_port)

                self.xMotor = self.bus.get_motor(MODULE_ADDRESS, 0)
                self.xMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.xMotor)

                self.yMotor = self.bus.get_motor(MODULE_ADDRESS, 1)
                self.yMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.yMotor)

                self.zMotor = self.bus.get_motor(MODULE_ADDRESS, 2)
                self.zMotorParametersInterface = TMCL.motor.AxisParameterInterface(self.zMotor)

                stallguard_value = 30  # -64..+63
                stallguard_minimum_speed = 5000  # 0...7999774
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
                velocity_max = [400000, 400000, 200000, STIRRING_VELOCITY, 300000]  # 0...7999774
                velocity_V1 = 0  # the target velocity to attain before going to a second phase of velocity
                microsteps = [8,8,6]
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
                    motor.set(140, microsteps[motorsParametersInterface.index(motor)])

                    digitalOutputsNb2 = 8
                    for i in range(digitalOutputsNb2):
                        self.set_output(i, 0)
                if self.positive_pressure:
                    initialiseMotorList(self,[self.zMotor])

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

        if self.positive_pressure:
            self.posPressure=PosPressure(self,self.zMotor,1)

        if self.pump_card_1 :

            serial_port_pump_1 = Serial(PORT_PUMP_1, 9600)
            self.bus_pump_1 = TMCL.connect(serial_port_pump_1)

            self.motors_pump_1=[]
            self.motors_parameters_pump_1=[]
            for i in range(3):
                self.motors_pump_1.append(self.bus_pump_1.get_motor(MODULE_ADDRESS,i))
                self.motors_parameters_pump_1.append(TMCL.motor.AxisParameterInterface(self.motors_pump_1[-1]))

            stallguard_value = 30  # -64..+63
            stallguard_minimum_speed = 5000  # 0...7999774
            current_max = [130 for i in range(3)]   # 0..255
            current_standby = [8 for i in range(3)]   # 0..255
            acceleration_max = [6629278 for i in range(3)]  # 0...7629278
            deceleration_max = acceleration_max  # 0...7629278
            reference_type = [65,65,65]
            swap_switches = [0,0,0]
            right_limit_switch_polarity = [0,0,0]
            left_limit_switch_polarity = [0,0,0]
            reference_search_velocity = [100000 for i in range(3)]
            precise_reference_search_velocity = [5000 for i in range(3)]
            velocity_max = [350000 for i in range(3)]
            microsteps = [6 for i in range(3)]
            velocity_V1=0

            self.apply_axis_parameters(self.motors_parameters_pump_1, velocity_max, acceleration_max, current_max, current_standby,
                                       deceleration_max, velocity_V1, swap_switches, right_limit_switch_polarity,
                                       left_limit_switch_polarity, reference_type,reference_search_velocity,
                                       precise_reference_search_velocity, microsteps
                                       )

            self.dispense_units_1=[]
            for i in range(3):
                self.dispense_units_1.append(DispenseUnit(self,self.motors_pump_1[i],self.motors_parameters_pump_1[i],self.bus_pump_1,i))

        if self.pump_card_2 :

            serial_port_pump_2 = Serial(PORT_PUMP_2, 9600)
            self.bus_pump_2 = TMCL.connect(serial_port_pump_2)

            self.motors_pump_2=[]
            self.motors_parameters_pump_2=[]
            for i in range(3):
                self.motors_pump_2.append(self.bus_pump_2.get_motor(MODULE_ADDRESS,i))
                self.motors_parameters_pump_2.append(TMCL.motor.AxisParameterInterface(self.motors_pump_2[-1]))

            stallguard_value = 30  # -64..+63
            stallguard_minimum_speed = 5000  # 0...7999774
            current_max = [130 for i in range(3)]   # 0..255
            current_standby = [8 for i in range(3)]   # 0..255
            acceleration_max = [6629278 for i in range(3)]  # 0...7629278
            deceleration_max = acceleration_max  # 0...7629278
            reference_type = [65,65,65]
            swap_switches = [0,0,0]
            right_limit_switch_polarity = [0,0,0]
            left_limit_switch_polarity = [0,0,0]
            reference_search_velocity = [100000 for i in range(3)]
            precise_reference_search_velocity = [5000 for i in range(3)]
            velocity_max = [350000 for i in range(3)]
            microsteps = [6 for i in range(3)]
            velocity_V1=0

            self.apply_axis_parameters(self.motors_parameters_pump_2, velocity_max, acceleration_max, current_max, current_standby,
                                       deceleration_max, velocity_V1, swap_switches, right_limit_switch_polarity,
                                       left_limit_switch_polarity, reference_type,reference_search_velocity,
                                       precise_reference_search_velocity, microsteps
                                       )

            self.dispense_units_2=[]
            for i in range(3):
                self.dispense_units_2.append(DispenseUnit(self,self.motors_pump_2[i],self.motors_parameters_pump_2[i],self.bus_pump_2,i))


        if self.pump_card_3 :

            serial_port_pump_2 = Serial(PORT_PUMP_3, 9600)
            self.bus_pump_3 = TMCL.connect(serial_port_pump_2)

            self.motors_pump_3=[]
            self.motors_parameters_pump_3=[]
            for i in range(3):
                self.motors_pump_3.append(self.bus_pump_3.get_motor(MODULE_ADDRESS,i))
                self.motors_parameters_pump_3.append(TMCL.motor.AxisParameterInterface(self.motors_pump_3[-1]))

            stallguard_value = 30  # -64..+63
            stallguard_minimum_speed = 5000  # 0...7999774
            current_max = [130 for i in range(3)]   # 0..255
            current_standby = [8 for i in range(3)]   # 0..255
            acceleration_max = [6629278 for i in range(3)]  # 0...7629278
            deceleration_max = acceleration_max  # 0...7629278
            reference_type = [65,65,65]
            swap_switches = [0,0,0]
            right_limit_switch_polarity = [0,0,0]
            left_limit_switch_polarity = [0,0,0]
            reference_search_velocity = [100000 for i in range(3)]
            precise_reference_search_velocity = [5000 for i in range(3)]
            velocity_max = [350000 for i in range(3)]
            microsteps = [6 for i in range(3)]
            velocity_V1=0

            self.apply_axis_parameters(self.motors_parameters_pump_3, velocity_max, acceleration_max, current_max, current_standby,
                                       deceleration_max, velocity_V1, swap_switches, right_limit_switch_polarity,
                                       left_limit_switch_polarity, reference_type,reference_search_velocity,
                                       precise_reference_search_velocity, microsteps
                                       )

            self.dispense_units_3=[]

            self.dispense_units_3.append(DispenseUnit(self,self.motors_pump_3[0],self.motors_parameters_pump_3[0],self.bus_pump_3,0,"very big"))
            self.dispense_units_3.append(DispenseUnit(self,self.motors_pump_3[1],self.motors_parameters_pump_3[1],self.bus_pump_3,1,"chineseMotor"))
            self.dispense_units_3.append(DispenseUnit(self, self.motors_pump_3[2], self.motors_parameters_pump_3[2], self.bus_pump_3, 2, "very big"))


    def initialisation(self):

        self.parent.directCommand.initialisationLed.configure(bg='red')

        #initialiseMotorList(self, [self.zMotor,self.magnetMotor])
        #self.zMotor.move_absolute_wait(self,9149)
        if self.firstCard:
            if self.positive_pressure:
                initialiseMotorList(self, [self.zMotor])
            initialiseMotorList(self, [self.xMotor,self.yMotor])
        if self.arduino:
            self.arduinoControl.stopShaking()

        self.parent.directCommand.initialisationLed.configure(bg='green')

    def give_positions(self):
        # Returns the positions of all motors
        names=['xMotor','yMotor','zMotor']
        motorsParametersInterface = [self.xMotorParametersInterface, self.yMotorParametersInterface, self.zMotorParametersInterface]
        for motorInterface in motorsParametersInterface:
            print (names[motorsParametersInterface.index(motorInterface)] + ' position is ' + str(motorInterface.actual_position))


    def set_output(self, output, value):
        # Sets the digital output i to high or low depending on the value
        self.bus.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def set_output2(self, output, value):
        # Sets the digital output i to high or low depending on the value on the second card
        self.bus_stirrer.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def vacValveOpen(self):
        self.set_output(2,1)

    def vacValveClose(self):
        self.set_output(2, 0)

    def pressureOpen(self):
        self.set_output(1,1)

    def pressureClose(self):
        self.set_output(1, 0)

    def init_du(self,du_index):
        #du_index from 0 to 5
        if du_index in [0,1,2]:
            self.dispense_units_1[du_index].initialise_position()
        elif du_index in [3,4,5]:
            self.dispense_units_2[du_index-3].initialise_position()
        else:
            self.dispense_units_3[du_index - 6].initialise_position()

    def init_all_du(self):

        #du_index from 0 to 5
        for du_index in [0,1,2]:
            self.dispense_units_1[du_index].set_param_init()
            self.dispense_units_2[du_index].set_param_init()
            self.dispense_units_3[du_index].set_param_init()
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].push(self.dispense_units_1[du_index].init_forward)
            self.dispense_units_2[du_index].push(self.dispense_units_2[du_index].init_forward)
            self.dispense_units_3[du_index].push(self.dispense_units_3[du_index].init_forward)
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].set_param_std()
            self.dispense_units_2[du_index].set_param_std()
            self.dispense_units_3[du_index].set_param_std()
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].pull(self.dispense_units_1[du_index].pullback)
            self.dispense_units_2[du_index].pull(self.dispense_units_2[du_index].pullback)
            self.dispense_units_3[du_index].pull(self.dispense_units_3[du_index].pullback)
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].pull_from_reservoir(self.dispense_units_1[du_index].init_backward)
            self.dispense_units_2[du_index].pull_from_reservoir(self.dispense_units_2[du_index].init_backward)
            self.dispense_units_3[du_index].pull_from_reservoir(self.dispense_units_3[du_index].init_backward)
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].wait_for_pos()
            self.dispense_units_2[du_index].wait_for_pos()
            self.dispense_units_3[du_index].wait_for_pos()
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].motor_parameters.set(1, 0)
            self.dispense_units_2[du_index].motor_parameters.set(1, 0)
            self.dispense_units_3[du_index].motor_parameters.set(1, 0)
        for du_index in [0, 1, 2]:
            self.dispense_units_1[du_index].motor_parameters.set(0, 0)
            self.dispense_units_2[du_index].motor_parameters.set(0, 0)
            self.dispense_units_3[du_index].motor_parameters.set(0, 0)

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
