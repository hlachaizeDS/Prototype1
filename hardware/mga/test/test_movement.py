import unittest
from hardware.mga.movement import (
    get_movement_range_coordinates,
    find_alignment_coordinates,
)
from hardware.mga.configuration import StandardGeometry, Coordinate
from hardware.mga.dispense import Routine, Alignment
from hardware.mga.types import Well


class TestMovement(unittest.TestCase):
    def test_get_movement_range_coordinates(self):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=6, column=0)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3

        alignment = Alignment(line_index=0, nozzle_index=3, row=6)
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=0, state={}),
                Routine.Item(positionThreshold=10, state={}),
            ],
        )
        coordinates = get_movement_range_coordinates(
            geometry, alignment, routine, Coordinate(2, 0)
        )

        self.assertIsNotNone(coordinates)
        if coordinates is not None:
            self.assertTupleEqual(coordinates, (Coordinate(198.0, 100.0), Coordinate(212.0, 100.0)))

    def test_find_alignment_coordinates_reference(self):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=6, column=0)
        geometry.reference.position = Coordinate(10.0, 100.0)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 0

        alignment = Alignment(line_index=0, nozzle_index=3, row=0)
        coordinate = find_alignment_coordinates(geometry, alignment)

        self.assertEqual(coordinate, Coordinate(13.0, 100.0))

    def test_find_alignment_coordinates_different_line_to_reference(self):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=6, column=0)
        geometry.reference.position = Coordinate(300.0, 10.0)
        geometry.reference.line_index = 2
        geometry.reference.nozzle_index = 3

        alignment = Alignment(line_index=5, nozzle_index=3, row=6)
        coordinate = find_alignment_coordinates(geometry, alignment)

        self.assertEqual(coordinate, Coordinate(327.0, 10.0))

    def test_find_alignment_coordinates_different_nozzle_to_reference(self):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=8, column=0)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 2
        geometry.reference.nozzle_index = 3

        alignment = Alignment(line_index=2, nozzle_index=1, row=8)
        coordinate = find_alignment_coordinates(geometry, alignment)

        self.assertEqual(coordinate, Coordinate(198.0, 82.0))

    def test_find_alignment_coordinates_different_row_to_reference(self):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=4, column=0)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 3
        geometry.reference.nozzle_index = 1

        alignment = Alignment(line_index=3, nozzle_index=1, row=10)
        coordinate = find_alignment_coordinates(geometry, alignment)

        self.assertEqual(coordinate, Coordinate(200.0, 127.0))

    def test_find_alignment_coordinates_different_nozzle_to_reference_different_manifolds(
        self,
    ):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=6, column=0)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 6
        geometry.reference.nozzle_index = 0

        alignment = Alignment(line_index=0, nozzle_index=0, row=6)
        coordinate = find_alignment_coordinates(geometry, alignment)

        self.assertEqual(coordinate, Coordinate(200.0, 64.0))

    def test_find_alignment_coordinates_different_line_row_nozzle_to_reference_different_manifolds(
        self,
    ):
        geometry = StandardGeometry
        geometry.reference.well = Well(row=0, column=0)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 11
        geometry.reference.nozzle_index = 3

        alignment = Alignment(line_index=0, nozzle_index=0, row=12)
        coordinate = find_alignment_coordinates(geometry, alignment)

        self.assertEqual(coordinate, Coordinate(152.0, 91.0))
