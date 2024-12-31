from hardware.common.arduinoControl import ArduinoControl, MockArduinoControl
from tkinter import Frame
import grpc
import mga_testbench_interface.generated.gantry_pb2_grpc as gantry_grpc
import mga_testbench_interface.generated.gantry_pb2 as gantry
import mga_testbench_interface.generated.valves_pb2_grpc as valves_grpc
import mga_testbench_interface.generated.valves_pb2 as valves
import mga_testbench_interface.generated.pumps_pb2_grpc as pumps_grpc
import mga_testbench_interface.generated.pumps_pb2 as pumps
import time
from hardware.mga.test.utils import create_geogram

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
    LineIndex,
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
from hardware.mga.types import Coordinate, PumpIndex, Volume
from hardware.mga.fluidics import (
    estimate_volume_usage,
    get_pump_start_stop_positions,
    PumpStartMargin,
)

class MGATestbenchHardware(Frame):
    def __init__(self, parent, mock_components=True):
        self.mock_components = mock_components
        self.parent = parent

        self.thermalCam = 0  # Will impact rightFrame in guitab1

        if self.mock_components:
            self.arduinoControl = MockArduinoControl(self)
        else:
            self.arduinoControl = ArduinoControl(self)

        self.channel = (
            grpc.secure_channel("localhost:7051", grpc.local_channel_credentials())
            # if not self.mock_components
            # else grpc.insecure_channel("localhost:7050")
        )
        self.gantry = gantry_grpc.GantryStub(self.channel)
        self.valves = valves_grpc.ValvesStub(self.channel)
        self.pumps = pumps_grpc.PumpsStub(self.channel)

    def initialisation(self):
        if self.parent:
            self.parent.directCommand.initialisationLed.configure(bg="red")
        if self.arduinoControl:
            self.arduinoControl.close_vac()
            self.arduinoControl.stopShaking()

        self.set_gantry_parameters()
        self.gantry.home(gantry._())
        self.valves.initialize(valves._())
        self.pumps.home(
            pumps.PumpIndexes(pumps=[pumps.PumpIndex(value=i + 1) for i in range(11)])
        )
        self._wait_for_pump_moves_to_finish([i for i in range(11)])
        # if not self.mock_components:
        #     # wait for home to finish
        time.sleep(10)
        if self.parent:
            self.parent.directCommand.initialisationLed.configure(bg="green")

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

    def dispense(self, volume_per_line: ReagentVolumeWells):
        print("Dispensing ", volume_per_line, "uL")

        dispense_plan = create_dispense_plan(
            volume_per_line, ReagentToFluidicLineIndexMapping
        )

        volume = [volume for reagent, (volume, _) in volume_per_line.items()][0]

        movement_axis = Axis.y
        are_rows_ascending = True
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
            print("Range: ", range)
            if range is None:
                continue
            print(create_geogram(routine))

            start, end = range
            pump_ranges, line_indexes = get_pump_start_stop_positions(
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
            print(
                "Dispense axis speed",
                gantry_dispense_speed,
                "mm/s, volume",
                volume,
                "uL",
            )
            volume_usage = estimate_volume_usage(
                pump_ranges=pump_ranges,
                gantry_dispense_movement_speed=gantry_dispense_speed,
                pump_speeds={
                    pump_index: PumpDynamicsMapping[pump_index].speed
                    for pump_index in pump_ranges.keys()
                },
            )

            pump_indexes = [pump_index for pump_index in pump_ranges.keys()]

            # print("Range", range)

            # setup
            self.valves.setRoutine(routine)
            self.move_to(start)
            self.set_gantry_parameters(
                axis=movement_axis, gantry_dispense_speed=gantry_dispense_speed
            )

            pump_remaining_volumes = self.get_remaining_volumes_in_pumps(pump_indexes)

            print("Volume usage: ", volume_usage)
            print("Pump remaining volumes: ", pump_remaining_volumes)
            pumps_requiring_refill = [
                pump_index
                for pump_index, volume in pump_remaining_volumes.items()
                if pump_index in volume_usage and volume < volume_usage[pump_index]
            ]
            print("Pumps requiring refill: ", pumps_requiring_refill)
            if len(pumps_requiring_refill) > 0:
                self.set_aspiration_valves(line_indexes, valves.State.ValveState.open)
                pump_indexes = self.refill_pumps(pumps_requiring_refill)
                self._wait_for_pump_moves_to_finish(pumps_requiring_refill)
                self.set_aspiration_valves(line_indexes, valves.State.ValveState.closed)

            pump_remaining_volumes = self.get_remaining_volumes_in_pumps(pump_indexes)

            volume_margin = 0.0
            end_volume_marks = {
                pump_index: max(
                    pump_remaining_volumes[pump_index]
                    - (volume * (1 + volume_margin)),
                    0.0,
                )
                for pump_index, volume in volume_usage.items()
            }
            print("move pumps to marks", end_volume_marks)

            # dispense
            self.valves.startRoutine(valves._())
            self.start_pump_moves(end_volume_marks)
            self.move_to(end, wait_to_finish=True, correct_slack=False)
            self.stop_pump_moves(pump_indexes)
            self.valves.stopRoutine(valves._())
        pass

    def set_gantry_parameters(
        self, axis: Axis | None = None, gantry_dispense_speed: float | None = None
    ):
        parameters = DefaultGantryParameters
        if axis and gantry_dispense_speed:
            parameters.axes[axis].speed = gantry_dispense_speed
        x = parameters.axes[Axis.x]
        y = parameters.axes[Axis.y]
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
            self.wait_for_movement_to_finish()

    def wait_for_movement_to_finish(self):
        while True:
            time.sleep(0.1)
            status = self.gantry.getStatus(gantry._())
            if not status.isBusy:
                break

    def refill_pumps(self, pumps_):
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
        # self.set_aspiration_valves(lines, valves.State.ValveState.open)
        return pumps_

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

    def get_remaining_volumes_in_pumps(
        self, pump_indexes: list[PumpIndex]
    ) -> dict[PumpIndex, Volume]:
        volume_marks = self.pumps.getVolumeMarks(
            pumps.PumpIndexes(
                pumps=[pumps.PumpIndex(value=index + 1) for index in pump_indexes]
            )
        )
        return {
            PumpIndex(pump.index.value - 1): pump.value for pump in volume_marks.pumps
        }

    def goToWell(self, element, well, quadrant):
        print("Going to ", element, well, quadrant)
        if element == "thermalCamera":
            coordinate = gantry.Position(x=0, y=0)
            self.gantry.moveTo(gantry.Position(x=coordinate.x, y=coordinate.y))
        pass

    def set_aspiration_valves(
        self, fluidic_lines: list[LineIndex], state: valves.State.ValveState
    ):
        valveStates = valves.State(
            valves=[
                valves.State.Valve(
                    identifier=valves.State.ValveIdentifier(
                        type=valves.State.ValveIdentifier.Type.aspiration,
                        fluidicLine=fluidic_line,
                    ),
                    state=state,
                )
                for fluidic_line in fluidic_lines
            ]
        )
        print("Valve states: ", valveStates)
        self.valves.setState(valveStates)
