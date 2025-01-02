from hardware.mga.testbench_hardware import MGATestbenchHardware
from hardware.mga.movement import Coordinate
import datetime

test_hardware = MGATestbenchHardware(None, mock_components=True)


def test_dispense():
    # Create a new instance of the class
    # Call the method
    test_hardware.initialisation()
    test_hardware.dispense(
        volume_per_line={
            "EB": (12, [i for i in range(1, 384 + 1)]),
        }
    )
    test_hardware.move_to(Coordinate(x=0.0, y=0.0))
