from hardware.mga.testbench_hardware import MGATestbenchHardware
from hardware.mga.movement import Coordinate

test_hardware = MGATestbenchHardware(None, mock_components=True, on_machine=True)


def test_dispense():
    all_wells= [i for i in range(1, 385)]
    test_hardware.initialisation()
    test_hardware.dispense(
        volume_per_line={
            # "EB": (12.5, all_wells),
            "DB": (12.5, all_wells),
            # "A": (12, all_wells),
            # "C": (12, all_wells),
            # "G": (12, all_wells),
            # "T": (12, all_wells),
        }
    )
    test_hardware.move_to(Coordinate(x=0.0, y=0.0))
