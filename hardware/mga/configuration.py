from dataclasses import dataclass

@dataclass
class Geometry:
    reference_position = 0.0  # position at which 1.1 is centered over G1
    inter_well_spacing = 4.5  # distance between two wells
    number_of_lines_in_manifold = 6
    number_of_manifolds = 2
    inter_line_spacing_wells = 2
    x_inter_nozzle_spacing_wells_in_line = 2 / 9
    y_inter_nozzle_spacing_wells_in_line = 2
    number_of_nozzles_per_line = 4
    number_of_rows = 16
    number_of_columns = 24