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
from hardware.mga.test.utils import create_geogram, print_routine
import datetime
import copy

from hardware.mga.configuration import (
    DefaultGeometry,
    LineConfigurations,
    ReagentToFluidicLineIndexMapping,
    FluidicLineIndexToPumpIndexMapping,
    Axis,
    DefaultPumpDynamicsMapping,
    PumpMaxVolume,
    PumpSlack,
    DefaultGantryParameters,
    LineIndex,
    GantryDispenseMovementSpeed,
)
from hardware.mga.dispense import (
    create_dispense_plan,
    ReagentVolumeWells,
    create_trips,
    Trip,
)
from hardware.mga.movement import (
    get_gantry_dispense_movement_speed,
)
from hardware.mga.types import Coordinate, PumpIndex, Volume, ValveStates, ValveState
from hardware.mga.fluidics import (
    estimate_volume_usage,
    get_pump_dispense_axis_start_stop_positions,
    PumpStartMargin,
    Volumes,
    get_pump_speed,
    get_valve_states_for_aspiration,
)


class MGATestbenchHardware(Frame):
    def __init__(self, parent, mock_components=False, on_machine=True):
        self.mock_components = mock_components
        self.parent = parent

        self.thermalCam = 1  # Will impact rightFrame in guitab1

        if self.mock_components:
            self.arduinoControl = MockArduinoControl(self)
        else:
            self.arduinoControl = ArduinoControl(self)

        self.channel = (
            grpc.secure_channel("localhost:7051", grpc.local_channel_credentials())
            if on_machine
            else grpc.insecure_channel("localhost:7050")
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
        # pump_indexes = [i for i in range(0, 8)]
        pump_indexes = set(
            [pump_index for _, pump_index in FluidicLineIndexToPumpIndexMapping.items()]
        )
        print("Home pumps ", pump_indexes)
        self.pumps.home(
            pumps.PumpIndexes(pumps=[pumps.PumpIndex(value=i) for i in pump_indexes])
        )
        self.move_to(Coordinate(0, 0))
        self.wait_for_movement_to_finish()
        # self.start_pump_moves({pump_index: 0 for pump_index in pump_indexes})
        self._wait_for_pump_home_to_finish([pump for pump in pump_indexes])
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
        print(datetime.datetime.now())
        dispense_plan = create_dispense_plan(
            volume_per_line, ReagentToFluidicLineIndexMapping
        )

        movement_axis = Axis.y
        volume = [volume for _, (volume, _) in volume_per_line.items()][0]

        trips = create_trips(
            geometry=DefaultGeometry,
            dispense_plan=dispense_plan,
            movement_axis=movement_axis,
            line_configurations=LineConfigurations,
            fluidic_line_to_pump_mapping=FluidicLineIndexToPumpIndexMapping,
        )
        for trip_index, (routine, movement_range) in enumerate(trips):
            gantry_dispense_movement_speed = GantryDispenseMovementSpeed

            current_trip_volume_usage, total_upcoming_volume_usage, line_indexes = (
                self._get_volume_usage_and_line_indexes_for_remaining_trips(
                    volume=volume,
                    trips=trips[trip_index:],
                )
            )

            self._print_trip_debug_info(
                routine=routine,
                movement_range=movement_range,
                gantry_dispense_speed=gantry_dispense_movement_speed,
                volume=volume,
                volume_usage=total_upcoming_volume_usage,
            )

            # refill if needed
            end_volume_marks = self._refill_and_get_end_volume_marks(
                current_trip_volume_usage=current_trip_volume_usage,
                total_upcoming_volume_usage=total_upcoming_volume_usage,
                line_indexes=line_indexes,
            )

            # set routine and gantry parameters
            self.valves.setRoutine(routine)
            movement_start, movement_end = movement_range

            self.move_to(movement_start)
            self._set_gantry_and_pump_speeds_for_dispense(
                volume=volume,
                movement_axis=movement_axis,
                gantry_dispense_movement_speed=gantry_dispense_movement_speed,
                end_volume_marks=end_volume_marks,
            )

            # dispense
            self.valves.startRoutine(valves._())
            self.start_pump_moves(end_volume_marks)
            self.move_to(movement_end, wait_to_finish=True, correct_slack=False)
            self.stop_pump_moves([pumpIndex for pumpIndex in end_volume_marks.keys()])
            self.valves.stopRoutine(valves._())
            self.set_gantry_parameters()
        print(datetime.datetime.now())

    def set_gantry_parameters(
        self, axis: Axis | None = None, gantry_dispense_speed: float | None = None
    ):
        parameters = copy.deepcopy(DefaultGantryParameters)
        if axis and gantry_dispense_speed:
            parameters.axes[axis].speed = gantry_dispense_speed
        x = parameters.axes[Axis.x]
        y = parameters.axes[Axis.y]
        axis_parameters = gantry.AxisParameters(
            axes=[
                gantry.AxisParameters.AxisInnerParameters(
                    axis=gantry.Axis.x,
                    speed=x.speed,
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
        # print(axis_parameters)
        self.gantry.setParameters(axis_parameters)

    def get_gantry_speed(self, axis: Axis):
        parameters: gantry.AxisParameters = self.gantry.getParameters(gantry._())
        protoAxis = gantry.Axis.x if axis == Axis.x else gantry.Axis.y
        axisParameters = next((x for x in parameters.axes if x.axis == protoAxis), None)
        if not axisParameters:
            return None
        return axisParameters.speed

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
            # print("gantry", status)
            if not status.isBusy:
                break

    def refill_pumps(self, pumps_):
        print("Refilling pumps ", pumps_)

        def get_pump_moves(volume: float):
            return pumps.PumpMoves(
                pumps=[
                    pumps.PumpMoves.PumpMove(
                        index=pumps.PumpIndex(value=index),
                        volumeMark=volume,
                    )
                    for index in pumps_
                ]
            )

        self.pumps.moveTo(get_pump_moves(PumpMaxVolume + PumpSlack))
        self._wait_for_pump_moves_to_finish(pumps_)
        self.pumps.moveTo(get_pump_moves(PumpMaxVolume))
        self._wait_for_pump_moves_to_finish(pumps_)
        # self.set_aspiration_valves(lines, ValveState.open)
        return pumps_

    def _set_pump_speeds(self, pump_speeds: dict[PumpIndex, float]):
        print("Setting pump speeds: ", pump_speeds)
        self.pumps.setParameters(
            pumps.PumpParameters(
                pumps=[
                    pumps.PumpParameters.PumpInnerParameters(
                        index=pumps.PumpIndex(value=index),
                        speed=speed,
                        acceleration=DefaultPumpDynamicsMapping[index].acceleration,
                        deceleration=DefaultPumpDynamicsMapping[index].deceleration,
                    )
                    for index, speed in pump_speeds.items()
                ]
            )
        )

    def _set_gantry_and_pump_speeds_for_dispense(
        self,
        volume: Volume,
        movement_axis: Axis,
        gantry_dispense_movement_speed: float,
        end_volume_marks: Volumes,
    ):
        self.set_gantry_parameters(
            axis=movement_axis, gantry_dispense_speed=gantry_dispense_movement_speed
        )
        output_movement_axis_speed = self.get_gantry_speed(movement_axis)
        if output_movement_axis_speed is not None:
            print("Precise dispense movement speed: ", output_movement_axis_speed)
            pump_speeds = {
                pump_index: get_pump_speed(
                    dispense_volume=volume,
                    gantry_speed=output_movement_axis_speed,
                    inter_nozzle_in_movement_distance=DefaultGeometry.x_inter_nozzle_spacing_wells_in_line
                    * DefaultGeometry.inter_well_spacing_mm,
                )
                for pump_index in end_volume_marks.keys()
            }
            self._set_pump_speeds(pump_speeds)

    def _wait_for_pump_home_to_finish(self, pump_indexes: list[PumpIndex]):
        while True:
            status: pumps.Statuses = self.pumps.getStatuses(
                pumps.PumpIndexes(
                    pumps=[pumps.PumpIndex(value=index) for index in pump_indexes]
                )
            )
            initialized = [pump.initialized for pump in status.pumps]
            # print(initialized)
            if all(initialized):
                break
            time.sleep(0.1)

    def _wait_for_pump_moves_to_finish(self, pump_indexes: list[PumpIndex]):
        while True:
            status: pumps.Statuses = self.pumps.getStatuses(
                pumps.PumpIndexes(
                    pumps=[pumps.PumpIndex(value=index) for index in pump_indexes]
                )
            )
            busy = [pump.isBusy for pump in status.pumps]
            # print("pumps busy", busy)
            if not any(busy):
                break
            time.sleep(0.1)

    def start_pump_moves(self, end_volume_marks: dict[PumpIndex, float]):
        moves = pumps.PumpMoves(
            pumps=[
                pumps.PumpMoves.PumpMove(
                    index=pumps.PumpIndex(value=index), volumeMark=volume
                )
                for index, volume in end_volume_marks.items()
            ]
        )
        self.pumps.moveTo(moves)

    def stop_pump_moves(self, pump_indexes: list[PumpIndex]):
        self.pumps.stop(
            pumps.PumpIndexes(
                pumps=[pumps.PumpIndex(value=index) for index in pump_indexes]
            )
        )

    def get_remaining_volumes_in_pumps(self, pump_indexes: list[PumpIndex]) -> Volumes:
        volume_marks = self.pumps.getVolumeMarks(
            pumps.PumpIndexes(
                pumps=[pumps.PumpIndex(value=index) for index in pump_indexes]
            )
        )
        return {PumpIndex(pump.index.value): pump.value for pump in volume_marks.pumps}

    def goToWell(self, element, well, quadrant):
        print("Going to ", element, well, quadrant)
        if element == "thermalCamera":
            self.move_to(Coordinate(0, 0))
        pass

    def set_valves(self, states: ValveStates):
        valveStates = valves.State(
            valves=[
                valves.State.Valve(
                    identifier=valves.State.ValveIdentifier(
                        type=valve.type,
                        fluidicLine=fluidic_line,
                        id=valve.id,
                    ),
                    state=state,
                )
                for fluidic_line in states.keys()
                for valve, state in states[fluidic_line].items()
            ]
        )
        # print("Valve states: ", valveStates)
        self.valves.setState(valveStates)

    def _refill_and_get_end_volume_marks(
        self,
        current_trip_volume_usage: Volumes,
        total_upcoming_volume_usage: Volumes,
        line_indexes: list[LineIndex],
    ):
        pump_indexes = [pump_index for pump_index in total_upcoming_volume_usage.keys()]
        pump_remaining_volumes = self.get_remaining_volumes_in_pumps(pump_indexes)
        # print("Volume usage: ", volume_usage)
        print("Pump remaining volumes: ", pump_remaining_volumes)
        pumps_requiring_refill = [
            pump_index
            for pump_index, volume in pump_remaining_volumes.items()
            if pump_index in total_upcoming_volume_usage
            and volume < total_upcoming_volume_usage[pump_index]
        ]
        print("Pumps requiring refill: ", pumps_requiring_refill)
        if len(pumps_requiring_refill) > 0:
            # if any pump requires a refill, use the opportunity
            # to refill all pumps in the trip
            self.set_valves(
                get_valve_states_for_aspiration(
                    line_indexes=line_indexes, aspiration_valve_state=ValveState.open
                )
            )
            pump_speeds = {
                pump_index: DefaultPumpDynamicsMapping[pump_index].speed
                for pump_index in pump_indexes
            }
            self._set_pump_speeds(pump_speeds)
            self.refill_pumps(pump_indexes)
            self._wait_for_pump_moves_to_finish(pump_indexes)
            self.set_valves(
                get_valve_states_for_aspiration(
                    line_indexes=line_indexes, aspiration_valve_state=ValveState.closed
                )
            )

        pump_remaining_volumes = self.get_remaining_volumes_in_pumps(pump_indexes)
        print("Pump remaining volumes: ", pump_remaining_volumes)

        volume_margin = 0.0
        end_volume_marks = {
            pump_index: max(
                pump_remaining_volumes[pump_index] - (volume * (1 + volume_margin)),
                0.0,
            )
            for pump_index, volume in current_trip_volume_usage.items()
        }
        print("move pumps to marks", end_volume_marks)
        return end_volume_marks

    def _get_volume_usage_and_line_indexes_for_remaining_trips(
        self, volume: Volume, trips: list[Trip]
    ) -> tuple[Volumes, Volumes, list[LineIndex]]:
        current_trip_volume_usage = {}
        total_volume_usage = {}
        all_line_indexes: set[LineIndex] = set()
        for index, (routine, _) in enumerate(trips):
            gantry_dispense_movement_speed = get_gantry_dispense_movement_speed(
                dispense_volume=volume,
                inter_nozzle_in_movement_distance=DefaultGeometry.x_inter_nozzle_spacing_wells_in_line
                * DefaultGeometry.inter_well_spacing_mm,
                pump_speed=DefaultPumpDynamicsMapping[1].speed,
            )
            pump_dispense_axis_ranges, line_indexes = (
                get_pump_dispense_axis_start_stop_positions(
                    routine=routine,
                    pump_start_stop_margin_mm=PumpStartMargin,
                    fluidic_line_to_pump_mapping=FluidicLineIndexToPumpIndexMapping,
                )
            )
            volume_usage = estimate_volume_usage(
                pump_dispense_axis_ranges=pump_dispense_axis_ranges,
                gantry_dispense_movement_speed=gantry_dispense_movement_speed,
                pump_speeds={
                    pump_index: DefaultPumpDynamicsMapping[pump_index].speed
                    for pump_index in pump_dispense_axis_ranges.keys()
                },
            )
            if index == 0:
                current_trip_volume_usage = volume_usage
            for pump_index, estimated_volume in volume_usage.items():
                if pump_index not in total_volume_usage:
                    total_volume_usage[pump_index] = 0.0
                total_volume_usage[pump_index] += estimated_volume

            for line_index in line_indexes:
                all_line_indexes.add(line_index)

        return (
            current_trip_volume_usage,
            total_volume_usage,
            [line_index for line_index in all_line_indexes],
        )

    def _print_trip_debug_info(
        self, routine, movement_range, gantry_dispense_speed, volume, volume_usage
    ):
        print("Movement range: ", movement_range)
        print(create_geogram(routine))
        # print_routine(routine)
        print(
            "Dispense axis speed",
            gantry_dispense_speed,
            "mm/s, volume",
            volume,
            "uL",
        )
        print("Volume usage: ", volume_usage)
