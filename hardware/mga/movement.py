from hardware.mga.configuration import Geometry
from hardware.mga.types import Coordinate, Alignment, Routine


def get_movement_range_coordinates(
    geometry: Geometry, alignment: Alignment, routine: Routine, margin: Coordinate
) -> tuple[Coordinate, Coordinate] | None:
    """
    Get the coordinates of the start and end of a movement for a routine
    """

    if routine is None or len(routine.positionThresholdToStateMapping) == 0:
        return None

    sign = 1 if routine.direction == routine.Direction.forward else -1
    start_x = (
        routine.positionThresholdToStateMapping[0].positionThreshold - sign * margin.x
    )
    end_x = (
        routine.positionThresholdToStateMapping[-1].positionThreshold + sign * margin.x
    )
    y = find_alignment_coordinates(geometry, alignment).y

    return Coordinate(start_x, y), Coordinate(end_x, y)


def find_alignment_coordinates(
    geometry: Geometry,
    alignment: Alignment,
):
    reference_manifold_index = (
        geometry.reference.line_index // geometry.number_of_lines_in_manifold
    )
    alignment_manifold_index = (
        alignment.line_index // geometry.number_of_lines_in_manifold
    )
    manifold_index_difference = alignment_manifold_index - reference_manifold_index

    reference_line_index = (
        geometry.reference.line_index % geometry.number_of_lines_in_manifold
    )
    alignment_line_index = alignment.line_index % geometry.number_of_lines_in_manifold

    return Coordinate(
        x=geometry.reference.position.x
        + (
            (alignment_line_index - reference_line_index)
            * geometry.inter_line_spacing_wells
            - geometry.reference.well.column
            + (alignment.nozzle_index - geometry.reference.nozzle_index)
            * geometry.x_inter_nozzle_spacing_wells_in_line
        )
        * geometry.inter_well_spacing_mm,
        y=geometry.reference.position.y
        + (
            (alignment.row - geometry.reference.well.row)
            + (
                alignment.nozzle_index
                - geometry.reference.nozzle_index
                + manifold_index_difference * geometry.number_of_nozzles_per_line
            )
            * geometry.y_inter_nozzle_spacing_wells_in_line
        )
        * geometry.inter_well_spacing_mm,
    )


def get_gantry_x_movement_speed(
    dispense_volume: float, pump_speed: float, inter_nozzle_x_distance: float
):
    """
    Get the gantry x movement speed
    """
    return inter_nozzle_x_distance / (dispense_volume / pump_speed)
