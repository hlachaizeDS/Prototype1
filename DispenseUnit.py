import TMCL
import math
import time


class DispenseUnit():
    def __init__(self, parent,motor ,motor_parameters,bus_pump,digOut,size="small"):
        self.parent = parent

        self.motor = motor
        self.motor_parameters = motor_parameters

        self.set_param_std()

        self.bus_tmcl=bus_pump
        self.digOut=digOut

        self.microsteps=2**6
        self.dist_per_full_step=0.01 #mm

        self.max_disp=80 #ul
        self.pullback=3 #ul

        if (size=="small"):
            self.radius = 3 / 2
            self.max_disp = 80  # ul
            self.pullback = 3  # ul
            self.init_forward = 110  # ul
        elif (size=="big"):
            self.radius = 4.6 / 2
            self.max_disp = 200  # ul
            self.pullback = 10  # ul
            self.init_forward = 210  # ul

        #init
        self.init_backward=self.max_disp+self.pullback+1 #ul


    def dispense(self,volume):

        remaining_vol=volume
        while remaining_vol!=0:
            if remaining_vol<=self.max_disp:
                vol_to_disp=remaining_vol
            else:
                vol_to_disp=self.max_disp

            self.wait_for_pos()

            steps_nb=int(vol_to_disp*self.microsteps/(math.pi*(self.radius**2)*self.dist_per_full_step))

            self.open_valve()
            self.motor.move_absolute_wait(self.parent,steps_nb)
            self.zero()

            remaining_vol-=vol_to_disp

    def push(self,volume):
        self.wait_for_pos()
        self.open_valve()
        steps_nb = int((volume+self.pullback) * self.microsteps / (math.pi * (self.radius ** 2) * self.dist_per_full_step))
        self.motor.move_relative( steps_nb)

    def pull(self,volume):
        self.wait_for_pos()
        self.open_valve()
        steps_nb = int(volume * self.microsteps / (math.pi * (self.radius ** 2) * self.dist_per_full_step))
        self.motor.move_relative( -steps_nb)

    def pull_from_reservoir(self,volume):
        self.wait_for_pos()
        self.close_valve()
        steps_nb = int(volume * self.microsteps / (math.pi * (self.radius ** 2) * self.dist_per_full_step))
        self.motor.move_relative( -steps_nb)

    def open_valve(self):
        self.bus_tmcl.send(1, TMCL.commands.Command.SIO, self.digOut, 2, 1)

    def close_valve(self):
        self.bus_tmcl.send(1, TMCL.commands.Command.SIO, self.digOut, 2, 0)

    def zero(self):
        self.wait_for_pos()
        self.close_valve()
        self.motor.move_absolute(0)

    def wait_for_pos(self):
        while self.motor_parameters.get(8) == 0:
            time.sleep(0.05)

    def set_param_init(self):
        self.wait_for_pos()
        # we reduce current, velocity,acceleration and deceleration
        self.motor_parameters.set(6, 90)
        self.motor_parameters.set(5, int(7629278 / 10))
        self.motor_parameters.set(17, int(7629278 / 10))
        self.motor_parameters.set(4, int(450000 / 10))

    def set_param_std(self):
        self.wait_for_pos()
        self.motor_parameters.set(6, 162)
        self.motor_parameters.set(5, 6629278)
        self.motor_parameters.set(17, 6629278)
        self.motor_parameters.set(4, 350000)

    def initialise_position(self):

        self.set_param_init()

        self.push(self.init_forward)

        self.set_param_std()

        self.pull(self.pullback)

        self.pull_from_reservoir(self.init_backward)

        self.wait_for_pos()

        self.motor_parameters.set(1, 0)
        self.motor_parameters.set(0, 0)

