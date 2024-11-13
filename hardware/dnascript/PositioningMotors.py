from serial import *
import pyTMCL
import COM_port


class PositioningMotors:
    '''
    Represents an X and Y motors
    '''

    def __init__(self,parent):

        self.parent = parent

        comport_dictionnaries = COM_port.list_1161_coms_by_adress()
        x_port = comport_dictionnaries[21]
        y_port = comport_dictionnaries[22]

        self.xserial_port = Serial(x_port, 115200, timeout=5)
        self.xbus = pyTMCL.connect(self.xserial_port)
        self.xMotor = self.xbus.get_motor(1, 0)

        self.yserial_port = Serial(y_port, 115200, timeout=5)
        self.ybus = pyTMCL.connect(self.yserial_port)
        self.yMotor = self.ybus.get_motor(1, 0)

        self.apply_std_parameters([self.xMotor,self.yMotor])

    def apply_std_parameters(self, motor_list):

        reverse_shaft = [1, 0]  # changes the sens of rotation
        current_max = [150,200]  # 0..255
        current_standby = [20, 50]  # 0..255
        acceleration_max = [3629278, 3629278]  # 0...7629278
        deceleration_max = acceleration_max  # 0...7629278
        reference_type = [1, 1]
        swap_switches = [0, 0]
        right_limit_switch_polarity = [0, 0]
        left_limit_switch_polarity = [0, 0]
        reference_search_velocity = [50000, 50000]
        precise_reference_search_velocity = [5000, 5000]
        velocity_max = [400000, 400000]  # 0...7999774
        velocity_V1 = 0  # the target velocity to attain before going to a second phase of velocity
        microsteps = [8, 8, 6]

        for motor in motor_list:
            motor.set_axis_parameter(4, velocity_max[motor_list.index(motor)])
            motor.set_axis_parameter(5, acceleration_max[motor_list.index(motor)])
            motor.set_axis_parameter(6, current_max[motor_list.index(motor)])
            motor.set_axis_parameter(7, current_standby[motor_list.index(motor)])
            motor.set_axis_parameter(17, deceleration_max[motor_list.index(motor)])
            motor.set_axis_parameter(16, velocity_V1)
            motor.set_axis_parameter(14, swap_switches[motor_list.index(motor)])
            motor.set_axis_parameter(24, right_limit_switch_polarity[motor_list.index(motor)])
            motor.set_axis_parameter(25, left_limit_switch_polarity[motor_list.index(motor)])

            motor.set_axis_parameter(193, reference_type[motor_list.index(motor)])
            motor.set_axis_parameter(194, reference_search_velocity[motor_list.index(motor)])
            motor.set_axis_parameter(195, precise_reference_search_velocity[motor_list.index(motor)])
            motor.set_axis_parameter(140, microsteps[motor_list.index(motor)])
            motor.set_axis_parameter(251, reverse_shaft[motor_list.index(motor)])

if __name__ == "__main__":

    positioning_motors=PositioningMotors("FP")