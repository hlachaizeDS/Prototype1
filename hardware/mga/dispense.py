import mga_testbench_interface.generated.valves_pb2 as valves
import numpy as np
from hardware.mga.configuration import (
    Geometry,
    ReagentToLineMapping,
)
from math import isclose
from hardware.mga.types import (
    Alignment,
    Direction,
    LineIndex,
    NozzleIndex,
    Routine,
    Well,
    DispensePlan,
    ReagentVolumeWells,
    LineConfiguration,
)
from hardware.mga.movement import find_alignment_coordinates

StandardDispenseTrips = [
    (Alignment(line_index=0, nozzle_index=3, row=0), Direction.forward),
    (Alignment(line_index=0, nozzle_index=3, row=1), Direction.backward),
    (Alignment(line_index=0, nozzle_index=3, row=8), Direction.forward),
    (Alignment(line_index=0, nozzle_index=3, row=9), Direction.backward),
    (Alignment(line_index=6, nozzle_index=3, row=8), Direction.forward),
    (Alignment(line_index=6, nozzle_index=3, row=9), Direction.backward),
]


def create_dispense_plan(
    reagent_volume_wells: ReagentVolumeWells,
    reagentToFluidicLineIndexMapping: ReagentToLineMapping,
) -> DispensePlan:
    dispense_plan: DispensePlan = {}

    volumes: set[float] = {
        volume for volume, _ in reagent_volume_wells.values() if volume != 0
    }
    if len(volumes) > 1 or (len(volumes) > 0 and volumes.pop() < 0):
        raise ValueError("All volumes must be the same and positive")

    for reagent, (_, wellIndexes) in reagent_volume_wells.items():
        lineIndex = reagentToFluidicLineIndexMapping.get(reagent)
        if lineIndex is None:
            raise ValueError(
                f"Reagent {reagent} not found in reagentToFluidicLineIndexMapping"
            )
        if len(wellIndexes) == 0:
            continue

        wells = [Well(index=wellIndex) for wellIndex in wellIndexes]
        if isinstance(lineIndex, dict):
            for direction, index in lineIndex.items():
                dispense_plan[index] = [
                    well
                    for well in wells
                    if well.row % 2 == (0 if direction == Direction.forward else 1)
                ]
        else:
            dispense_plan[lineIndex] = wells

        # print(dispense_plan)
    return dispense_plan


def create_routine(
    dispense_plan: DispensePlan,
    alignment: Alignment,
    direction: Direction,
    geometry: Geometry,
    line_configurations: dict[LineIndex, LineConfiguration],
):
    if len(dispense_plan) == 0:
        return valves.Routine()

    routine = Routine(direction=direction)

    max_column = max(
        well.column for _, wells in dispense_plan.items() for well in wells
    )
    min_line_index = min(line_index for line_index, _ in dispense_plan.items())

    dispensed_wells: dict[LineIndex, list[Well]] = {
        line_index: [] for line_index in dispense_plan.keys()
    }

    max_step = (
        max_column
        + geometry.number_of_lines_in_manifold * geometry.inter_line_spacing_wells
        - min_line_index * (1 if direction == Direction.forward else -1)
    )

    start = 0 if direction == Direction.forward else max_step
    stop = max_step if direction == Direction.forward else 0
    step_change = (
        (1 if direction == Direction.forward else -1)
        * geometry.x_inter_nozzle_spacing_wells_in_line
        / 2
    )

    base_row = __find_base_row(alignment, geometry)

    for step in np.arange(
        start - step_change,
        stop + step_change,
        step_change,
    ):
        for line_index, wells in dispense_plan.items():
            valve_identifier: valves.State.ValveIdentifier | None = None

            for nozzle_index in range(0, geometry.number_of_nozzles_per_line):
                nozzle_row, nozzle_column = __get_nozzle_row_column(
                    alignment, geometry, base_row, step, nozzle_index, line_index
                )
                if nozzle_row is None or nozzle_column is None:
                    continue

                target_well = __get_target_well(
                    wells, nozzle_row, nozzle_column, direction, geometry
                )

                if target_well is None:
                    continue

                should_dispense = target_well is not None
                if should_dispense:
                    valve_identifier = valves.State.ValveIdentifier(
                        type=valves.State.ValveIdentifier.Type.dispense,
                        fluidicLine=line_index + 1,
                        id=nozzle_index + 1,
                    )
                    dispensed_wells[line_index].append(target_well)
                    break

            if valve_identifier is None:
                continue
            __add_valve_action_to_routine(
                routine,
                alignment,
                direction,
                geometry,
                step,
                line_configurations[line_index],
                valve_identifier,
            )

    return __complete_routine(routine, geometry)


