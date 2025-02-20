from dataclasses import dataclass
import mga_testbench_interface.generated.valves_pb2 as valves

Row = int  # starts from 0
LineIndex = int  # starts from 0
NozzleIndex = int  # starts from 0
Direction = valves.Routine.Direction
ValveState = valves.State.ValveState
Routine = valves.Routine
Volume = float


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class Well:
    row: int
    column: int

    def __init__(
        self,
        index: int | None = None,
        row: int | None = None,
        column: int | None = None,
    ):
        if index is not None:
            self.row = ((index - 1) % 16) + 1
            self.column = ((index - 1) // 16) + 1
        elif row is not None and column is not None:
            self.row = row
            self.column = column
        else:
            raise ValueError("Either index or row and column must be provided")


@dataclass
class Alignment:
    line_index: LineIndex
    nozzle_index: NozzleIndex
    row: Row


@dataclass
class LineConfiguration:
    open_offset: float  # % of inter-nozzle spacing
    close_offset: float  # % of inter-nozzle spacing


PumpIndex = int
DispensePlan = dict[LineIndex, list[Well]]
ReagentVolumeWells = dict[str, tuple[float, list[int]]]

ValveType = valves.State.ValveIdentifier.Type

@dataclass(frozen=True)
class Valve:
    type: ValveType
    fluidicLine: int
    id: int = 0

ValveStates = dict[LineIndex, dict[Valve, valves.State.ValveState]]

MovementRange = tuple[Coordinate, Coordinate]