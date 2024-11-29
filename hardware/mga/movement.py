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

    sign = 1 if routine.direction == routine.Direction.forward else -1
    start_x = (
        routine.positionThresholdToStateMapping[0].positionThreshold - sign * margin.x
    )
    end_x = (
        routine.positionThresholdToStateMapping[-1].positionThreshold + sign * margin.x
    )

    y = geometry.reference.position.y + (
        alignment.row
        - alignment.nozzle_index * geometry.y_inter_nozzle_spacing_wells_in_line
    )

    return Coordinate(0 * start_x, y), Coordinate(end_x, y)


def find_first_nozzle_on_first_well_coordinate(
    geometry: Geometry,
    alignment: Alignment,
):
    return Coordinate(
        x=geometry.reference.position.x
        + (
            (alignment.line_index - geometry.reference.line_index)
            * geometry.x_inter_nozzle_spacing_wells_in_line
            + geometry.reference.well.column
        )
        * geometry.inter_well_spacing_mm,
        y=geometry.reference.position.y
        + (
            (
                alignment.row - geometry.reference.well.row
                + alignment.nozzle_index * geometry.y_inter_nozzle_spacing_wells_in_line
            )
            * geometry.inter_well_spacing_mm
        ),
    )
