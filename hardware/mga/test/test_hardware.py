from hardware.mga.testbench_hardware import MGATestbenchHardware

test_hardware = MGATestbenchHardware(None, mock_components=True)


def test_dispense():
    # Create a new instance of the class
    # Call the method
    test_hardware.initialisation()
    test_hardware.dispense(
        volume_per_line={
            "A": (12, [i for i in range(1, 384 + 1)]),
        }
    )
