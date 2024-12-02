import unittest
from hardware.mga.fluidics import get_pump_start_stop_positions
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
        fluidic_line_to_pump_mapping = {0: 5, 3: 8}
        pump_start_stop_margin_mm = 1
        pump_positions = get_pump_start_stop_positions(
            routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
        )

        self.assertIsNotNone(pump_positions)
        if pump_positions is not None:
            self.assertDictEqual(
                pump_positions,
                {
                    5: (199.0, 206.0),
                    8: (202.0, 209.0),
                },
            )

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
        fluidic_line_to_pump_mapping = {2: 0, 8: 1}
        pump_start_stop_margin_mm = 1
        pump_positions = get_pump_start_stop_positions(
            routine, fluidic_line_to_pump_mapping, pump_start_stop_margin_mm
        )

        self.assertIsNotNone(pump_positions)
        if pump_positions is not None:
            self.assertDictEqual(
                pump_positions,
                {
                    0: (151.0, 141.0),
                    1: (133.0, 117.0),
                },
            )