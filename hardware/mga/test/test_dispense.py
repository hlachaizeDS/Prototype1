from hardware.mga.dispense import (
    create_abstract_routine,
    create_dispense_plan,
    project_routine_to_axes,
)
from hardware.mga.configuration import DefaultGeometry, ReagentToLineMapping, Axis
import numpy as np
import sys
import copy
from math import isclose
import unittest
from hardware.mga.types import (
    Alignment,
    Direction,
    LineConfiguration,
    Routine,
    Well,
    LineIndex,
    DispensePlan,
    ValveState,
    Coordinate,
)


class TestDispensePlan(unittest.TestCase):
    reagentToFluidicLineIndexMapping: ReagentToLineMapping = {
        "A": {Direction.forward: 1, Direction.backward: 6},
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5,
        "F": 7,
    }

    def test_create_dispense_plan_with_empty_reagent_volume_wells(self):
        reagent_volume_wells = {}
        dispense_plan, volumes_per_well_per_line = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )
        self.assertDictEqual(dispense_plan, dict())
        self.assertDictEqual(volumes_per_well_per_line, dict())

    def test_create_dispense_plan_with_empty_reagent_to_line_mapping(self):
        reagent_volume_wells = {
            "A": (10.0, [well + 1 for well in range(384)]),
        }
        self.assertRaises(
            ValueError,
            create_dispense_plan,
            reagent_volume_wells,
            dict(),
        )

    def test_create_single_dispense_plan(self):
        reagent_volume_wells = {
            "E": (10.0, [well + 1 for well in range(384)]),
        }

        dispense_plan, volumes_per_well_per_line = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            5: [Well(wellIndex + 1) for wellIndex in range(384)]
        }
        self.assertDictEqual(dispense_plan, expected_dispense_plan)
        self.assertDictEqual(volumes_per_well_per_line, {5: 10.0})

    def test_create_multi_dispense_plan(self):
        reagent_volume_wells = {
            "B": (50.0, [well + 1 for well in range(384) if well % 2 == 0]),
            "C": (25.0, [well + 1 for well in range(384) if well % 2 == 1]),
        }

        dispense_plan, volumes_per_well_per_line = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            2: [Well(wellIndex + 1) for wellIndex in range(0, 384, 2)],
            3: [Well(wellIndex + 1) for wellIndex in range(1, 384, 2)],
        }

        self.assertDictEqual(dispense_plan, expected_dispense_plan)
        self.assertDictEqual(volumes_per_well_per_line, {2: 50.0, 3: 25.0})

    def test_create_multi_dispense_plan_with_empty_wells(self):
        reagent_volume_wells = {
            "B": (50.0, [well + 1 for well in range(384) if well % 2 == 0]),
            "C": (12.0, []),
        }

        dispense_plan, volumes_per_well_per_line = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            2: [Well(wellIndex + 1) for wellIndex in range(0, 384, 2)],
        }

        self.assertDictEqual(dispense_plan, expected_dispense_plan)
        self.assertDictEqual(volumes_per_well_per_line, {2: 50.0})

    def test_create_multi_dispense_plan_with_empty_reagent_volume_wells(self):
        reagent_volume_wells = {
            "B": (50.0, [well + 1 for well in range(384) if well % 2 == 0]),
            "C": (12.0, [well + 1 for well in range(384) if well % 2 == 1]),
            "D": (0.0, []),
        }

        dispense_plan, volumes_per_well_per_line = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            2: [Well(wellIndex + 1) for wellIndex in range(0, 384, 2)],
            3: [Well(wellIndex + 1) for wellIndex in range(1, 384, 2)],
        }

        self.assertDictEqual(dispense_plan, expected_dispense_plan)
        self.assertDictEqual(volumes_per_well_per_line, {2: 50.0, 3: 12.0})

    def test_create_dispense_plan_with_directional_reagent(self):
        reagent_volume_wells = {
            "A": (25.0, [well + 1 for well in range(384)]),
        }

        dispense_plan, volumes_per_well_per_line = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        # sort dispense_plan by row, column
        dispense_plan = {
            line: sorted(wells, key=lambda well: (well.row, well.column))
            for line, wells in dispense_plan.items()
        }

        expected_dispense_plan: DispensePlan = {
            1: sorted(
                [
                    Well(row=row, column=column)
                    for row in range(1, 17, 2)
                    for column in range(1, 25)
                ],
                key=lambda well: (well.row, well.column),
            ),
            6: sorted(
                [
                    Well(row=row, column=column)
                    for row in range(2, 17, 2)
                    for column in range(1, 25)
                ],
                key=lambda well: (well.row, well.column),
            ),
        }
        self.assertEqual(dispense_plan.keys(), expected_dispense_plan.keys())
        self.assertDictEqual(dispense_plan, expected_dispense_plan)
        self.assertDictEqual(volumes_per_well_per_line, {1: 25.0, 6: 25.0})


