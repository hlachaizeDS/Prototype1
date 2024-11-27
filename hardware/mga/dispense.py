import mga_testbench_interface.generated.valves_pb2 as valves
from dataclasses import dataclass
import numpy as np

Row = int  # starts from 0
Line = int  # starts from 0
NozzleIndex = int  # starts from 0
Direction = valves.Routine.Direction
ValveState = valves.State.ValveState
Routine = valves.Routine


@dataclass
class Well:
    row: int
    column: int


@dataclass
class Geometry:
    reference_position = 0.0  # position at which 1.1 is centered over G1
    inter_well_spacing = 4.5  # distance between two wells
    number_of_lines_in_manifold = 6
    number_of_manifolds = 2
    inter_line_spacing_wells = 2
    x_inter_nozzle_spacing_wells_in_line = 1 / 4
    y_inter_nozzle_spacing_wells_in_line = 2
    number_of_nozzles_per_line = 4
    number_of_rows = 16
    number_of_columns = 24


@dataclass
class LineConfiguration:
    open_distance: float
    open_offset: float
    close_offset: float


@dataclass
class Alignment:
    line: Line
    nozzle_index: NozzleIndex
    row: Row


def multi_dispense_map_to_routine(
    volumes: dict[Line, list[Well]],
    alignment: Alignment,
    direction: Direction,
    geometry: Geometry,
    line_configurations: dict[Line, LineConfiguration],
):
    routine = Routine(direction=direction)

    max_column = max(well.column for _, wells in volumes.items() for well in wells)
    min_line = min(line for line, _ in volumes.items())

    # row on which line 0 nozzle 0 is aligned
    manifold_index = alignment.line // geometry.number_of_lines_in_manifold
    if manifold_index >= geometry.number_of_manifolds:
        raise ValueError("Manifold index out of bounds")

    base_row = (
        alignment.row
        + (
            alignment.nozzle_index
            + manifold_index * geometry.number_of_nozzles_per_line
        )
        * geometry.y_inter_nozzle_spacing_wells_in_line
    )
    # print(f"base_row: {base_row}")

    dispensed_wells: dict[Line, list[Well]] = {line: [] for line in volumes.keys()}

    max_step = (
        max_column
        + geometry.number_of_lines_in_manifold
        + geometry.inter_line_spacing_wells
        - min_line
    )

    start = 0 if direction == Direction.forward else max_step
    stop = max_step if direction == Direction.forward else 0
    step_change = (
        (1 if direction == Direction.forward else -1)
        * 1
        / geometry.number_of_nozzles_per_line
    )

    for step in np.arange(
        start,
        stop,
        step_change,
    ):
        for line, wells in volumes.items():
            valve_identifier: valves.State.ValveIdentifier | None = None
            manifold_row_offset = (
                (line // geometry.number_of_lines_in_manifold)
                * geometry.number_of_nozzles_per_line
                * geometry.y_inter_nozzle_spacing_wells_in_line
            )
            for nozzle_index in range(0, geometry.number_of_nozzles_per_line):
                nozzle_row = (
                    base_row
                    - manifold_row_offset
                    - nozzle_index * geometry.y_inter_nozzle_spacing_wells_in_line
                )
                nozzle_column: float = (
                    step
                    - (line % geometry.number_of_lines_in_manifold) * geometry.inter_line_spacing_wells
                    - nozzle_index * geometry.x_inter_nozzle_spacing_wells_in_line
                )
                if (
                    nozzle_column < 0
                    or nozzle_column >= geometry.number_of_columns
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

            open_position, close_position = get_open_close_positions(
                direction, geometry, step, line_configurations[line]
            )

            for position in [open_position, close_position]:
                state = (
                    valves.State.ValveState.open
                    if position == open_position
                    else valves.State.ValveState.closed
                )
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
                    state=state,
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
    return complete_routine(routine, geometry)


def complete_routine(routine: valves.Routine, geometry: Geometry):
    for item in routine.positionThresholdToStateMapping:
        for line in range(1, geometry.number_of_lines_in_manifold + 1):

            def lineValves():
                return [
                    valve
                    for valve in item.state.valves
                    if valve.identifier.fluidicLine == line
                ]

            if len(lineValves()) == 0:
                continue
            # check exactly one valve is open
            valve_open = len(
                [
                    valve
                    for valve in lineValves()
                    if valve.state == valves.State.ValveState.open
                ]
            )
            if valve_open > 1:
                raise ValueError(f"More than one valve open in a line {line}")

            if valve_open == 0:
                item.state.valves.append(
                    valves.State.Valve(
                        identifier=valves.State.ValveIdentifier(
                            type=valves.State.ValveIdentifier.Type.discharge,
                            fluidicLine=line,
                            id=0,  # discharge id
                        ),
                        state=valves.State.ValveState.open,
                    )
                )

            missing_valve_indexes = [
                index
                for index in range(0, geometry.number_of_nozzles_per_line + 1)
                if index not in [valve.identifier.id for valve in lineValves()]
            ]

            for missing_valve_index in missing_valve_indexes:
                item.state.valves.append(
                    valves.State.Valve(
                        identifier=valves.State.ValveIdentifier(
                            type=valves.State.ValveIdentifier.Type.discharge
                            if missing_valve_index == 0
                            else valves.State.ValveIdentifier.Type.dispense,
                            fluidicLine=line,
                            id=missing_valve_index,  # discharge id
                        ),
                        state=valves.State.ValveState.closed,
                    )
                )
            item.state.valves.sort(
                key=lambda valve: (valve.identifier.fluidicLine, valve.identifier.id)
            )
    return routine


def get_open_close_positions(
    direction: Direction,
    geometry: Geometry,
    step: float,
    line_configurations: LineConfiguration,
):
    sign = 1 if direction == Direction.forward else -1
    open_position = (
        geometry.reference_position
        + step * geometry.inter_well_spacing
        - sign * (line_configurations.open_distance / 2)
        - sign * line_configurations.open_offset
    )
    close_position = (
        geometry.reference_position
        + step * geometry.inter_well_spacing
        + sign * (line_configurations.open_distance / 2)
        - sign * line_configurations.close_offset
    )
    return (open_position, close_position)
