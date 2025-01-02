import grpc
from concurrent import futures
from mga_testbench_interface.generated import gantry_pb2_grpc
from mga_testbench_interface.generated import gantry_pb2
from mga_testbench_interface.generated import valves_pb2_grpc
from mga_testbench_interface.generated import valves_pb2
from mga_testbench_interface.generated import pumps_pb2_grpc
from mga_testbench_interface.generated import pumps_pb2


class GantryServicer(gantry_pb2_grpc.GantryServicer):
    parameters: gantry_pb2.AxisParameters

    def __init__(self):
        pass

    def home(self, request, context):
        print("gantry home called", request)
        return gantry_pb2.GantryStatus(
            isBusy=False,
            initialized=True,
        )

    def getPosition(self, request, context):
        print("gantry getPosition called")
        return gantry_pb2.Position(x=10, y=20)

    def moveTo(self, request, context):
        print("gantry moveTo called")
        return gantry_pb2.GantryStatus(
            isBusy=True,
            initialized=True,
        )

    def setParameters(self, request: gantry_pb2.AxisParameters, context):
        print("gantry setParameters called with", request)
        self.parameters = request
        return gantry_pb2.GantryStatus(
            isBusy=False,
            initialized=True,
        )

    def getParameters(self, request, context):
        print("gantry getParameters called")
        return self.parameters

    def getStatus(self, request, context):
        return gantry_pb2.GantryStatus(
            isBusy=False,
            initialized=True,
        )


class ValvesServicer(valves_pb2_grpc.ValvesServicer):
    def __init__(self):
        pass

    def initialize(self, request, context):
        print("valves initialize called")
        return valves_pb2._()

    def setRoutine(self, request, context):
        print("valves setRoutine called")
        return valves_pb2.ValveStatus(
            routine=valves_pb2.ValveStatus.RoutineStatus.stopped
        )

    def startRoutine(self, request, context):
        print("valves startRoutine called")
        return valves_pb2.ValveStatus(
            routine=valves_pb2.ValveStatus.RoutineStatus.running
        )

    def stopRoutine(self, request, context):
        print("valves stopRoutine called")
        return valves_pb2.ValveStatus(
            routine=valves_pb2.ValveStatus.RoutineStatus.stopped
        )

    def setState(self, request, context):
        print("valves setState called", request)
        return valves_pb2.State(valves=[])


class PumpsServicer(pumps_pb2_grpc.PumpsServicer):
    initialized = False
    pumpMarks: list[float] = []

    def __init__(self):
        pass

    def home(self, request: pumps_pb2.PumpIndexes, context):
        print("pumps home called", request)
        self.pumpMarks = [0 for _ in range(11)]
        self.initialized = True
        return self._statuses(isBusy=False)

    def getStatuses(self, request, context):
        print("pumps getStatuses called", request)
        return self._statuses(isBusy=False)

    def moveTo(self, request: pumps_pb2.PumpMoves, context):
        print("pumps moveTo called", request)
        for pump in request.pumps:
            self.pumpMarks[pump.index.value - 1] = pump.volumeMark
        return self._statuses(isBusy=True)

    def stop(self, request, context):
        print("pumps stop called", request)
        return self._statuses(isBusy=False)

    def setParameters(self, request, context):
        print("pumps setParameters called", request)
        return self._statuses(isBusy=False)

    def _statuses(self, isBusy: bool):
        return pumps_pb2.Statuses(
            pumps=[
                pumps_pb2.Statuses.PumpStatus(
                    index=pumps_pb2.PumpIndex(value=index + 1),
                    isBusy=isBusy,
                    initialized=self.initialized,
                    errorCode=0,
                    errorMessage="",
                )
                for index in range(11)
            ]
        )

    def getVolumeMarks(self, request, context):
        print("pumps getVolumeMarks called", request)
        return pumps_pb2.VolumeMarks(
            pumps=[
                pumps_pb2.VolumeMarks.VolumeMark(
                    index=pumps_pb2.PumpIndex(value=index + 1), value=value
                )
                for index, value in enumerate(self.pumpMarks)
            ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    gantry_pb2_grpc.add_GantryServicer_to_server(GantryServicer(), server)
    valves_pb2_grpc.add_ValvesServicer_to_server(ValvesServicer(), server)
    pumps_pb2_grpc.add_PumpsServicer_to_server(PumpsServicer(), server)

    server.add_insecure_port("[::]:7050")
    server.start()
    print("Server started at localhost:7050")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
