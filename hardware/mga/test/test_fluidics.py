import unittest
from hardware.mga.fluidics import (
    get_pump_dispense_axis_start_stop_positions,
    estimate_volume_usage,
)
from hardware.mga.types import Routine
import mga_testbench_interface.generated.valves_pb2 as valves


class TestFluidics(unittest.TestCase):
    def test_get_movement_range_coordinates_forward(self):
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
        pump_positions, line_indexes = get_pump_dispense_axis_start_stop_positions(
            routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
        )

        self.assertIsNotNone(pump_positions)
        if pump_positions is not None:
            self.assertDictEqual(
                pump_positions,
                {
                    6: (199.0, 206.0),
                    9: (202.0, 209.0),
                },
            )
        self.assertListEqual(line_indexes, [1, 4])

    def test_get_movement_range_coordinates_backward(self):
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
        pump_positions, line_indexes = get_pump_dispense_axis_start_stop_positions(
            routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
        )

        self.assertIsNotNone(pump_positions)
        if pump_positions is not None:
            self.assertDictEqual(
                pump_positions,
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

    def test_get_movement_range_coordinates_two_lines_one_pump(self):
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
            pump_positions, line_indexes = get_pump_dispense_axis_start_stop_positions(
                routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
            )

            self.assertIsNotNone(pump_positions)
            if pump_positions is not None:
                self.assertDictEqual(
                    pump_positions,
                    {
                        1: (99.0, 211.0),
                    },
                )
            self.assertListEqual(sorted(line_indexes), sorted([7, 12]))