from hardware.common.arduinoControl import ArduinoControl
from tkinter import Frame
import grpc
import mga_testbench_interface.generated.gantry_pb2_grpc as gantry_grpc
import mga_testbench_interface.generated.gantry_pb2 as gantry
import mga_testbench_interface.generated.valves_pb2_grpc as valves_grpc
import mga_testbench_interface.generated.valves_pb2 as valves
import mga_testbench_interface.generated.pumps_pb2_grpc as pumps_grpc
import mga_testbench_interface.generated.pumps_pb2 as pumps
import time

from hardware.mga.configuration import (
    DefaultGeometry,
    LineConfigurations,
    ReagentToFluidicLineIndexMapping,
    FluidicLineIndexToPumpIndexMapping,
    Axis,
    PumpDynamicsMapping,
    PumpMaxVolume,
    PumpSlack,
    DefaultGantryParameters,
)
from hardware.mga.dispense import (
    create_dispense_plan,
    create_abstract_routine,
    project_routine_to_axes,
    ReagentVolumeWells,
    DefaultDispenseTrips,
)
from hardware.mga.movement import (
    get_movement_range_coordinates,
    DispenseMovementMargin,
    get_gantry_dispense_movement_speed,
)
from hardware.mga.types import Coordinate, PumpIndex
from hardware.mga.fluidics import (
    estimate_volume_usage,
    get_pump_start_stop_positions,
    PumpStartMargin,
)


