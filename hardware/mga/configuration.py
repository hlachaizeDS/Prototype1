from dataclasses import dataclass
from enum import Enum
from hardware.mga.types import (
    Coordinate,
    Well,
    LineIndex,
    PumpIndex,
    Direction,
    LineConfiguration,
)

###########################################################
############ IMPORTANT: ALL INDEXES START AT 1 ############
###########################################################


# mappings
LineToPumpMapping = dict[LineIndex, PumpIndex]
FluidicLineIndexToPumpIndexMapping: LineToPumpMapping = {
    1: 7,
    2: 8,
    3: 1,
    7: 6,
    8: 2,
    9: 3,
    10: 4,
    11: 5,
    12: 6,
}


ReagentToLineMapping = dict[str, LineIndex | dict[Direction, LineIndex]]
ReagentToFluidicLineIndexMapping: ReagentToLineMapping = {
    "EB": {
        Direction.forward: 12,
        Direction.backward: 7,
    },
    "DB": 1,
    "Buff1": 2,
    "A": 8,
    "C": 9,
    "G": 10,
    "T": 11,
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


DefaultGeometry = Geometry(
    reference=Reference(
        position=Coordinate(126.66, 162.99),
        # the following values should not be modified
        line_index=1,
        nozzle_index=1,
        well=Well(row=7, column=1),
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
    index: LineConfiguration(open_offset=0, close_offset=0) for index in range(1, 13)
}


@dataclass
class PumpDynamics:
    acceleration: float = 5000.0  # µl/s²
    deceleration: float = 5000.0  # µl/s²
    speed = 500.0  # µl/s


PumpDynamicsMapping: dict[PumpIndex, PumpDynamics] = {
    index: PumpDynamics() for index in range(1, 9)
}


@dataclass
class ValveParameters:
    open_time_per_ul: float  # ms/µl


DefaultValveParameters = ValveParameters(open_time_per_ul=2.0)


class Axis(Enum):
    x = 0
    y = 1


@dataclass
class AxisDynamics:
    acceleration: float  # mm/s²
    deceleration: float  # mm/s²
    speed: float | None  # mm/s


@dataclass
class GantryParameters:
    axes: dict[Axis, AxisDynamics]


DefaultGantryParameters = GantryParameters(
    axes={
        # speed is determined by pump speed and valve opening time
        Axis.x: AxisDynamics(acceleration=100.0, deceleration=100.0, speed=100.0),
        Axis.y: AxisDynamics(acceleration=100.0, deceleration=100.0, speed=100.0),
    }
)

PumpMaxVolume = 5000.0  # µl
PumpSlack = 50.0  # µl
