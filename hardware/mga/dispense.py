import mga_testbench_interface.generated.valves_pb2 as valves
from dataclasses import dataclass
import numpy as np


@dataclass
class Well:
    row: int
    column: int


Line = int  # starts from 0
Volume = float


def multi_dispense_map_to_routine(
    reference_position: float,
    inter_well_spacing: float,
    open_interval: float,
    row: int,
    volumes: dict[Line, tuple[Volume, list[Well]]],
):
    number_of_rows = 16
    number_of_columns = 24

    routine = valves.Routine(
        direction=valves.Routine.Direction.forward
        if row % 2 == 0
        else valves.Routine.Direction.backward
    )

    max_column = max(well.column for _, (_, wells) in volumes.items() for well in wells)
    min_line = min(line for line, (_, _) in volumes.items())

    number_of_lines_x = 6
    inter_line_spacing_wells = 1
    x_inter_nozzle_spacing_wells_in_line = 1 / 4
    y_inter_nozzle_spacing_wells_in_line = 2
    number_of_nozzles_per_line = 4
    dispensed_wells: dict[Line, list[Well]] = {line: [] for line in volumes.keys()}

    for step in np.arange(
        0,
        (max_column + number_of_lines_x + inter_line_spacing_wells - min_line),
        1 / number_of_nozzles_per_line,
    ):
        for line, (volume, wells) in volumes.items():
            if volume <= 0:
                print(f"Volume is less than or equal to 0 in line {line+1}")
                continue
            valve_identifier: valves.State.ValveIdentifier | None = None
            for nozzle_index in range(0, number_of_nozzles_per_line):
                nozzle_row = row + nozzle_index * y_inter_nozzle_spacing_wells_in_line
                nozzle_column: float = (
                    step - line - nozzle_index * x_inter_nozzle_spacing_wells_in_line
                )
                if (
                    nozzle_column < 0
                    or nozzle_column >= number_of_rows
                    or int(nozzle_column) != nozzle_column
                ):
                    continue
                target_well = Well(
                    row=nozzle_row,
                    column=int(nozzle_column),
                )
                should_dispense = (
                    target_well in wells and target_well not in dispensed_wells[line]
                )
                if should_dispense:
                    valve_identifier = valves.State.ValveIdentifier(
                        type=valves.State.ValveIdentifier.Type.dispense,
                        fluidicLine=line + 1,
                        id=nozzle_index + 1,
                    )
                    dispensed_wells[line].append(target_well)
            if valve_identifier is None:
                continue

            for offset_index, offset in enumerate(
                [-open_interval / 2, open_interval / 2]
            ):
                position = reference_position + (step) * inter_well_spacing + offset
                itemIndexWithSameThreshold = next(
                    (
                        i
                        for i, item in enumerate(
                            routine.positionThresholdToStateMapping
                        )
                        if item.positionThreshold == position
                    ),
                    None,
                )

                valve = valves.State.Valve(
                    identifier=valve_identifier,
                    state=valves.State.ValveState.open
                    if offset_index == 0
                    else valves.State.ValveState.closed,
                )

                if itemIndexWithSameThreshold is not None:
                    routine.positionThresholdToStateMapping[
                        itemIndexWithSameThreshold
                    ].state.valves.append(valve)

                else:
                    routine.positionThresholdToStateMapping.append(
                        valves.Routine.Item(
                            positionThreshold=position,
                            state=valves.State(
                                valves=[valve],
                            ),
                        )
                    )

    return routine
