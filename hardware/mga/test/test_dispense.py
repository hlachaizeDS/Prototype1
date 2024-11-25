from hardware.mga.dispense import multi_dispense_map_to_routine, Well


def test_dispense_multi_dispense_map_to_routine():
    wells: list[Well] = []
    for row in range(16):
        for column in range(24):
            wells.append(Well(row, column))

    volumes = {
        0: (50.0, wells),
        5: (50.0, wells),
    }
    routine = multi_dispense_map_to_routine(0, 100, 25, 0, volumes)

    for item in routine.positionThresholdToStateMapping:
        print(item.positionThreshold)
        for valve in item.state.valves:
            print(
                f"\t{valve.identifier.fluidicLine}.{valve.identifier.id} -> {'open' if valve.state == 0 else 'closed'}"
            )
    pass
