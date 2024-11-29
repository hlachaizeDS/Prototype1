import unittest
from hardware.mga.movement import (
    get_movement_range_coordinates,
    find_first_nozzle_on_first_well_coordinate,
)
from hardware.mga.configuration import StandardGeometry, Coordinate
from hardware.mga.dispense import Routine, Alignment


class TestMovement(unittest.TestCase):
    geometry = StandardGeometry

    # def test_get_movement_range_coordinates(self):
    #     alignment = Alignment(line_index=0, nozzle_index=3, row=0)
    #     routine = Routine(
    #         direction=Routine.Direction.forward,
    #         positionThresholdToStateMapping=[
    #             Routine.Item(positionThreshold=0, state={}),
    #             Routine.Item(positionThreshold=10, state={}),
    #         ],
    #     )
    #     coordinates = get_movement_range_coordinates(
    #         self.geometry, alignment, routine, Coordinate(2, 0)
    #     )

    #     self.assertIsNone(coordinates)
    #     if coordinates is not None:
    #         self.assertTupleEqual(coordinates, (Coordinate(-2, 0), Coordinate(12, 0)))

    def test_find_first_nozzle_on_first_well_coordinate(self):
        alignment = Alignment(line_index=0, nozzle_index=3, row=0)
        coordinate = find_first_nozzle_on_first_well_coordinate(
            self.geometry, alignment
        )

        self.assertEqual(coordinate, Coordinate(0.0, 0.0))
