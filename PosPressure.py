from time import *


class PosPressure:

    def __init__(self,hardware,zMotor,valve):

        self.hardware = hardware
        self.zMotor = zMotor
        self.valve = valve #ID of the output on the card

        self.bottom_height=390340
        self.above_plate_height=250213

        self.dessalt_bottom_height=101140
        self.dessalt_above_plate_height=0

        self.synDessaltStack_bottom_height = 130813
        self.synDessaltStack_above_plate_height = 0

        self.cols=2
        self.rows=2

    def pressure_start(self):
        self.hardware.set_output(self.valve,1)

    def pressure_stop(self):
        self.hardware.set_output(self.valve,0)

    def goDown(self,plate="dessalt"):
        if plate=="dessalt":
            self.zMotor.move_absolute_wait(self.hardware,self.dessalt_bottom_height)
        if plate=="synthesis":
            self.zMotor.move_absolute_wait(self.hardware,self.bottom_height)
        if plate=="synDessaltStack":
            self.zMotor.move_absolute_wait(self.hardware,self.synDessaltStack_bottom_height)

    def goApproach(self,plate="dessalt"):
        if plate == "dessalt":
            self.zMotor.move_absolute_wait(self.hardware,self.dessalt_above_plate_height)
        if plate == "synthesis":
            self.zMotor.move_absolute_wait(self.hardware,self.above_plate_height)
        if plate=="synDessaltStack":
            self.zMotor.move_absolute_wait(self.hardware,self.synDessaltStack_above_plate_height)

    def goUp(self):
        self.zMotor.move_absolute_wait(self.hardware,0)

    def apply_pressure(self,time,plate="dessalt"):

        self.goDown(plate)
        self.pressure_start()
        sleep(time)
        self.pressure_stop()
        sleep(0.5)
        self.goApproach(plate)


