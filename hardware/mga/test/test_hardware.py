from hardware.mga.testbench_hardware import MGATestbenchHardware
from mga_testbench_interface.generated.gantry_pb2_grpc import GantryServicer

test_hardware = MGATestbenchHardware(None)

def test_initialisation():
    # Create a new instance of the class
    # Call the method
    test_hardware.initialisation()

def test_get_positions():
    # Call the method
    test_hardware.print_positions()

