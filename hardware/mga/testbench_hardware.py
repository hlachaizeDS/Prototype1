from hardware.common.arduinoControl import ArduinoControl
from tkinter import Frame
import grpc
import mga_testbench_interface.generated.gantry_pb2_grpc as gantry_grpc
import mga_testbench_interface.generated.gantry_pb2 as gantry


class MGATestbenchHardware(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.arduinoControl = None  # ArduinoControl()

        self.channel = grpc.insecure_channel("localhost:7050")
        self.gantry = gantry_grpc.GantryStub(self.channel)

    def initialisation(self):
        # self.parent.directCommand.initialisationLed.configure(bg="red")
        if self.arduinoControl:
            self.arduinoControl.close_vac()
            self.arduinoControl.stopShaking()

        self.gantry.setParameters(
            gantry.AxisParameters(
                axes=[
                    gantry.AxisParameters.AxisInnerParameters(
                        axis=gantry.Axis.x,
                        speed=100,
                        acceleration=100,
                        deceleration=100,
                    ),
                    gantry.AxisParameters.AxisInnerParameters(
                        axis=gantry.Axis.y,
                        speed=100,
                        acceleration=100,
                        deceleration=100,
                    ),
                ]
            )
        )
        # self.parent.directCommand.initialisationLed.configure(bg="green")

    def print_positions(self):
        position: gantry.Position = self.gantry.getPosition(gantry._())
        print("Current position: ", position.x, position.y)
        pass

    def vacValveOpen(self):
        if self.arduinoControl:
            self.arduinoControl.open_vac()
        else:
            print("Arduino control not initialized")

    def vacValveClose(self):
        if self.arduinoControl:
            self.arduinoControl.close_vac()
        else:
            print("Arduino control not initialized")

    def multi_dispense(self, volume_per_line: dict[str, tuple[float, list[int]]], max_vol=None):
        print("Dispensing ", volume_per_line, "uL")
        pass

    def multiDispensePumps(self, volumes, max_vol=None):
        print("Dispensing ", volumes, "uL")
        pass

    def goToWell(self, element, well, quadrant):
        print("Going to ", element, well, quadrant)
        self.gantry.moveTo()
        pass