class MGATestbenchHardware(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.arduinoControl = None  # ArduinoControl()

        self.channel = grpc.insecure_channel("localhost:7050")
        self.gantry = gantry_grpc.GantryStub(self.channel)
        self.valves = valves_grpc.ValvesStub(self.channel)
        self.pumps = pumps_grpc.PumpsStub(self.channel)

    def initialisation(self):
        # self.parent.directCommand.initialisationLed.configure(bg="red")
        if self.arduinoControl:
            self.arduinoControl.close_vac()
            self.arduinoControl.stopShaking()

        x = DefaultGantryParameters.axes[Axis.x]
        y = DefaultGantryParameters.axes[Axis.y]

        self.gantry.home(gantry._())
        self.gantry.setParameters(
            gantry.AxisParameters(
                axes=[
                    gantry.AxisParameters.AxisInnerParameters(
                        axis=gantry.Axis.x,
                        speed=x.speed if x.speed is not None else 40,
                        acceleration=x.acceleration,
                        deceleration=x.deceleration,
                    ),
                    gantry.AxisParameters.AxisInnerParameters(
                        axis=gantry.Axis.y,
                        speed=y.speed,
                        acceleration=y.acceleration,
                        deceleration=y.deceleration,
                    ),
                ]
            )
        )
        self.valves.initialize(valves._())
        self.pumps.home(
            pumps.PumpIndexes(pumps=[pumps.PumpIndex(value=i + 1) for i in range(11)])
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

    def dispense(self, volume_per_line: ReagentVolumeWells, max_vol=None):
        print("Dispensing ", volume_per_line, "uL")

        dispense_plan = create_dispense_plan(
            volume_per_line, ReagentToFluidicLineIndexMapping
        )

        volume = [volume for reagent, (volume, _) in volume_per_line.items()][0]

        movement_axis = Axis.y
        are_rows_ascending = False
        are_columns_ascending = False

        for alignment, direction in DefaultDispenseTrips:
            abstract_routine = create_abstract_routine(
                dispense_plan=dispense_plan,
                alignment=alignment,
                geometry=DefaultGeometry,
                direction=direction,
                line_configurations=LineConfigurations,
            )

            routine = project_routine_to_axes(
                abstract_routine,
                geometry=DefaultGeometry,
                axis=movement_axis,
                are_rows_ascending=are_rows_ascending,
                are_columns_ascending=are_columns_ascending,
            )

            range = get_movement_range_coordinates(
                alignment=alignment,
                geometry=DefaultGeometry,
                routine=routine,
                margin=DispenseMovementMargin,
                movement_axis=movement_axis,
                are_rows_ascending=are_rows_ascending,
                are_columns_ascending=are_columns_ascending,
            )
            if range is None:
                continue

            start, end = range
            pump_ranges = get_pump_start_stop_positions(
                routine=routine,
                pump_start_stop_margin_mm=PumpStartMargin,
                fluidic_line_to_pump_mapping=FluidicLineIndexToPumpIndexMapping,
            )

            firstPumpIndex = min(pump_ranges.keys())

            gantry_dispense_speed = get_gantry_dispense_movement_speed(
                dispense_volume=volume,
                inter_nozzle_in_movement_distance=DefaultGeometry.x_inter_nozzle_spacing_wells_in_line
                * DefaultGeometry.inter_well_spacing_mm,
                pump_speed=PumpDynamicsMapping[firstPumpIndex].speed,
            )
            volume_usage = estimate_volume_usage(
                pump_ranges=pump_ranges,
                gantry_dispense_movement_speed=gantry_dispense_speed,
                pump_speeds={
                    pumpIndex: PumpDynamicsMapping[pumpIndex].speed
                    for pumpIndex in pump_ranges.keys()
                },
            )

            volume_margin = 0.1
            end_volume_marks = {
                pumpIndex: max(PumpMaxVolume - (volume * (1 + volume_margin)), 0.0)
                for pumpIndex, volume in volume_usage.items()
            }

            pump_indexes = [pumpIndex for pumpIndex in pump_ranges.keys()]

            # setup
            self.valves.setRoutine(routine)
            self.refill_pumps(pump_indexes)
            self.move_to(start)

            # dispense
            self.valves.startRoutine(valves._())
            self.start_pump_moves(end_volume_marks)
            self.move_to(end, wait_to_finish=True, correct_slack=False)
            self.stop_pump_moves(pump_indexes)
            self.valves.stopRoutine(valves._())
        pass

    def goToWell(self, element, well, quadrant):
        print("Going to ", element, well, quadrant)
        self.gantry.moveTo()
        pass

    def move_to(
        self,
        coordinate: Coordinate,
        wait_to_finish: bool = True,
        correct_slack: bool = True,
    ):
        print("Moving to ", coordinate)

        def move():
            self.gantry.moveTo(gantry.Position(x=coordinate.x, y=coordinate.y))

        move()
        if wait_to_finish:
            self.wait_for_movement_to_finish()
        if correct_slack:
            move()

    def wait_for_movement_to_finish(self):
        while True:
            status = self.gantry.getStatus(gantry._())
            if not status.isBusy:
                break
            time.sleep(0.01)

    def refill_pumps(self, pumps_: list[PumpIndex]):
        print("Refilling pumps ", pumps_)

        def get_pump_moves(volume: float):
            return pumps.PumpMoves(
                pumps=[
                    pumps.PumpMoves.PumpMove(
                        index=pumps.PumpIndex(value=index + 1),
                        volumeMark=volume,
                    )
                    for index in pumps_
                ]
            )

        self.pumps.moveTo(get_pump_moves(PumpMaxVolume + PumpSlack))
        self._wait_for_pump_moves_to_finish(pumps_)
        self.pumps.moveTo(get_pump_moves(PumpMaxVolume))
        self._wait_for_pump_moves_to_finish(pumps_)

    def _wait_for_pump_moves_to_finish(self, pump_indexes: list[PumpIndex]):
        while True:
            status: pumps.Statuses = self.pumps.getStatuses(
                pumps.PumpIndexes(
                    pumps=[pumps.PumpIndex(value=index + 1) for index in pump_indexes]
                )
            )
            if all(not pump.isBusy for pump in status.pumps):
                break
            time.sleep(0.01)

    def start_pump_moves(self, end_volume_marks: dict[PumpIndex, float]):
        moves = pumps.PumpMoves(
            pumps=[
                pumps.PumpMoves.PumpMove(
                    index=pumps.PumpIndex(value=index + 1), volumeMark=volume
                )
                for index, volume in end_volume_marks.items()
            ]
        )
        self.pumps.moveTo(moves)

    def stop_pump_moves(self, pump_indexes: list[PumpIndex]):
        self.pumps.stop(
            pumps.PumpIndexes(
                pumps=[pumps.PumpIndex(value=index + 1) for index in pump_indexes]
            )
        )
