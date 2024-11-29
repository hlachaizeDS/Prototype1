from dataclasses import dataclass
from enum import Enum
from hardware.mga.types import Coordinate, Well, LineIndex, PumpIndex, Direction, LineConfiguration



# mappings
FluidicLineIndexToPumpIndexMapping: dict[LineIndex, PumpIndex] = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 0,
}

ReagentToLineMapping = dict[str, LineIndex | dict[Direction, LineIndex]]
ReagentToFluidicLineIndexMapping: ReagentToLineMapping = {
    "EB": {
        Direction.forward: 0,
        Direction.backward: 5,
    },  # make sure this aligns with StandardDispenseTrips in dispense.py
    "A": 1,
    "C": 2,
    "G": 3,
    "T": 4,
    "M": 6,
    "N": 7,
    "O": 8,
    "P": 9,
    "Q": 10,
    "R": 11,
}


@dataclass
class Reference:
    position: Coordinate
    line_index: LineIndex
    nozzle_index: int
    well: Well


# parameters
@dataclass
class Geometry:
    reference: Reference
    inter_well_spacing_mm: float
    number_of_lines_in_manifold: int
    number_of_manifolds: int
    inter_line_spacing_wells: int
    x_inter_nozzle_spacing_wells_in_line: float
    y_inter_nozzle_spacing_wells_in_line: int
    number_of_nozzles_per_line: int
    number_of_rows: int
    number_of_columns: int


StandardGeometry = Geometry(
    reference=Reference(
        position=Coordinate(0, 0),
        line_index=0,
        nozzle_index=3,
        well=Well(row=6, column=0),
    ),
    inter_well_spacing_mm=4.5,
    number_of_lines_in_manifold=6,
    number_of_manifolds=2,
    inter_line_spacing_wells=2,
    x_inter_nozzle_spacing_wells_in_line=2 / 9,
    y_inter_nozzle_spacing_wells_in_line=2,
    number_of_nozzles_per_line=4,
    number_of_rows=16,
    number_of_columns=24,
)


LineConfigurations: dict[LineIndex, LineConfiguration] = {
    index: LineConfiguration(open_offset=0, close_offset=0) for index in range(12)
}


@dataclass
class PumpDynamics:
    acceleration = 5000.0  # µl/s²
    deceleration = 5000.0  # µl/s²
    speed = 500.0  # µl/s


PumpDynamicsMapping: dict[PumpIndex, PumpDynamics] = {
    index: PumpDynamics() for index in range(11)
}


@dataclass
class ValveParameters:
    open_time_per_ul = 2.0  # ms/µl


class Axis(Enum):
    x = 0
    y = 1


@dataclass
class AxisDynamics:
    acceleration = 100.0  # mm/s²
    deceleration = 100.0  # mm/s²
    # speed is determined by pump speed and valve opening time


@dataclass
class GantryParameters:
    axes: dict[Axis, AxisDynamics]


MovementMargin = Coordinate(0.5, 0.0)
