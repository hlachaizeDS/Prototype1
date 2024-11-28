from hardware.mga.dispense import (
    createRoutine,
    Well,
    Direction,
    Alignment,
    Routine,
    LineIndex,
    ValveState,
    LineConfiguration,
)
from hardware.mga.configuration import Geometry
import numpy as np
import sys
from math import isclose


def test_dispense_multi_dispense_map_to_routine_forward():
    wells: list[Well] = []
    for row in range(0, 16):
        for column in range(0, 24):
            # if column % 2 == row % 2:
            #     continue
            wells.append(Well(row, column))

    # log plate
    print()
    for row in range(0, 16):
        print("|", end="")
        for column in range(0, 24):
            print("x|" if Well(row, column) in wells else " |", end="")
        print()
    print()

    volumes = {key: wells for key in range(0, 12)}

    geometry = Geometry()

    line_configuration = LineConfiguration(open_offset=0, close_offset=0)
    line_configurations: dict[LineIndex, LineConfiguration] = {}
    for line in range(0, 12):
        line_configurations[line] = line_configuration

    def run_trips():
        trip = [
            (Alignment(line_index=0, nozzle_index=3, row=0), Direction.forward),
            (Alignment(line_index=0, nozzle_index=3, row=1), Direction.backward),
            (Alignment(line_index=0, nozzle_index=3, row=8), Direction.forward),
            (Alignment(line_index=0, nozzle_index=3, row=9), Direction.backward),
            (Alignment(line_index=6, nozzle_index=3, row=8), Direction.forward),
            (Alignment(line_index=6, nozzle_index=3, row=9), Direction.backward),
        ]

        for alignment, direction in trip:
            print(
                f"Alignment: {alignment} Direction: {'forward' if direction == Direction.forward else 'backward'}"
            )
            routine = createRoutine(
                volumes=volumes,
                alignment=alignment,
                geometry=geometry,
                direction=direction,
                line_configurations=line_configurations,
            )

            # for item in routine.positionThresholdToStateMapping:
            #     print(item.positionThreshold)
            #     for valve in item.state.valves:
            #         print(
            #             f"\t{valve.identifier.fluidicLine}.{valve.identifier.id} -> {'open' if valve.state == 0 else 'closed'}"
            #         )
            print_geogramme(routine)

    print_in_file("out.txt", run_trips)


# def test_dispense_multi_dispense_map_to_routine_backward():
#     wells: list[Well] = []
#     for row in range(8):
#         for column in range(24):
#             wells.append(Well(row, column))

#     volumes = {
#         0: wells,
#         5: wells,
#     }

#     geometry = Geometry(
#         inter_well_spacing=100,
#         reference_position=0,
#     )

#     line_configurations = {
#         0: LineConfiguration(open_distance=25, open_offset=-0, close_offset=0),
#         5: LineConfiguration(open_distance=25, open_offset=0, close_offset=0),
#     }

#     routine = multi_dispense_map_to_routine(
#         volumes=volumes,
#         row=0,
#         geometry=geometry,
#         line_configurations=line_configurations,
#         direction=-1,
#     )

#     for item in routine.positionThresholdToStateMapping:
#         print(item.positionThreshold)
#         for valve in item.state.valves:
#             print(
#                 f"\t{valve.identifier.fluidicLine}.{valve.identifier.id} -> {'open' if valve.state == 0 else 'closed'}"
#             )
#     pass


# utils


def print_in_file(file: str, function):
    orig_stdout = sys.stdout
    f = open(file, "w")
    sys.stdout = f

    function()

    sys.stdout = orig_stdout
    f.close()


def print_geogramme(routine: Routine):
    if len(routine.positionThresholdToStateMapping) == 0:
        return
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
    end = (
        max_threshold + step
        if routine.direction == Direction.forward
        else min_threshold + step
    )

    print(f"Range [{start:.4f}, {end:.4f}) Step: {step:.4f}")
    for line in lines:
        for nozzle in range(5):
            last_valve_state = ValveState.open if nozzle == 0 else ValveState.closed
            print(f"{line}.{nozzle} ", end="")
            for threshold in np.arange(start, end, step):
                for item in routine.positionThresholdToStateMapping:
                    # print(f"{item.positionThreshold} {threshold}")
                    if isclose(item.positionThreshold, threshold, abs_tol=0.01):
                        # print("equals!")
                        for valve in item.state.valves:
                            if (
                                valve.identifier.fluidicLine == line
                                and valve.identifier.id == nozzle
                            ):
                                last_valve_state = valve.state
                # print(threshold, end="")
                print("█" if last_valve_state == ValveState.open else "_", end="")
            print()
        print()
