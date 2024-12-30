from hardware.mga.testbench_hardware import MGATestbenchHardware

test_hardware = MGATestbenchHardware(None, mock_components=True)


def test_initialisation():
    # Create a new instance of the class
    # Call the method
    test_hardware.initialisation()
    test_hardware.dispense(
        volume_per_line={
            "EB": (50, [i for i in range(16)]),
        }
    )


def _do_no_testtest_get_positions():
    # Call the method
    test_hardware.print_positions()
