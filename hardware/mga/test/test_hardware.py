from hardware.mga.testbench_hardware import MGATestbenchHardware
from hardware.mga.movement import Coordinate

test_hardware = MGATestbenchHardware(None, mock_components=True, on_machine=True)


def test_dispense():
    all_wells= [i for i in range(1, 385)]

    left_wells = [i for i in range(1, 65)]
    right_wells = [i for i in range(65, 129)]

    test_hardware.initialisation()
    test_hardware.dispense(
        volume_per_line={
            # "EB": (12.5, all_wells),
            # "DB": (12.5, all_wells),
            "A": (25, left_wells),
            "C": (25, right_wells),
            # "G": (12, all_wells),
            # "T": (25, right_wells),
        }
    )
    test_hardware.move_to(Coordinate(x=0.0, y=0.0))
