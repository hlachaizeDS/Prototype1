import grpc
from concurrent import futures
from mga_testbench_interface.generated import gantry_pb2_grpc
from mga_testbench_interface.generated import gantry_pb2


class GantryServicer(gantry_pb2_grpc.GantryServicer):
    def __init__(self):
        pass

    def getPosition(self, request, context):
        print("getPosition called")
        return gantry_pb2.Position(x=10, y=20)

    def moveTo(self, request, context):
        print("moveTo called")
        return gantry_pb2.Position(x=0, y=0)

    def setParameters(self, request: gantry_pb2.AxisParameters, context):
        print("setParameters called with ", request)
        return gantry_pb2.GantryStatus(
            isBusy=False,
            initialized=True,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    gantry_pb2_grpc.add_GantryServicer_to_server(GantryServicer(), server)

    server.add_insecure_port("[::]:7050")
    server.start()
    print("Server started at localhost:7050")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
