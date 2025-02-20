from hardware.mga.types import (
    PumpIndex,
    Routine,
    LineIndex,
    Volume,
    ValveStates,
    ValveState,
    Valve,
    ValveType,
    MovementRange,
)

from hardware.mga.configuration import Axis
from hardware.mga.movement import get_coordinate_axis

PumpDispenseAxisRanges = dict[PumpIndex, tuple[float, float]]
Volumes = dict[PumpIndex, Volume]
PumpSpeeds = dict[PumpIndex, float]

PumpStartMargin = 0.2


def get_pump_dispense_axis_range_from_movement_range(
    routine: Routine,
    movement_range: MovementRange,
    movement_axis: Axis,
    fluidic_line_to_pump_mapping: dict[LineIndex, PumpIndex],
):
    start = get_coordinate_axis(movement_range[0], movement_axis)
    stop = get_coordinate_axis(movement_range[1], movement_axis)

    pumpRanges: PumpDispenseAxisRanges = {}
    all_line_indexes = [lineIndex for lineIndex in fluidic_line_to_pump_mapping.keys()]

    line_indexes: set[LineIndex] = set()
    for line_index in all_line_indexes:
        for item in routine.positionThresholdToStateMapping:
            lineValves = [
                valve
                for valve in item.state.valves
                if valve.identifier.fluidicLine == line_index
            ]
            if len(lineValves) == 0:
                continue
            pumpIndex = fluidic_line_to_pump_mapping[line_index]
            if pumpIndex is None:
                raise KeyError(
                    "{lineIndex} does not exist in fluidic_line_to_pump_mapping"
                )
            line_indexes.add(line_index)
            if pumpIndex not in pumpRanges:
                pumpRanges[pumpIndex] = (
                    start,
                    stop,
                )

    return pumpRanges, [lineIndex for lineIndex in line_indexes]


def get_pump_dispense_axis_range_from_routine(
    routine: Routine,
    fluidic_line_to_pump_mapping: dict[LineIndex, PumpIndex],
    pump_start_stop_margin_mm: float,
) -> tuple[PumpDispenseAxisRanges, list[LineIndex]]:
    """
    Get the pump usage in routine
    """
    all_line_indexes = [lineIndex for lineIndex in fluidic_line_to_pump_mapping.keys()]

    pumpRanges: PumpDispenseAxisRanges = {}

    direction = routine.direction
    first = min if direction == Routine.Direction.forward else max
    last = max if direction == Routine.Direction.forward else min
    sign = 1 if direction == Routine.Direction.forward else -1

    line_indexes: set[LineIndex] = set()
    for lineIndex in all_line_indexes:
        for item in routine.positionThresholdToStateMapping:
            lineValves = [
                valve
                for valve in item.state.valves
                if valve.identifier.fluidicLine == lineIndex
            ]
            if len(lineValves) == 0:
                continue
            pumpIndex = fluidic_line_to_pump_mapping[lineIndex]
            if pumpIndex is None:
                raise KeyError(
                    "{lineIndex} does not exist in fluidic_line_to_pump_mapping"
                )
            line_indexes.add(lineIndex)
            if pumpIndex not in pumpRanges:
                pumpRanges[pumpIndex] = (
                    item.positionThreshold - sign * pump_start_stop_margin_mm,
                    item.positionThreshold + sign * pump_start_stop_margin_mm,
                )
            else:
                start, stop = pumpRanges[pumpIndex]
                pumpRanges[pumpIndex] = (
                    first(
                        start, item.positionThreshold - sign * pump_start_stop_margin_mm
                    ),
                    last(
                        stop, item.positionThreshold + sign * pump_start_stop_margin_mm
                    ),
                )
    return pumpRanges, [lineIndex for lineIndex in line_indexes]


def estimate_volume_usage(
    pump_dispense_axis_ranges: PumpDispenseAxisRanges,
    pump_speeds: dict[PumpIndex, float],
    gantry_dispense_movement_speed,
) -> Volumes:
    volumeUsage = Volumes()
    for pumpIndex, (start, stop) in pump_dispense_axis_ranges.items():
        volumeUsage[pumpIndex] = Volume(
            abs(stop - start) / gantry_dispense_movement_speed * pump_speeds[pumpIndex]
        )
    return volumeUsage


def get_pump_speed(
    dispense_volume: float,
    gantry_speed: float,
    inter_nozzle_in_movement_distance: float,
):
    return dispense_volume * (gantry_speed / inter_nozzle_in_movement_distance)


def get_valve_states_for_aspiration(
    line_indexes: list[LineIndex],
    aspiration_valve_state: ValveState,
) -> ValveStates:
    return {
        lineIndex: {
            Valve(
                type=ValveType.aspiration, fluidicLine=lineIndex
            ): aspiration_valve_state,
            Valve(type=ValveType.discharge, fluidicLine=lineIndex): ValveState.open
            if aspiration_valve_state == ValveState.closed
            else ValveState.closed,
            **{
                Valve(
                    type=ValveType.dispense, fluidicLine=lineIndex, id=id
                ): ValveState.closed
                for id in range(1, 5)
            },
        }
        for lineIndex in line_indexes
    }
