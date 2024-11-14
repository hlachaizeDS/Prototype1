from hardware.common.arduinoControl import ArduinoControl
from tkinter import Frame


class MGATestbenchHardware(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.arduinoControl = ArduinoControl()

    def initialisation(self):
        self.parent.directCommand.initialisationLed.configure(bg="red")
        if self.arduinoControl:
            self.arduinoControl.close_vac()
            self.arduinoControl.stopShaking()
        self.parent.directCommand.initialisationLed.configure(bg="green")

    def print_positions(self):
        pass

    def vacValveOpen(self):
        self.arduinoControl.open_vac()

    def vacValveClose(self):
        self.arduinoControl.close_vac()