def __complete_routine(routine: valves.Routine, geometry: Geometry):
    for item in routine.positionThresholdToStateMapping:
        for line in range(
            1, geometry.number_of_lines_in_manifold * geometry.number_of_manifolds + 1
        ):

            def lineValves():
                return [
                    valve
                    for valve in item.state.valves
                    if valve.identifier.fluidicLine == line
                ]

            if len(lineValves()) == 0:
                continue

            valve_open = len(
                [
                    valve
                    for valve in lineValves()
                    if valve.state == valves.State.ValveState.open
                ]
            )
            if valve_open > 1:
                raise ValueError(f"More than one valve open in line {line}")

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


def __get_nozzle_row_column(
    alignment: Alignment,
    geometry: Geometry,
    base_row: int,
    step: float,
    nozzle_index: NozzleIndex,
    line_index: LineIndex,
):
    manifold_row_offset = (
        (line_index // geometry.number_of_lines_in_manifold)
        * geometry.number_of_nozzles_per_line
        * geometry.y_inter_nozzle_spacing_wells_in_line
    )
    nozzle_row = (
        base_row
        - manifold_row_offset
        - nozzle_index * geometry.y_inter_nozzle_spacing_wells_in_line
    )
    nozzle_column: float = (
        step
        - (line_index % geometry.number_of_lines_in_manifold)
        * geometry.inter_line_spacing_wells
        - nozzle_index * geometry.x_inter_nozzle_spacing_wells_in_line
    )
    if (
        nozzle_row < 0
        or nozzle_row >= geometry.number_of_rows
        or nozzle_column < -1
        or nozzle_column > geometry.number_of_columns + 1
    ):
        return (None, None)
    return (nozzle_row, nozzle_column)


def __get_target_well(
    wells: list[Well],
    nozzle_row: int,
    nozzle_column: float,
    direction: Direction,
    geometry: Geometry,
):
    sign = 1 if direction == Direction.forward else -1
    return next(
        (
            well
            for well in wells
            if well.row == nozzle_row
            and isclose(
                -(nozzle_column - well.column) * sign,
                geometry.x_inter_nozzle_spacing_wells_in_line / 2,
                abs_tol=0.01,
            )
        ),
        None,
    )


def __get_open_close_positions(
    direction: Direction,
    alignment: Alignment,
    geometry: Geometry,
    start_step: float,
    line_configurations: LineConfiguration,
):
    sign = 1 if direction == Direction.forward else -1
    reference = find_alignment_coordinates(geometry, alignment)
    open_position = (
        reference.x
        + (start_step) * geometry.inter_well_spacing_mm
        - sign * line_configurations.open_offset
    )
    close_position = (
        reference.x
        + (start_step + sign * geometry.x_inter_nozzle_spacing_wells_in_line)
        * geometry.inter_well_spacing_mm
        - sign * line_configurations.close_offset
    )
    return (open_position, close_position)


# row on which line 0 nozzle 0 is aligned
def __find_base_row(
    alignment: Alignment,
    geometry: Geometry,
):
    manifold_index = alignment.line_index // geometry.number_of_lines_in_manifold
    if manifold_index >= geometry.number_of_manifolds:
        raise ValueError("Manifold index out of bounds")
    return (
        alignment.row
        + (
            alignment.nozzle_index
            + manifold_index * geometry.number_of_nozzles_per_line
        )
        * geometry.y_inter_nozzle_spacing_wells_in_line
    )


def __add_valve_action_to_routine(
    routine: valves.Routine,
    alignment: Alignment,
    direction: Direction,
    geometry: Geometry,
    step: float,
    lineConfiguration: LineConfiguration,
    valve_identifier: valves.State.ValveIdentifier,
):
    open_position, close_position = __get_open_close_positions(
        direction, alignment, geometry, step, lineConfiguration
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
                for i, item in enumerate(routine.positionThresholdToStateMapping)
                if isclose(item.positionThreshold, position, abs_tol=0.01)
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