class TestCreateRoutine(unittest.TestCase):
    geometry = copy.deepcopy(DefaultGeometry)

    def test_create_abstract_routine_single_line_forward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {1: wells}

        line_configurations = {1: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=1, nozzle_index=4, row=1)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________█\n"
            " 1.1 ██_______██_______\n"
            " 1.2 __██_______██_____\n"
            " 1.3 ____██_______██___\n"
            " 1.4 ______██_______██_\n"
        )

        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_single_line_forward_3rd_trip(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 17)
            for column in range(1, 3)
        ]

        dispense_plan = {1: wells}

        line_configurations = {1: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=1, nozzle_index=1, row=15)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________█\n"
            " 1.1 ██_______██_______\n"
            " 1.2 __██_______██_____\n"
            " 1.3 ____██_______██___\n"
            " 1.4 ______██_______██_\n"
        )

        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_single_line_forward_2nd_manifold(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 17)
            for column in range(1, 3)
        ]

        dispense_plan = {12: wells}

        line_configurations = {12: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=7, nozzle_index=1, row=15)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            "12.0 ________█________\n"
            "12.1 ██_______██______\n"
            "12.2 __██_______██____\n"
            "12.3 ____██_______██__\n"
            "12.4 ______██_______██\n"
        )

        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_single_line_backward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {1: wells}

        line_configurations = {1: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=1, nozzle_index=4, row=1)
        direction = Direction.backward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds, reverse=True))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________█\n"
            " 1.1 ______██_______██_\n"
            " 1.2 ____██_______██___\n"
            " 1.3 __██_______██_____\n"
            " 1.4 ██_______██_______\n"
        )

        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_single_line_backward_absent_common_line(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {1: wells}

        line_configurations = {
            1: LineConfiguration(open_offset=0, close_offset=0),
            5: LineConfiguration(open_offset=0, close_offset=0),
        }

        alignment = Alignment(line_index=1, nozzle_index=4, row=1)
        direction = Direction.backward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
            lines_with_common_discharge_valve={1: 5, 5: 1},
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds, reverse=True))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________█\n"
            " 1.1 ______██_______██_\n"
            " 1.2 ____██_______██___\n"
            " 1.3 __██_______██_____\n"
            " 1.4 ██_______██_______\n"
            " 5.0 ________█________█\n"
            " 5.1 __________________\n"
            " 5.2 __________________\n"
            " 5.3 __________________\n"
            " 5.4 __________________\n"
        )

        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_multi_line_same_manifold_forward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {
            1: wells,
            6: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=1, nozzle_index=4, row=1)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________███████████████████████████████████████████████████████████████████████████████████████████\n"
            " 1.1 ██_______██_________________________________________________________________________________________________\n"
            " 1.2 __██_______██_______________________________________________________________________________________________\n"
            " 1.3 ____██_______██_____________________________________________________________________________________________\n"
            " 1.4 ______██_______██___________________________________________________________________________________________\n"
            " 6.0 ██████████████████████████████████████████████████████████████████████████████████████████________█________█\n"
            " 6.1 __________________________________________________________________________________________██_______██_______\n"
            " 6.2 ____________________________________________________________________________________________██_______██_____\n"
            " 6.3 ______________________________________________________________________________________________██_______██___\n"
            " 6.4 ________________________________________________________________________________________________██_______██_\n"
        )
        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_multi_line_same_manifold_backward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {
            7: wells,
            10: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=7, nozzle_index=4, row=1)
        direction = Direction.backward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds, reverse=True))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 7.0 ██████████████████████████████████████████████████████________█________█\n"
            " 7.1 ____________________________________________________________██_______██_\n"
            " 7.2 __________________________________________________________██_______██___\n"
            " 7.3 ________________________________________________________██_______██_____\n"
            " 7.4 ______________________________________________________██_______██_______\n"
            "10.0 ________█________███████████████████████████████████████████████████████\n"
            "10.1 ______██_______██_______________________________________________________\n"
            "10.2 ____██_______██_________________________________________________________\n"
            "10.3 __██_______██___________________________________________________________\n"
            "10.4 ██_______██_____________________________________________________________\n"
        )
        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_multi_line_different_manifold_forward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 17, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {
            1: wells,
            12: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=7, nozzle_index=4, row=1)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________███████████████████████████████████████████████████████████████████████████████████████████\n"
            " 1.1 ██_______██_________________________________________________________________________________________________\n"
            " 1.2 __██_______██_______________________________________________________________________________________________\n"
            " 1.3 ____██_______██_____________________________________________________________________________________________\n"
            " 1.4 ______██_______██___________________________________________________________________________________________\n"
            "12.0 ██████████████████████████████████████████████████████████████████████████████████████████________█________█\n"
            "12.1 __________________________________________________________________________________________██_______██_______\n"
            "12.2 ____________________________________________________________________________________________██_______██_____\n"
            "12.3 ______________________________________________________________________________________________██_______██___\n"
            "12.4 ________________________________________________________________________________________________██_______██_\n"
        )
        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_multi_line_same_manifold_shared_discharge_valve(
        self,
    ):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 17, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {
            7: wells,
            12: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=7, nozzle_index=4, row=1)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
            lines_with_common_discharge_valve={7: 12, 12: 7},
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 7.0 ________█________█████████████████████████████████████████████████████████████████████████________█________█\n"
            " 7.1 ██_______██_________________________________________________________________________________________________\n"
            " 7.2 __██_______██_______________________________________________________________________________________________\n"
            " 7.3 ____██_______██_____________________________________________________________________________________________\n"
            " 7.4 ______██_______██___________________________________________________________________________________________\n"
            "12.0 ________█________█████████████████████████████████████████████████████████████████████████________█________█\n"
            "12.1 __________________________________________________________________________________________██_______██_______\n"
            "12.2 ____________________________________________________________________________________________██_______██_____\n"
            "12.3 ______________________________________________________________________________________________██_______██___\n"
            "12.4 ________________________________________________________________________________________________██_______██_\n"
        )
        self.assertEqual(geogram, expected_geogram)

    def test_create_abstract_routine_multi_line_single_manifold_missing_column(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 17, 2)
            for column in range(1, 5)
            if column != 3  # missing column
        ]

        dispense_plan = {
            1: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=7, nozzle_index=4, row=1)
        direction = Direction.forward

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        geogram = create_geogram(routine)

        expected_geogram = (
            " 1.0 ________█________██████████________█\n"
            " 1.1 ██_______██________________██_______\n"
            " 1.2 __██_______██________________██_____\n"
            " 1.3 ____██_______██________________██___\n"
            " 1.4 ______██_______██________________██_\n"
        )

        self.assertEqual(geogram, expected_geogram)

    def test_project_routine_start_end_thresholds_forward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(1, 3)
        ]

        dispense_plan = {1: wells}

        line_configurations = {1: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=3, nozzle_index=4, row=1)
        direction = Direction.forward

        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(100, 200)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=geometry,
            direction=direction,
            line_configurations=line_configurations,
        )
        routine = project_routine_to_axes(
            routine,
            geometry,
            axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds))

        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 99.5, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[-1].positionThreshold, 108.0, 3
        )

    def test_project_routine_start_end_thresholds_backward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 9, 2)
            for column in range(7, 9)
        ]

        dispense_plan = {2: wells}

        line_configurations = {2: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=1, nozzle_index=4, row=1)
        direction = Direction.backward

        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(400, 0)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )
        routine = project_routine_to_axes(
            routine,
            geometry,
            axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]
        self.assertEqual(thresholds, sorted(thresholds, reverse=True))

        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 444.0, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[-1].positionThreshold, 435.5, 3
        )

    def test_project_routine_foward_in_ascending_x(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        abstract_routine = Routine(
            direction=Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=-4.0, state={}),
                Routine.Item(positionThreshold=10.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine,
            geometry,
            axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=True,
        )

        self.assertEqual(routine.direction, Direction.forward)
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 182, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[1].positionThreshold, 245, 3
        )
        self.assertEqual(create_geogram(routine), create_geogram(abstract_routine))

    def test_project_routine_foward_in_descending_x(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        abstract_routine = Routine(
            direction=Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=-1.0, state={}),
                Routine.Item(positionThreshold=5.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine,
            geometry,
            axis=Axis.x,
            are_rows_ascending=True,
            are_columns_ascending=False,
        )

        self.assertEqual(routine.direction, Direction.backward)
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 204.5, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[1].positionThreshold, 177.5, 3
        )
        self.assertEqual(create_geogram(routine), create_geogram(abstract_routine))

    def test_project_routine_foward_in_descending_y(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        abstract_routine = Routine(
            direction=Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=-1.0, state={}),
                Routine.Item(positionThreshold=5.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine,
            geometry,
            axis=Axis.y,
            are_rows_ascending=True,
            are_columns_ascending=False,
        )

        self.assertEqual(routine.direction, Direction.backward)
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 404.5, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[1].positionThreshold, 377.5, 3
        )
        self.assertEqual(create_geogram(routine), create_geogram(abstract_routine))

    def test_project_routine_backward_in_descending_y(self):
        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        abstract_routine = Routine(
            direction=Direction.backward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=4.0, state={}),
                Routine.Item(positionThreshold=-2.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine,
            geometry,
            axis=Axis.y,
            are_rows_ascending=True,
            are_columns_ascending=False,
        )

        self.assertEqual(routine.direction, Direction.forward)
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 382, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[1].positionThreshold, 409, 3
        )
        self.assertEqual(create_geogram(routine), create_geogram(abstract_routine))

    def test_project_routine_real_data(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(1, 17)
            for column in range(1, 2)
        ]

        dispense_plan = {1: wells}

        line_configurations = {1: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=1, nozzle_index=4, row=7)
        direction = Direction.forward

        geometry = copy.deepcopy(DefaultGeometry)
        geometry.reference.position = Coordinate(127.67, 162.96)
        geometry.reference.line_index = 1
        geometry.reference.nozzle_index = 4
        geometry.reference.well = Well(row=7, column=1)

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=geometry,
            direction=direction,
            line_configurations=line_configurations,
        )
        routine = project_routine_to_axes(
            routine,
            geometry,
            axis=Axis.y,
            are_rows_ascending=False,
            are_columns_ascending=False,
        )

        thresholds = [
            item.positionThreshold for item in routine.positionThresholdToStateMapping
        ]

        self.assertEqual(routine.direction, Direction.backward)

        self.assertEqual(thresholds, sorted(thresholds, reverse=True))

        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 163.46, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[-1].positionThreshold, 159.46, 3
        )


