from hardware.mga.types import PumpIndex, Routine, LineIndex, Volume
from hardware.mga.dispense import DispensePlan
from hardware.mga.configuration import ReagentToLineMapping, LineToPumpMapping

PumpDispenseAxisRanges = dict[PumpIndex, tuple[float, float]]

PumpStartMargin = 0.2


def get_pump_dispense_axis_start_stop_positions(
    routine: Routine,
    fluidic_line_to_pump_mapping: dict[LineIndex, PumpIndex],
    pump_start_stop_margin_mm: float,
) -> tuple[PumpDispenseAxisRanges, list[LineIndex]]:
    """
    Get the pump usage in routine
    """
    lineIndexes = [lineIndex for lineIndex in fluidic_line_to_pump_mapping.keys()]

    pumpRanges: PumpDispenseAxisRanges = {}

    direction = routine.direction
    first = min if direction == Routine.Direction.forward else max
    last = max if direction == Routine.Direction.forward else min
    sign = 1 if direction == Routine.Direction.forward else -1

    line_indexes: set[LineIndex] = set()
    for lineIndex in lineIndexes:
        for item in routine.positionThresholdToStateMapping:
            lineValves = [
                valve
                for valve in item.state.valves
                if valve.identifier.fluidicLine == lineIndex + 1
            ]
            if len(lineValves) == 0:
                continue
            pumpIndex = fluidic_line_to_pump_mapping[lineIndex]
            if pumpIndex is None:
                raise KeyError("{lineIndex} does not exist in fluidic_line_to_pump_mapping")
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


VolumeUsage = dict[PumpIndex, Volume]


def estimate_volume_usage(
    pump_dispense_axis_ranges: PumpDispenseAxisRanges,
    pump_speeds: dict[PumpIndex, float],
    gantry_dispense_movement_speed,
) -> VolumeUsage:
    volumeUsage = VolumeUsage()
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
