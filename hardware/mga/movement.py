from hardware.mga.dispense import Routine, Alignment
from hardware.mga.configuration import Geometry
from hardware.mga.types import Coordinate


def get_movement_range_coordinates(
    geometry: Geometry, alignment: Alignment, routine: Routine, margin: Coordinate
) -> tuple[Coordinate, Coordinate] | None:
    """
    Get the coordinates of the start and end of a movement for a routine
    """

    if routine is None or len(routine.positionThresholdToStateMapping) == 0:
        return None

    start_coordinate = find_alignment_coordinates(geometry, alignment)

    sign = 1 if routine.direction == routine.Direction.forward else -1
    start_x = start_coordinate.x + (
        routine.positionThresholdToStateMapping[0].positionThreshold - sign * margin.x
    )
    end_x = start_coordinate.x + (
        routine.positionThresholdToStateMapping[-1].positionThreshold + sign * margin.x
    )
    y = start_coordinate.y

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