# utils


def print_in_file(file: str, function):
    orig_stdout = sys.stdout
    f = open(file, "w")
    sys.stdout = f

    function()

    sys.stdout = orig_stdout
    f.close()


def create_geogram(routine: Routine) -> str:
    if len(routine.positionThresholdToStateMapping) == 0:
        return ""
    # get all lines
    lines: set[LineIndex] = set()
    for item in routine.positionThresholdToStateMapping:
        for valve in item.state.valves:
            lines.add(valve.identifier.fluidicLine)

    # find minimum distance between to consecutive thresholds
    step: float = np.inf
    for i in range(1, len(routine.positionThresholdToStateMapping)):
        step = min(
            step,
            abs(
                routine.positionThresholdToStateMapping[i].positionThreshold
                - routine.positionThresholdToStateMapping[i - 1].positionThreshold
            ),
        )

    step = step * (1 if routine.direction == Direction.forward else -1)
    if step == 0:
        raise ValueError("Step is 0")

    min_threshold = min(
        [item.positionThreshold for item in routine.positionThresholdToStateMapping]
    )
    max_threshold = max(
        [item.positionThreshold for item in routine.positionThresholdToStateMapping]
    )

    start = min_threshold if routine.direction == Direction.forward else max_threshold
    end = max_threshold if routine.direction == Direction.forward else min_threshold

    output = ""
    for line in [line for line in sorted(lines)]:
        for nozzle in range(5):
            last_valve_state = ValveState.open if nozzle == 0 else ValveState.closed
            output += f"{line:2.0f}.{nozzle} "
            for threshold in np.arange(start, end, step):
                for item in routine.positionThresholdToStateMapping:
                    if isclose(item.positionThreshold, threshold, abs_tol=0.001):
                        # print("equals!")
                        for valve in item.state.valves:
                            if (
                                valve.identifier.fluidicLine == line
                                and valve.identifier.id == nozzle
                            ):
                                last_valve_state = valve.state
                output += "█" if last_valve_state == ValveState.open else "_"
            output += "\n"
    return output


def print_wells(wells: list[Well]):
    print()
    for row in range(1, 17):
        print("|", end="")
        for column in range(1, 25):
            print("x|" if Well(row=row, column=column) in wells else " |", end="")
        print()
    print()


def print_routine(routine: Routine):
    for item in routine.positionThresholdToStateMapping:
        print(item.positionThreshold)
        for valve in item.state.valves:
            print(
                f"\t{valve.identifier.fluidicLine}.{valve.identifier.id} -> {'open' if valve.state == 0 else 'closed'}"
            )
