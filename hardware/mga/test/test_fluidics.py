import unittest
from hardware.mga.fluidics import (
    get_pump_dispense_axis_range_from_routine,
    get_pump_dispense_axis_range_from_movement_range,
    estimate_volume_usage,
)
from hardware.mga.types import Routine, Coordinate
import mga_testbench_interface.generated.valves_pb2 as valves
from hardware.mga.configuration import Axis


class TestFluidics(unittest.TestCase):
    def test_pump_dispense_axis_range_from_routine_forward(self):
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(
                    positionThreshold=threshold,
                    state=valves.State(
                        valves=[
                            valves.State.Valve(
                                identifier=valves.State.ValveIdentifier(
                                    fluidicLine=line
                                ),
                                state=state,
                            )
                        ]
                    ),
                )
                for threshold, line, state in [
                    (200.0, 1, valves.State.open),
                    (203.0, 4, valves.State.open),
                    (205.0, 1, valves.State.closed),
                    (208.0, 4, valves.State.closed),
                ]
            ],
        )
        fluidic_line_to_pump_mapping = {1: 6, 4: 9}
        pump_start_stop_margin_mm = 1
        pump_dispense_axis_ranges, line_indexes = (
            get_pump_dispense_axis_range_from_routine(
                routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
            )
        )

        self.assertIsNotNone(pump_dispense_axis_ranges)
        if pump_dispense_axis_ranges is not None:
            self.assertDictEqual(
                pump_dispense_axis_ranges,
                {
                    6: (199.0, 206.0),
                    9: (202.0, 209.0),
                },
            )
        self.assertListEqual(line_indexes, [1, 4])

    def test_pump_dispense_axis_range_from_routine_backward(self):
        routine = Routine(
            direction=Routine.Direction.backward,
            positionThresholdToStateMapping=[
                Routine.Item(
                    positionThreshold=threshold,
                    state=valves.State(
                        valves=[
                            valves.State.Valve(
                                identifier=valves.State.ValveIdentifier(
                                    fluidicLine=line
                                ),
                                state=state,
                            )
                        ]
                    ),
                )
                for threshold, line, state in [
                    (150.0, 3, valves.State.open),
                    (142.0, 3, valves.State.closed),
                    (132.0, 9, valves.State.open),
                    (128.0, 9, valves.State.closed),
                    (122.0, 9, valves.State.open),
                    (118.0, 9, valves.State.closed),
                ]
            ],
        )
        fluidic_line_to_pump_mapping = {3: 1, 9: 2}
        pump_start_stop_margin_mm = 1
        pump_dispense_axis_ranges, line_indexes = (
            get_pump_dispense_axis_range_from_routine(
                routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
            )
        )

        self.assertIsNotNone(pump_dispense_axis_ranges)
        if pump_dispense_axis_ranges is not None:
            self.assertDictEqual(
                pump_dispense_axis_ranges,
                {
                    1: (151.0, 141.0),
                    2: (133.0, 117.0),
                },
            )
        self.assertListEqual(sorted(line_indexes), [3, 9])

    def test_estimate_volume_usage(self):
        pump_ranges = {1: (151.0, 141.0), 2: (133.0, 118.0)}
        pump_speeds = {1: 10.0, 2: 20.0}  # µl/s
        gantry_x_movement_speed = 5.0  # mm/s
        volume_usage = estimate_volume_usage(
            pump_ranges, pump_speeds, gantry_x_movement_speed
        )

        self.assertIsNotNone(volume_usage)
        if volume_usage is not None:
            self.assertDictEqual(
                volume_usage,
                {
                    1: 20.0,
                    2: 60.0,
                },
            )

    def test_pump_dispense_axis_range_from_routine_two_lines_one_pump(self):
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(
                    positionThreshold=threshold,
                    state=valves.State(
                        valves=[
                            valves.State.Valve(
                                identifier=valves.State.ValveIdentifier(
                                    fluidicLine=line
                                ),
                                state=state,
                            )
                        ]
                    ),
                )
                for threshold, line, state in [
                    (100.0, 7, valves.State.open),
                    (120.0, 7, valves.State.closed),
                    (200.0, 12, valves.State.closed),
                    (210.0, 12, valves.State.closed),
                ]
            ],
        )
        fluidic_line_to_pump_mapping = {7: 1, 12: 1}
        pump_start_stop_margin_mm = 1
        pump_dispense_axis_ranges, line_indexes = (
            get_pump_dispense_axis_range_from_routine(
                routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
            )
        )

        self.assertIsNotNone(pump_dispense_axis_ranges)
        if pump_dispense_axis_ranges is not None:
            self.assertDictEqual(
                pump_dispense_axis_ranges,
                {
                    1: (99.0, 211.0),
                },
            )
        self.assertListEqual(sorted(line_indexes), sorted([7, 12]))

    def test_pump_dispense_axis_range_from_movement_range_forward(self):
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(
                    positionThreshold=threshold,
                    state=valves.State(
                        valves=[
                            valves.State.Valve(
                                identifier=valves.State.ValveIdentifier(
                                    fluidicLine=line
                                ),
                                state=state,
                            )
                        ]
                    ),
                )
                for threshold, line, state in [
                    (200.0, 1, valves.State.open),
                    (203.0, 4, valves.State.open),
                    (205.0, 1, valves.State.closed),
                    (208.0, 4, valves.State.closed),
                ]
            ],
        )
        fluidic_line_to_pump_mapping = {1: 6, 4: 9}
        movement_range = (Coordinate(111.0, 200.0), Coordinate(111.0, 208.0))
        movement_axis = Axis.y
        pump_dispense_axis_ranges, line_indexes = (
            get_pump_dispense_axis_range_from_movement_range(
                routine, movement_range, movement_axis, fluidic_line_to_pump_mapping
            )
        )

        self.assertIsNotNone(pump_dispense_axis_ranges)
        if pump_dispense_axis_ranges is not None:
            self.assertDictEqual(
                pump_dispense_axis_ranges,
                {
                    6: (200.0, 208.0),
                    9: (200.0, 208.0),
                },
            )
        self.assertListEqual(line_indexes, [1, 4])

    def test_pump_dispense_axis_range_from_movement_range_backward(self):
        routine = Routine(
            direction=Routine.Direction.forward,
            positionThresholdToStateMapping=[
                Routine.Item(
                    positionThreshold=threshold,
                    state=valves.State(
                        valves=[
                            valves.State.Valve(
                                identifier=valves.State.ValveIdentifier(
                                    fluidicLine=line
                                ),
                                state=state,
                            )
                        ]
                    ),
                )
                for threshold, line, state in [
                    (150.0, 3, valves.State.open),
                    (142.0, 3, valves.State.closed),
                    (132.0, 9, valves.State.open),
                    (128.0, 9, valves.State.closed),
                    (122.0, 9, valves.State.open),
                    (118.0, 9, valves.State.closed),
                ]
            ],
        )
        fluidic_line_to_pump_mapping = {3: 1, 9: 2}
        movement_range = (Coordinate(111.0, 150.0), Coordinate(111.0, 118.0))
        movement_axis = Axis.y
        pump_dispense_axis_ranges, line_indexes = (
            get_pump_dispense_axis_range_from_movement_range(
                routine, movement_range, movement_axis, fluidic_line_to_pump_mapping
            )
        )

        self.assertIsNotNone(pump_dispense_axis_ranges)
        if pump_dispense_axis_ranges is not None:
            self.assertDictEqual(
                pump_dispense_axis_ranges,
                {
                    1: (150.0, 118.0),
                    2: (150.0, 118.0),
                },
            )
        self.assertListEqual(sorted(line_indexes), [3, 9])
