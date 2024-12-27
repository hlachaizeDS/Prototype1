from hardware.mga.types import PumpIndex, Routine, LineIndex, Volume

PumpRanges = dict[PumpIndex, tuple[float, float]]

PumpStartMargin = 0.2

def get_pump_start_stop_positions(
    routine: Routine,
    fluidic_line_to_pump_mapping: dict[LineIndex, PumpIndex],
    pump_start_stop_margin_mm: float,
) -> PumpRanges:
    """
    Get the pump usage in routine
    """
    lineIndexes = [lineIndex for lineIndex in fluidic_line_to_pump_mapping.keys()]

    pumpRanges: PumpRanges = {}

    direction = routine.direction
    first = min if direction == Routine.Direction.forward else max
    last = max if direction == Routine.Direction.forward else min
    sign = 1 if direction == Routine.Direction.forward else -1

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
    return pumpRanges


def estimate_volume_usage(
    pump_ranges: PumpRanges, pump_speeds: dict[PumpIndex, float], gantry_dispense_movement_speed
) -> dict[PumpIndex, Volume]:
    volumeUsage = dict[PumpIndex, Volume]()
    for pumpIndex, (start, stop) in pump_ranges.items():
        volumeUsage[pumpIndex] = Volume(
            abs(stop - start) / gantry_dispense_movement_speed * pump_speeds[pumpIndex]
        )
    return volumeUsage
