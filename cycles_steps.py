from elementaryFunctions import *
from excelRead import *
import copy

quadrant_nb=4

def multi_dispense_in_wells(hardware,lines_volumes_wells_dict,is384=0,max_vol=None):
    '''

    :param hardware: connection to the prototype's hardware

    :param lines_volumes_wells_dict: dictionnary with keys correponding to lines, and values being a list of 2 parameters:
    the volume to dispense, and the wells to dispense in
    example : {"DB":[50,[1,2,3,4,5,6,7,8]} dispenses 50ul in wells 1,2,3,4,5,6,7 and 8
    The first parameter can be a list of 12 (or 24 for 384) values, corresponding to each column
    example : {"DB":[[25,50,25,50,25,50,25,50,25,50,25,50],wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12)}
    dispenses alternatively 25 and 50ul of DB in the whole plate

    :param is384: 0 if 96 well plate, 1 if 384
    :param max_vol: the maximum volume to be dispensed in a single dispense
    :return:
    '''


    'Copy of the dictionnary to pop the wells as we dispense them'
    lines_volumes_wells_copy = copy.deepcopy(lines_volumes_wells_dict)

    'Each nozzle represented by [row,column,nb of nozzles] compared to the first one when looking at dispense head like a plate'
    dispense_head = {"M": [0, 0, 1],
                     "N": [1, 0, 1],
                     "A": [2, 1, 1],
                     "C": [3, 1, 1],
                     "G": [4, 1, 1],
                     "T": [5, 1, 1],
                     "O": [2, 0, 1],
                     "P": [3, 0, 1],
                     "Q": [4, 0, 1],
                     "DB": [6, -1, 4],
                     "BB": [6, 0, 4],
                     "Buff1": [6, 1, 4],
                     "Buff2": [6, 2, 4]
                     }

    dispense_head_max_col = max([coord[1] for coord in dispense_head.values()])
    dispense_head_min_col = min([coord[1] for coord in dispense_head.values()])
    dispense_head_col_nb = dispense_head_max_col - dispense_head_min_col + 1

    dispense_head_max_row = max([coord[0] for coord in dispense_head.values()])
    dispense_head_min_row = min([coord[0] for coord in dispense_head.values()])
    dispense_head_row_nb = dispense_head_max_row - dispense_head_min_row + 1

    if is384:
        dispense_head_max_col *= 2
        dispense_head_min_col *= 2

        dispense_head_max_row *= 2
        dispense_head_min_row *= 2

        dispense_head_row_nb *= 2
        dispense_head_col_nb *= 2
        real_plate_dims = [16,24]
    else:
        real_plate_dims = [8,12]

    dispHead_dims = [dispense_head_row_nb, dispense_head_col_nb]


    'fake_plate_dims corresponds to the plate that the first nozzle needs to go through so that each nozzle has a chance to shoot'

    fake_plate_dims = [real_plate_dims[0] + 2 * (dispense_head_row_nb - 1), real_plate_dims[1] + 2 * (dispense_head_col_nb - 1)]

    for col in range(0 - dispense_head_min_col, fake_plate_dims[1] - (dispense_head_max_col) +1 , 1):

        for first_well in range(1 - dispense_head_min_row + fake_plate_dims[0] * col, 1 + fake_plate_dims[0] * (col+1) - dispense_head_max_row , 1):

            dispense_dict={}
            for line in lines_volumes_wells_copy.keys():
                if is384:
                    well = first_well + 2 * dispense_head[line][0] + fake_plate_dims[0] * 2 * dispense_head[line][1]
                else:
                    well = first_well + dispense_head[line][0] + fake_plate_dims[0] * dispense_head[line][1]

                real_well = fake_plate_well_to_real_well(well, real_plate_dims, fake_plate_dims, dispHead_dims)

                nozzle_nb = dispense_head[line][2]
                real_wells_all_nozzles=[]
                for well_offset in range(nozzle_nb):
                    if is384:
                        real_wells_all_nozzles.append(real_well + 2 * well_offset)
                        accepted_modulos=[0,1]
                        division_factor = nozzle_nb * 2

                    else:
                        real_wells_all_nozzles.append(real_well + well_offset)
                        accepted_modulos = [0]
                        division_factor = nozzle_nb

                if ((real_well-1) % division_factor in accepted_modulos) and any(well_to_dispense in lines_volumes_wells_copy[line][1] for well_to_dispense in real_wells_all_nozzles):
                    #We check if we want different volumes per column for this reagent
                    if isinstance(lines_volumes_wells_copy[line][0], list):
                        column_real_well = (real_well-1) // real_plate_dims[0] + 1
                        dispense_dict[line] = lines_volumes_wells_copy[line][0][column_real_well-1] * nozzle_nb
                    else:
                        dispense_dict[line] = lines_volumes_wells_copy[line][0] * nozzle_nb

                    for well_to_remove in real_wells_all_nozzles:
                        if well_to_remove in lines_volumes_wells_copy[line][1]:
                            lines_volumes_wells_copy[line][1].remove(well_to_remove)

            if dispense_dict!={}:
                if is384:
                    goToFakeWell(hardware, first_well, fake_plate_dims, dispHead_dims, 5, X_step=X_step/2, Y_step=Y_step/2)
                else:
                    goToFakeWell(hardware, first_well, fake_plate_dims, dispHead_dims, 0)
                multi_dispense(hardware, dispense_dict, max_vol)

            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)



def removeSupernatant(hardware,vacuumTime):

    goToWell(hardware, 'thermalCamera', 1,0)

    hardware.vacValveOpen()

    wait(hardware, vacuumTime)
    hardware.vacValveClose()

    wait(hardware, 3)


def fillPlate(hardware, buffer, vol, is384, max_vol=None):

    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet(path)
    getParameters(synthesis_sheet)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    if buffer=="nucs":
        dispensePumps(hardware, [vol]*8,
                      nucleo_arrays[5], nucleo_arrays[6],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[],[], is384, max_vol)
    else:
        dispenseWashes(hardware,vol,buffer,activeWells,is384)


def updateCycleLabel(hardware,cycle,step):
    print("Cycle " + str(cycle) + " " + step)
    hardware.parent.leftFrame.cycleLabelString.set("Cycle " + str(cycle) + " " + step)

def upperThreshold(wellList,threshold):
    return [well for well in wellList if well>=threshold]

def underThreshold(wellList,threshold):
    return [well for well in wellList if well<threshold]

def wellListFromHalfColumns(halfColsList):

    wellList=[]
    for halfCol in halfColsList:
        wellList.append((halfCol-1)*4+1)
        wellList.append((halfCol-1)*4+2)
        wellList.append((halfCol-1)*4+3)
        wellList.append((halfCol-1)*4+4)
    return wellList

def wellListFromColumns(ColsList):

    wellList=[]
    for Col in ColsList:
        wellList.append((Col-1)*8+1)
        wellList.append((Col-1)*8+2)
        wellList.append((Col-1)*8+3)
        wellList.append((Col-1)*8+4)
        wellList.append((Col-1)*8+5)
        wellList.append((Col-1)*8+6)
        wellList.append((Col-1)*8+7)
        wellList.append((Col-1)*8+8)
    return wellList

def wellListFromColumns_384(ColsList):

    wellList=[]
    for col in ColsList:
        wellList=wellList+(list(range((col-1)*16+1,(col)*16+1)))
    return wellList

def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())

if __name__ == "__main__":
    print(wellListFromColumns_384([1,2]))

