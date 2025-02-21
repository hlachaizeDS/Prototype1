from hardware.mga.testbench_hardware import MGATestbenchHardware
from hardware.mga.movement import Coordinate

test_hardware = MGATestbenchHardware(None, mock_components=True, on_machine=True)


def test_dispense():
    all_wells= [i for i in range(1, 385)]

    left_wells = [i for i in range(1, 193)]
    right_wells = [i for i in range(193, 385)]

    checkered_positive = [
        i for i in range(1, 385) if (i - 1) % 16 % 2 == (i - 1) // 16 % 2
    ]
    checkered_negative = [
        i for i in range(1, 385) if (i - 1) % 16 % 2 != (i - 1) // 16 % 2  
    ]

    test_hardware.initialisation()
    test_hardware.dispense(
        volume_per_line={
            # "T": (25, checkered_positive),
            # "A": (12, checkered_negative),
            # "EB": (25, left_wells),
            # "DB": (25, all_wells),
            # "C": (12, left_wells),
            "A": (12, left_wells),
            # "G": (12, right_wells),
            "T": (12, right_wells),
        }
    )
    test_hardware.move_to(Coordinate(x=0.0, y=0.0))
