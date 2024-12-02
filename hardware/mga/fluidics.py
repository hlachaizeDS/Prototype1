from hardware.mga.types import PumpIndex, Routine, LineIndex


def get_pump_start_stop_positions(
    routine: Routine,
    fluidic_line_to_pump_mapping: dict[LineIndex, PumpIndex],
    pump_start_stop_margin_mm: float,
) -> dict[PumpIndex, tuple[float, float]]:
    """
    Get the pump usage in routine
    """
    lineIndexes = [lineIndex for lineIndex in fluidic_line_to_pump_mapping.keys()]

    pumpPositions: dict[PumpIndex, tuple[float, float]] = {}

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
            if pumpIndex not in pumpPositions:
                pumpPositions[pumpIndex] = (
                    item.positionThreshold - sign * pump_start_stop_margin_mm,
                    item.positionThreshold + sign * pump_start_stop_margin_mm,
                )
            else:
                start, stop = pumpPositions[pumpIndex]
                pumpPositions[pumpIndex] = (
                    first(
                        start, item.positionThreshold - sign * pump_start_stop_margin_mm
                    ),
                    last(
                        stop, item.positionThreshold + sign * pump_start_stop_margin_mm
                    ),
                )
    return pumpPositions
