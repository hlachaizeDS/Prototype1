from hardware.mga.dispense import (
    create_abstract_routine,
    create_dispense_plan,
    project_routine_to_axes,
)
from hardware.mga.configuration import DefaultGeometry, ReagentToLineMapping, Axis
import numpy as np
import sys
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
        "A": {Direction.forward: 0, Direction.backward: 5},
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 6,
    }

    def test_create_dispense_plan_with_empty_reagent_volume_wells(self):
        reagent_volume_wells = {}
        dispense_plan = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )
        self.assertDictEqual(dispense_plan, dict())

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

    def test_create_multi_dispense_plan_with_different_volumes(self):
        reagent_volume_wells = {
            "E": (10.0, [well + 1 for well in range(384)]),
            "D": (5.0, [well + 1 for well in range(384)]),
        }
        self.assertRaises(
            ValueError,
            create_dispense_plan,
            reagent_volume_wells,
            self.reagentToFluidicLineIndexMapping,
        )

    def test_create_single_dispense_plan(self):
        reagent_volume_wells = {
            "E": (10.0, [well + 1 for well in range(384)]),
        }

        dispense_plan = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            4: [Well(wellIndex + 1) for wellIndex in range(384)]
        }
        self.assertDictEqual(dispense_plan, expected_dispense_plan)

    def test_create_multi_dispense_plan(self):
        reagent_volume_wells = {
            "B": (50.0, [well + 1 for well in range(384) if well % 2 == 0]),
            "C": (50.0, [well + 1 for well in range(384) if well % 2 == 1]),
        }

        dispense_plan = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            1: [Well(wellIndex + 1) for wellIndex in range(0, 384, 2)],
            2: [Well(wellIndex + 1) for wellIndex in range(1, 384, 2)],
        }

        self.assertDictEqual(dispense_plan, expected_dispense_plan)

    def test_create_multi_dispense_plan_with_empty_wells(self):
        reagent_volume_wells = {
            "B": (50.0, [well + 1 for well in range(384) if well % 2 == 0]),
            "C": (50.0, []),
        }

        dispense_plan = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            1: [Well(wellIndex + 1) for wellIndex in range(0, 384, 2)],
        }

        self.assertDictEqual(dispense_plan, expected_dispense_plan)

    def test_create_multi_dispense_plan_with_empty_reagent_volume_wells(self):
        reagent_volume_wells = {
            "B": (50.0, [well + 1 for well in range(384) if well % 2 == 0]),
            "C": (50.0, [well + 1 for well in range(384) if well % 2 == 1]),
            "D": (0.0, []),
        }

        dispense_plan = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        expected_dispense_plan: DispensePlan = {
            1: [Well(wellIndex + 1) for wellIndex in range(0, 384, 2)],
            2: [Well(wellIndex + 1) for wellIndex in range(1, 384, 2)],
        }

        self.assertDictEqual(dispense_plan, expected_dispense_plan)

    def test_create_dispense_plan_with_directional_reagent(self):
        reagent_volume_wells = {
            "A": (25.0, [well + 1 for well in range(384)]),
        }

        dispense_plan = create_dispense_plan(
            reagent_volume_wells, self.reagentToFluidicLineIndexMapping
        )

        # sort dispense_plan by row, column
        dispense_plan = {
            line: sorted(wells, key=lambda well: (well.row, well.column))
            for line, wells in dispense_plan.items()
        }

        expected_dispense_plan: DispensePlan = {
            0: sorted(
                [
                    Well(row=row, column=column)
                    for row in range(0, 16, 2)
                    for column in range(0, 24)
                ],
                key=lambda well: (well.row, well.column),
            ),
            5: sorted(
                [
                    Well(row=row, column=column)
                    for row in range(1, 16, 2)
                    for column in range(0, 24)
                ],
                key=lambda well: (well.row, well.column),
            ),
        }
        self.assertEqual(dispense_plan.keys(), expected_dispense_plan.keys())
        self.assertDictEqual(dispense_plan, expected_dispense_plan)


