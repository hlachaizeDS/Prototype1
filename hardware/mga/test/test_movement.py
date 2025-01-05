import unittest
from hardware.mga.movement import (
    get_movement_range_coordinates,
    find_alignment_coordinates,
    get_gantry_dispense_movement_speed,
)
from hardware.mga.configuration import DefaultGeometry, Coordinate, Axis
from hardware.mga.dispense import Routine, Alignment
from hardware.mga.types import Well
import copy


class TestMovement(unittest.TestCase):
    def test_find_alignment_coordinates_reference_self(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(10.0, 100.0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=1, nozzle_index=4, row=7)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.y,
            are_rows_ascending=False,
            are_columns_ascending=False,
        )

        self.assertEqual(coordinate, Coordinate(10.0, 100.0))

    def test_find_alignment_coordinates_reference(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(10.0, 100.0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 1

        alignment = Alignment(line_index=1, nozzle_index=4, row=1)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(coordinate, Coordinate(13.0, 100.0))

    def test_find_alignment_coordinates_different_line_to_reference(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(300.0, 10.0)
        geometry.reference.line_index = 3
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=6, nozzle_index=4, row=7)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(coordinate, Coordinate(327.0, 10.0))

    def test_find_alignment_coordinates_different_nozzle_to_reference(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=9, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 3
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=3, nozzle_index=2, row=9)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(coordinate, Coordinate(198.0, 82.0))

    def test_find_alignment_coordinates_different_row_to_reference(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=5, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 4
        geometry.reference.nozzle_index = 2

        alignment = Alignment(line_index=4, nozzle_index=2, row=11)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(coordinate, Coordinate(200.0, 127.0))

    def test_find_alignment_coordinates_different_nozzle_to_reference_different_manifolds(
        self,
    ):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 7
        geometry.reference.nozzle_index = 1

        alignment = Alignment(line_index=1, nozzle_index=1, row=7)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(coordinate, Coordinate(200.0, 64.0))

    def test_find_alignment_coordinates_different_line_row_nozzle_to_reference_different_manifolds(
        self,
    ):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=1, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 12
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=1, nozzle_index=1, row=13)
        coordinate = find_alignment_coordinates(
            geometry,
            alignment,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(coordinate, Coordinate(152.0, 91.0))

    def test_get_gantry_x_movement_speed(self):
        self.assertAlmostEqual(
            get_gantry_dispense_movement_speed(
                dispense_volume=12.5,
                pump_speed=500,
                inter_nozzle_in_movement_distance=1,
            ),
            40.0,
            3,
        )

    def test_get_movement_range_coordinates_forward_x(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=1, nozzle_index=4, row=7)
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=200.0, state={}),
                Routine.Item(positionThreshold=210.0, state={}),
            ],
        )
        coordinates = get_movement_range_coordinates(
            geometry,
            alignment,
            routine,
            margin=2.0,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertIsNotNone(coordinates)
        if coordinates is not None:
            self.assertTupleEqual(
                coordinates, (Coordinate(198.0, 100.0), Coordinate(212.0, 100.0))
            )

    def test_get_movement_range_coordinates_backward_x(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=1, nozzle_index=4, row=7)
        routine = Routine(
            direction=Routine.Direction.backward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=180.0, state={}),
                Routine.Item(positionThreshold=150.0, state={}),
            ],
        )
        coordinates = get_movement_range_coordinates(
            geometry,
            alignment,
            routine,
            margin=2.0,
            movement_axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertIsNotNone(coordinates)
        if coordinates is not None:
            self.assertTupleEqual(
                coordinates, (Coordinate(182.0, 100.0), Coordinate(148.0, 100.0))
            )

    def test_get_movement_range_coordinates_forward_y(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=7, nozzle_index=4, row=7)
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=90.0, state={}),
                Routine.Item(positionThreshold=120.0, state={}),
            ],
        )
        coordinates = get_movement_range_coordinates(
            geometry,
            alignment,
            routine,
            margin=3.0,
            movement_axis=Axis.y,
            are_rows_ascending=False,
            are_columns_ascending=False,
        )

        self.assertIsNotNone(coordinates)
        if coordinates is not None:
            self.assertTupleEqual(
                coordinates, (Coordinate(164.0, 87.0), Coordinate(164.0, 123.0))
            )

    def test_get_movement_range_coordinates_backward_y(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.well = Well(row=7, column=1)
        geometry.reference.position = Coordinate(200.0, 100.0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4

        alignment = Alignment(line_index=1, nozzle_index=4, row=8)
        routine = Routine(
            direction=Routine.Direction.backward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=110.0, state={}),
                Routine.Item(positionThreshold=80.0, state={}),
            ],
        )
        coordinates = get_movement_range_coordinates(
            geometry,
            alignment,
            routine,
            margin=3.0,
            movement_axis=Axis.y,
            are_rows_ascending=False,
            are_columns_ascending=False,
        )

        self.assertIsNotNone(coordinates)
        if coordinates is not None:
            self.assertTupleEqual(
                coordinates, (Coordinate(195.5, 113.0), Coordinate(195.5, 77.0))
            )
