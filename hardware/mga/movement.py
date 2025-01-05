from hardware.mga.configuration import Geometry, Axis
from hardware.mga.types import Coordinate, Alignment, Routine

DispenseMovementMargin = 1.0  # mm
MovementRange = tuple[Coordinate, Coordinate]


def get_movement_range_coordinates(
    geometry: Geometry,
    alignment: Alignment,
    routine: Routine,
    margin: float,
    movement_axis: Axis,
    are_rows_ascending: bool,
    are_columns_ascending: bool,
) -> MovementRange | None:
    """
    Get the coordinates of the start and end of a movement for a routine
    """

    if routine is None or len(routine.positionThresholdToStateMapping) == 0:
        return None

    sign = 1 if routine.direction == routine.Direction.forward else -1

    start = routine.positionThresholdToStateMapping[0].positionThreshold - sign * margin
    end = routine.positionThresholdToStateMapping[-1].positionThreshold + sign * margin
    alignment_coordinates = find_alignment_coordinates(
        geometry,
        alignment,
        movement_axis,
        are_rows_ascending=are_rows_ascending,
        are_columns_ascending=are_columns_ascending,
    )

    if movement_axis == Axis.x:
        return Coordinate(start, alignment_coordinates.y), Coordinate(
            end, alignment_coordinates.y
        )

    return Coordinate(alignment_coordinates.x, start), Coordinate(
        alignment_coordinates.x, end
    )


def find_alignment_coordinates(
    geometry: Geometry,
    alignment: Alignment,
    movement_axis: Axis,
    are_rows_ascending: bool,
    are_columns_ascending: bool,
):
    manifold_index_difference = (
        geometry.reference.line_index - alignment.line_index
    ) // geometry.number_of_lines_in_manifold

    alignment_line_index_difference = (
        geometry.reference.line_index - alignment.line_index
    ) % geometry.number_of_lines_in_manifold
    nozzle_index_difference = alignment.nozzle_index - geometry.reference.nozzle_index
    row_difference = alignment.row - geometry.reference.well.row

    parallel_sign = 1 if are_columns_ascending else -1
    parallel_offset = (
        parallel_sign
        * (
            alignment_line_index_difference * geometry.inter_line_spacing_wells
            - (geometry.reference.well.column - 1)
            + nozzle_index_difference * geometry.x_inter_nozzle_spacing_wells_in_line
        )
        * geometry.inter_well_spacing_mm
    )

    perpendicular_sign = 1 if are_rows_ascending else -1
    perpendicular_offset = (
        perpendicular_sign
        * (
            row_difference
            + (
                nozzle_index_difference
                + manifold_index_difference * geometry.number_of_nozzles_per_line
            )
            * geometry.y_inter_nozzle_spacing_wells_in_line
        )
        * geometry.inter_well_spacing_mm
    )

    x_offset = parallel_offset if movement_axis == Axis.x else perpendicular_offset
    y_offset = perpendicular_offset if movement_axis == Axis.x else parallel_offset

    return Coordinate(
        x=geometry.reference.position.x + x_offset,
        y=geometry.reference.position.y + y_offset,
    )


def get_gantry_dispense_movement_speed(
    dispense_volume: float, pump_speed: float, inter_nozzle_in_movement_distance: float
):
    """
    Get the gantry dispense movement speed
    """
    return inter_nozzle_in_movement_distance / (dispense_volume / pump_speed)
