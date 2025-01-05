from hardware.mga.types import (
    Direction,
    Routine,
    Well,
    LineIndex,
    ValveState,
)
import numpy as np
import math

def create_geogram(routine: Routine) -> str:
    if len(routine.positionThresholdToStateMapping) == 0:
        return ""
    # get all lines
    lines: set[LineIndex] = set()
    for item in routine.positionThresholdToStateMapping:
        for valve in item.state.valves:
            lines.add(valve.identifier.fluidicLine)

    # find minimum distance between to consecutive thresholds
    step: float = np.inf
    for i in range(1, len(routine.positionThresholdToStateMapping)):
        step = min(
            step,
            abs(
                routine.positionThresholdToStateMapping[i].positionThreshold
                - routine.positionThresholdToStateMapping[i - 1].positionThreshold
            ),
        )

    step = step * (1 if routine.direction == Direction.forward else -1)
    if step == 0:
        raise ValueError("Step is 0")

    min_threshold = min(
        [item.positionThreshold for item in routine.positionThresholdToStateMapping]
    )
    max_threshold = max(
        [item.positionThreshold for item in routine.positionThresholdToStateMapping]
    )

    start = min_threshold if routine.direction == Direction.forward else max_threshold
    end = max_threshold if routine.direction == Direction.forward else min_threshold

    output = ""
    for line in [line for line in sorted(lines)]:
        for nozzle in range(5):
            last_valve_state = ValveState.open if nozzle == 0 else ValveState.closed
            output += f"{line:2.0f}.{nozzle} "
            for threshold in np.arange(start, end, step):
                for item in routine.positionThresholdToStateMapping:
                    if math.isclose(item.positionThreshold, threshold, abs_tol=0.001):
                        # print("equals!")
                        for valve in item.state.valves:
                            if (
                                valve.identifier.fluidicLine == line
                                and valve.identifier.id == nozzle
                            ):
                                last_valve_state = valve.state
                output += "█" if last_valve_state == ValveState.open else "_"
            output += "\n"
    return output


def print_wells(wells: list[Well]):
    print()
    for row in range(1, 17):
        print("|", end="")
        for column in range(1, 25):
            print("x|" if Well(row=row, column=column) in wells else " |", end="")
        print()
    print()


def print_routine(routine: Routine):
    for item in routine.positionThresholdToStateMapping:
        print(item.positionThreshold)
        for valve in item.state.valves:
            print(
                f"\t{valve.identifier.fluidicLine}.{valve.identifier.id} -> {'open' if valve.state == 0 else 'closed'}"
            )