class TestCreateRoutine(unittest.TestCase):
    geometry = DefaultGeometry

    def test_create_abstract_routine_single_line_forward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(0, 8, 2)
            for column in range(0, 2)
        ]

        dispense_plan = {0: wells}

        line_configurations = {0: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=0, nozzle_index=3, row=0)
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

    def test_create_abstract_routine_single_line_backward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(0, 8, 2)
            for column in range(0, 2)
        ]

        dispense_plan = {0: wells}

        line_configurations = {0: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=0, nozzle_index=3, row=0)
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

    def test_create_abstract_routine_multi_line_same_manifold_forward(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(0, 8, 2)
            for column in range(0, 2)
        ]

        dispense_plan = {
            0: wells,
            5: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=0, nozzle_index=3, row=0)
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
            for row in range(0, 8, 2)
            for column in range(0, 2)
        ]

        dispense_plan = {
            6: wells,
            9: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=6, nozzle_index=3, row=0)
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
            for row in range(0, 16, 2)
            for column in range(0, 2)
        ]

        dispense_plan = {
            0: wells,
            11: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=6, nozzle_index=3, row=0)
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

    def test_create_abstract_routine_multi_line_single_manifold_missing_column(self):
        wells: list[Well] = [
            Well(row=row, column=column)
            for row in range(0, 16, 2)
            for column in range(0, 4)
            if column != 2  # missing column
        ]

        dispense_plan = {
            0: wells,
        }

        line_configurations = {
            index: LineConfiguration(open_offset=0, close_offset=0)
            for index in dispense_plan.keys()
        }

        alignment = Alignment(line_index=6, nozzle_index=3, row=0)
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
            for row in range(0, 8, 2)
            for column in range(0, 2)
        ]

        dispense_plan = {0: wells}

        line_configurations = {0: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=2, nozzle_index=3, row=0)
        direction = Direction.forward

        geometry = DefaultGeometry
        geometry.reference.position = Coordinate(100, 200)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3
        geometry.reference.well = Well(row=6, column=0)

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=geometry,
            direction=direction,
            line_configurations=line_configurations,
        )
        routine = project_routine_to_axes(
            routine, geometry, axis=Axis.x, is_forward_along_columns=True
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
            for row in range(0, 8, 2)
            for column in range(6, 8)
        ]

        dispense_plan = {1: wells}

        line_configurations = {1: LineConfiguration(open_offset=0, close_offset=0)}

        alignment = Alignment(line_index=0, nozzle_index=3, row=0)
        direction = Direction.backward

        geometry = DefaultGeometry
        geometry.reference.position = Coordinate(400, 0)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3
        geometry.reference.well = Well(row=6, column=0)

        routine = create_abstract_routine(
            dispense_plan=dispense_plan,
            alignment=alignment,
            geometry=self.geometry,
            direction=direction,
            line_configurations=line_configurations,
        )
        routine = project_routine_to_axes(
            routine, geometry, axis=Axis.x, is_forward_along_columns=True
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
        geometry = DefaultGeometry
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3
        geometry.reference.well = Well(row=6, column=0)

        abstract_routine = Routine(
            direction=Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=-4.0, state={}),
                Routine.Item(positionThreshold=10.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine, geometry, axis=Axis.x, is_forward_along_columns=True
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
        geometry = DefaultGeometry
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3
        geometry.reference.well = Well(row=6, column=0)

        abstract_routine = Routine(
            direction=Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=-1.0, state={}),
                Routine.Item(positionThreshold=5.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine, geometry, axis=Axis.x, is_forward_along_columns=False
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
        geometry = DefaultGeometry
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3
        geometry.reference.well = Well(row=6, column=0)

        abstract_routine = Routine(
            direction=Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=-1.0, state={}),
                Routine.Item(positionThreshold=5.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine, geometry, axis=Axis.y, is_forward_along_columns=False
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
        geometry = DefaultGeometry
        geometry.reference.position = Coordinate(200, 400)
        geometry.reference.line_index = 0
        geometry.reference.nozzle_index = 3
        geometry.reference.well = Well(row=6, column=0)

        abstract_routine = Routine(
            direction=Direction.backward,
            positionThresholdToStateMapping=[
                Routine.Item(positionThreshold=4.0, state={}),
                Routine.Item(positionThreshold=-2.0, state={}),
            ],
        )
        routine = project_routine_to_axes(
            abstract_routine, geometry, axis=Axis.y, is_forward_along_columns=False
        )

        self.assertEqual(routine.direction, Direction.forward)
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[0].positionThreshold, 382, 3
        )
        self.assertAlmostEqual(
            routine.positionThresholdToStateMapping[1].positionThreshold, 409, 3
        )
        self.assertEqual(create_geogram(routine), create_geogram(abstract_routine))


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
    for row in range(0, 16):
        print("|", end="")
        for column in range(0, 24):
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
