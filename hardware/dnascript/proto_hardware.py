from hardware.common.arduinoControl import ArduinoControl, MockArduinoControl

from tkinter import *
from serial import *
from time import sleep
from hardware.common.Vacuum import *
# from cycles import *

# from thermalCamera import *
from .DispenseUnit_Arduino import *
from .DispenseBlock_USB import DispenseBlock_USB, MockDispenseBlock
from hardware.dnascript.PositioningMotors import (
    PositioningMotors,
    MockPositioningMotors,
)

MODULE_ADDRESS = 1

# X_A1=155891
# Y_A1=27818

X_A1 = 145400
Y_A1 = 38018

X_step = 9200
Y_step = 9200


class ProtoHardware(Frame):
    def __init__(self, parent, mock_components=False, *args, **kwargs):
        self.parent = parent

        self.positioning_motors_flag = 1
        self.vacuumController = 0
        self.arduino = 1
        self.positive_pressure = 0
        self.thermalCam = 1  # Will impact rightFrame in guitab1
        self.pumps = 1

        if self.positioning_motors_flag:
            if mock_components:
                self.positioning_motors = MockPositioningMotors(self)
            else:
                self.positioning_motors = PositioningMotors(self)

        if self.pumps:
            if mock_components:
                self.dispenseBlock = MockDispenseBlock(self)
            else:
                self.dispenseBlock = DispenseBlock_USB(self)

        if self.arduino:
            if mock_components:
                self.arduinoControl = MockArduinoControl(self)
            else:
                self.arduinoControl = ArduinoControl(self)

            self.arduinoControl.close_vac()
            self.arduinoControl.stopShaking()

    def initialisation(self):
        self.parent.directCommand.initialisationLed.configure(bg="red")

        # initialiseMotorList(self, [self.zMotor,self.magnetMotor])
        # self.zMotor.move_absolute_wait(self,9149)
        if self.positioning_motors_flag:
            self.initialiseMotorList(
                [self.positioning_motors.xMotor, self.positioning_motors.yMotor]
            )
        if self.arduino:
            self.arduinoControl.stopShaking()

        self.parent.directCommand.initialisationLed.configure(bg="green")

    def print_positions(self):
        # Returns the positions of all motors
        names = ["xMotor", "yMotor"]
        motorsParametersInterface = [
            self.positioning_motors.xMotor.axis,
            self.positioning_motors.yMotor.axis,
        ]
        for motorInterface in motorsParametersInterface:
            print(
                names[motorsParametersInterface.index(motorInterface)]
                + " position is "
                + str(motorInterface.actual_position)
            )

    def set_output(self, output, value):
        # Sets the digital output i to high or low depending on the value
        self.bus.send(MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value)

    def set_output2(self, output, value):
        # Sets the digital output i to high or low depending on the value on the second card
        self.bus_stirrer.send(
            MODULE_ADDRESS, TMCL.commands.Command.SIO, output, 2, value
        )

    def vacValveOpen(self):
        self.arduinoControl.open_vac()

    def vacValveClose(self):
        self.arduinoControl.close_vac()

    def init_du(self, du_index):
        self.dispenseBlock.dus[du_index].init()

    def init_all_du(self):
        self.dispenseBlock.init()

    def initialiseMotorList(self, motor_list):
        """Gets a list of motors and initialise them in parallel"""
        for motor in motor_list:
            motor.reference_search(0)

        sleep(0.6)

        nb_motors_initialised = 0
        nb_motors_to_initialise = len(motor_list)

        while nb_motors_initialised != nb_motors_to_initialise:
            nb_motors_initialised = 0
            for motor in motor_list:
                if motor.axis.get(8) == 1:
                    nb_motors_initialised += 1

            self.parent.update()
            sleep(0.2)

        for motor in motor_list:
            motor.axis.set(1, 0)  # We set the actual position to 0 for each motor

    def multi_dispense(self, volume_per_line, max_vol=None):
        """
        :param volume_per_line: dictionnaries of volumes to dispense, eg {"DB":50,"BB":15}
        :param max_vol: maximum volume to dispense in a single dispense, in particular to avoid overflows
        :return:
        """

        pumps_index = {
            "M": 0,
            "N": 1,
            "A": 2,
            "C": 3,
            "G": 4,
            "T": 5,
            "O": 6,
            "P": 7,
            "DB": 8,
            "BB": 9,
            "Buff1": 10,
            "Buff2": 11,
            "Q": 12,
        }

        full_disp_list = [0] * len(pumps_index)

        for line in volume_per_line.keys():
            full_disp_list[pumps_index[line]] = volume_per_line[line]

        if max_vol != None:
            while any(full_disp_list) > 0:
                disp_list = []
                for i in range(len(full_disp_list)):
                    if full_disp_list[i] > max_vol:
                        disp_list.append(max_vol)
                        full_disp_list[i] -= max_vol
                    else:
                        disp_list.append(full_disp_list[i])
                        full_disp_list[i] = 0

                self.dispenseBlock.multi_dispense(disp_list)

        else:
            self.dispenseBlock.multi_dispense(full_disp_list)

    def multiDispensePumps(self, volumes, max_vol=None):
        # introduced max_vol to dispense a large amount in several strokes for 384, avoiding overflow
        if max_vol != None:
            volumes_copy = volumes.copy()
            while any(volumes_copy) > 0:
                to_disp = []
                for i in range(len(volumes_copy)):
                    if volumes_copy[i] > max_vol:
                        to_disp.append(max_vol)
                        volumes_copy[i] = volumes_copy[i] - max_vol
                    else:
                        to_disp.append(volumes_copy[i])
                        volumes_copy[i] = 0

                self.dispenseBlock.multi_dispense(to_disp)
        else:
            self.dispenseBlock.multi_dispense(volumes)

    def goToWell(self, element, well, quadrant):
        """Put Lee vann or needles 'element' at the well 'well'"""

        "Positions of A1 with the M nozzle"
        # X_1 = 88822
        # Y_1 = 10518
        X_1 = X_A1
        Y_1 = Y_A1

        true384 = 0

        if quadrant == 1:
            X_1 = X_1 - int(X_step / 4)
            Y_1 = Y_1 - int(Y_step / 4)
        if quadrant == 2:
            X_1 = X_1 + int(X_step / 4)
            Y_1 = Y_1 - int(Y_step / 4)
        if quadrant == 3:
            X_1 = X_1 - int(X_step / 4)
            Y_1 = Y_1 + int(Y_step / 4)
        if quadrant == 4:
            X_1 = X_1 + int(X_step / 4)
            Y_1 = Y_1 + int(Y_step / 4)

        if quadrant == 5:  # quadrant 5 for true 384
            X_1 = X_1 - int(X_step / 4)
            Y_1 = Y_1 - int(Y_step / 4)
            true384 = 1

        positions_dict = {
            "M": [0, 0],
            "N": [1, 0],
            "O": [2, 0],
            "P": [3, 0],
            "Q": [4, 0],
            "A": [2, 1],
            "C": [3, 1],
            "G": [4, 1],
            "T": [5, 1],
            "DB": [6, -1],
            "BB": [6, 0],
            "Buff1": [6, 1],
            "Buff2": [6, 2],
        }

        if element in positions_dict.keys():
            if true384:
                X_1 = X_1 - (positions_dict[element][0] * 2) * (X_step / 2)
                Y_1 = Y_1 - (positions_dict[element][1] * 2) * (Y_step / 2)
            else:
                X_1 = X_1 - positions_dict[element][0] * X_step
                Y_1 = Y_1 - positions_dict[element][1] * Y_step

        if element == "safe":
            X_1 = 0
            Y_1 = 128344

        if element == "thermo":
            X_1 = 0
            Y_1 = 128344

        if element == "thermalCamera":
            X_1 = 0
            Y_1 = 128344

        if element == "washPrime":
            # X_1 = 167686
            X_1 = 224963
            Y_1 = 0

        if element == "premixPrime":
            X_1 = 0
            Y_1 = 0

        if true384:
            X = X_1 + ((well - 1) % 16) * (X_step / 2)
            Y = Y_1 + ((well - 1) // 16) * (Y_step / 2)
        else:
            X = X_1 + ((well - 1) % 8) * X_step
            Y = Y_1 + ((well - 1) // 8) * Y_step

        xMotor = self.positioning_motors.xMotor
        yMotor = self.positioning_motors.yMotor
        xMotor.move_absolute(X)
        yMotor.move_absolute(Y)
        sleep(0.1)

        while (
            xMotor.axis.target_position_reached == 0
            or yMotor.axis.target_position_reached == 0
        ):
            self.parent.update()
            sleep(0.1)

    def goToFakeWell(
        self,
        fake_well,
        fake_plate_dims,
        dispHead_dims,
        quadrant,
        X_step=X_step,
        Y_step=Y_step,
    ):
        # Works only for the upper left nozzle

        "Positions of A1 with the up left Lee vann"
        X_1 = X_A1 - ((dispHead_dims[0] - 1) * X_step)
        Y_1 = Y_A1 - ((dispHead_dims[1] - 1) * Y_step)

        if quadrant == 1:
            X_1 = X_1 - int(X_step / 4)
            Y_1 = Y_1 - int(Y_step / 4)
        if quadrant == 2:
            X_1 = X_1 + int(X_step / 4)
            Y_1 = Y_1 - int(Y_step / 4)
        if quadrant == 3:
            X_1 = X_1 - int(X_step / 4)
            Y_1 = Y_1 + int(Y_step / 4)
        if quadrant == 4:
            X_1 = X_1 + int(X_step / 4)
            Y_1 = Y_1 + int(Y_step / 4)
        if quadrant == 5:  # 5th quadrant for the true 384
            X_1 = X_1 - int(X_step / 2)
            Y_1 = Y_1 - int(Y_step / 2)

        X = X_1 + ((fake_well - 1) % fake_plate_dims[0]) * X_step
        Y = Y_1 + ((fake_well - 1) // fake_plate_dims[0]) * Y_step

        xMotor = self.positioning_motors.xMotor
        yMotor = self.positioning_motors.yMotor
        xMotor.move_absolute(X)
        yMotor.move_absolute(Y)
        sleep(0.1)

        while (
            xMotor.axis.target_position_reached == 0
            or yMotor.axis.target_position_reached == 0
        ):
            self.parent.update()
            sleep(0.1)

    def primeDB_Idex(self, volume_ul):
        du = self.dispenseBlock.dus[8]
        max_disp_temp = du.max_disp
        du.max_disp = du.cylinder_volume

        full_strokes = volume_ul // du.max_disp
        additional_volume = volume_ul % du.max_disp

        for i in range(full_strokes):
            du.dispense_only_additional(du.max_disp)
            du.wait_for_idle()
        du.dispense_only_additional(additional_volume)

        du.max_disp = max_disp_temp
        du.init()
