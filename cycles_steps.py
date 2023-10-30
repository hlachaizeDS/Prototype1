from elementaryFunctions import *
from excelRead import *

quadrant_nb=4


def dispensePumps(hardware,volumes,M_array,N_array,A_array,C_array,G_array,T_array,O_array,P_array,is384,max_vol=None):

    pump_nb=8

    wellArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy(),O_array.copy(),P_array.copy()]
    'we loop for every position possible'
    dispHead_dims=[6,2] # 6 rows lines, 2 columns, when looking at it like the plate
    fake_plate_dims=[8 + 2*(dispHead_dims[0] - 1), 12 + 2*(dispHead_dims[1] - 1)] # only for first nozzle

    for col in range(0,fake_plate_dims[1] - (dispHead_dims[1]-1),1):
        for m_well in range(1 + fake_plate_dims[0]  * col, 1 + fake_plate_dims[0]  * (col+1) - (dispHead_dims[0] - 1), 1):
            n_well= m_well + 1
            o_well= m_well + 2
            p_well= m_well + 3
            a_well= m_well + 2 + fake_plate_dims[0] * 1
            c_well= m_well + 3 + fake_plate_dims[0] * 1
            g_well= m_well + 4 + fake_plate_dims[0] * 1
            t_well= m_well + 5 + fake_plate_dims[0] * 1
            wells= [m_well,n_well,a_well,c_well,g_well,t_well,o_well,p_well]
            disp=[0] * pump_nb #Flag to know if we should dispense
            for nozzle in range(pump_nb):
                if fake_plate_well_to_real_well(wells[nozzle], fake_plate_dims, dispHead_dims) in wellArrays[nozzle]:
                    disp[nozzle]=volumes[nozzle]
                    wellArrays[nozzle].remove(fake_plate_well_to_real_well(wells[nozzle], fake_plate_dims, dispHead_dims))
            if any(vol!=0 for vol in disp ):
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToFakeWell(hardware, m_well, fake_plate_dims, dispHead_dims, i)
                        multiDispensePumps(hardware,disp,max_vol)
                else:
                    goToFakeWell(hardware, m_well, fake_plate_dims, dispHead_dims, 0)
                    multiDispensePumps(hardware,disp,max_vol)
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispensePumps_384(hardware,volumes,M_array,N_array,A_array,C_array,G_array,T_array,O_array,P_array,max_vol=None):

    pump_nb=8

    wellArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy(),O_array.copy(),P_array.copy()]
    'we loop for every position possible'
    dispHead_dims=[12,4] # 6 rows lines, 2 columns, when looking at it like the plate
    fake_plate_dims=[16 + 2*(dispHead_dims[0] - 1), 24 + 2*(dispHead_dims[1] - 1)] # only for first nozzle

    for col in range(0,fake_plate_dims[1] - (dispHead_dims[1]-1),1):
        for m_well in range(1 + fake_plate_dims[0]  * col, 1 + fake_plate_dims[0]  * (col+1) - (dispHead_dims[0] - 1), 1):
            n_well= m_well + 2
            o_well= m_well + 4
            p_well= m_well + 6
            a_well= m_well + 4 + fake_plate_dims[0] * 2
            c_well= m_well + 6 + fake_plate_dims[0] * 2
            g_well= m_well + 8 + fake_plate_dims[0] * 2
            t_well= m_well + 10 + fake_plate_dims[0] * 2
            wells= [m_well,n_well,a_well,c_well,g_well,t_well,o_well,p_well]
            disp=[0] * pump_nb #Flag to know if we should dispense
            for nozzle in range(pump_nb):
                if fake_plate_well_to_real_well(wells[nozzle], fake_plate_dims, dispHead_dims) in wellArrays[nozzle]:
                    disp[nozzle]=volumes[nozzle]
                    wellArrays[nozzle].remove(fake_plate_well_to_real_well(wells[nozzle], fake_plate_dims, dispHead_dims))
            if any(vol!=0 for vol in disp ):
                goToFakeWell(hardware, m_well, fake_plate_dims, dispHead_dims, 0)
                multiDispensePumps(hardware,disp,max_vol)
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispensePumpsDiffCols(hardware,volumesPerCol,M_array,N_array,A_array,C_array,G_array,T_array,O_array,P_array,is384):

    pump_nb=8

    wellArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy(),O_array.copy(),P_array.copy()]
    'we loop for every position possible'
    dispHead_dims=[6,2] # 6 rows lines, 2 columns, when looking at it like the plate
    fake_plate_dims=[8 + 2*(dispHead_dims[0] - 1), 12 + 2*(dispHead_dims[1] - 1)] # only for first nozzle

    for col in range(0,fake_plate_dims[1] - (dispHead_dims[1]-1),1):
        for m_well in range(1 + fake_plate_dims[0]  * col, 1 + fake_plate_dims[0]  * (col+1) - (dispHead_dims[0] - 1), 1):
            n_well= m_well + 1
            o_well= m_well + 2
            p_well= m_well + 3
            a_well= m_well + 2 + fake_plate_dims[0] * 1
            c_well= m_well + 3 + fake_plate_dims[0] * 1
            g_well= m_well + 4 + fake_plate_dims[0] * 1
            t_well= m_well + 5 + fake_plate_dims[0] * 1
            wells= [m_well,n_well,a_well,c_well,g_well,t_well,o_well,p_well]
            disp=[0] * pump_nb #Flag to know if we should dispense
            for nozzle in range(pump_nb):
                real_well=fake_plate_well_to_real_well(wells[nozzle], fake_plate_dims, dispHead_dims)
                real_column=((real_well-1)//8)+1
                if real_well in wellArrays[nozzle]:
                    disp[nozzle]=volumesPerCol[real_column-1]
                    wellArrays[nozzle].remove(real_well)
            if any(vol!=0 for vol in disp ):
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToFakeWell(hardware, m_well, fake_plate_dims, dispHead_dims, i)
                        multiDispensePumps(hardware,disp)
                else:
                    goToFakeWell(hardware, m_well, fake_plate_dims, dispHead_dims, 0)
                    multiDispensePumps(hardware,disp)
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseWashes(hardware,volume,solution,array,is384):

    washArray=array.copy()
    if solution=="BB":
        disp_pattern=[0,0,0,0,0,0,0,0,0,volume*4,0,0]
    if solution=="DB":
        disp_pattern=[0,0,0,0,0,0,0,0,volume*4,0,0,0]
    if solution=="Buff1":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,volume*4,0]
    if solution=="Buff2":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,0,volume*4]

    for col in range(0, 12, 1):
        #Let's find the smallest and largest well in the column
        smallest_well=96
        largest_well=0
        for washWell in washArray:
            if washWell>=col*8+1 and washWell<col*8+9:
                if washWell>largest_well:
                    largest_well=washWell
                if washWell<smallest_well:
                    smallest_well=washWell
        if smallest_well!=96 or largest_well!=0: #meaning if there is a non empty well in the column
            #Either we can dispense only once
            if largest_well-smallest_well<4:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, min(smallest_well, col * 8 + 5), i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    multiDispensePumps(hardware, disp_pattern)
            else:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseWashesColDiffVols(hardware,volPerCol,solution,array,is384):

    washArray=array.copy()

    for col in range(0, 12, 1):
        if solution == "BB":
            disp_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, volPerCol[col] * 4, 0, 0]
        if solution == "DB":
            disp_pattern = [0, 0, 0, 0, 0, 0, 0, 0, volPerCol[col] * 4, 0, 0, 0]
        if solution == "Buff1":
            disp_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, volPerCol[col] * 4, 0]
        if solution == "Buff2":
            disp_pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, volPerCol[col] * 4]

        #Let's find the smallest and largest well in the column
        smallest_well=96
        largest_well=0
        for washWell in washArray:
            if washWell>=col*8+1 and washWell<col*8+9:
                if washWell>largest_well:
                    largest_well=washWell
                if washWell<smallest_well:
                    smallest_well=washWell
        if smallest_well!=96 or largest_well!=0: #meaning if there is a non empty well in the column
            #Either we can dispense only once
            if largest_well-smallest_well<4:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, min(smallest_well, col * 8 + 5), i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    multiDispensePumps(hardware, disp_pattern)
            else:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseDoubleWashes_Buff2(hardware,volume,solution,array,is384):

    washArray=array.copy()
    if solution=="BB":
        disp_pattern=[0,0,0,0,0,0,0,0,0,volume*4,0,0]
    if solution=="DB":
        disp_pattern=[0,0,0,0,0,0,0,0,volume*4,0,0,0]
    if solution=="Buff1":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,volume*4,0]
    if solution=="Buff2":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,volume*4,volume*4]

    for col in range(0, 12, 1):
        #Let's find the smallest and largest well in the column
        smallest_well=96
        largest_well=0
        for washWell in washArray:
            if washWell>=col*8+1 and washWell<col*8+9:
                if washWell>largest_well:
                    largest_well=washWell
                if washWell<smallest_well:
                    smallest_well=washWell
        if smallest_well!=96 or largest_well!=0: #meaning if there is a non empty well in the column
            #Either we can dispense only once
            if largest_well-smallest_well<4:
                if is384:
                    for i in range(1,5):
                        goToWell(hardware, solution, min(smallest_well, col * 8 + 5), i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    multiDispensePumps(hardware, disp_pattern)
            else:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseDoubleWashes_Buff1(hardware,volume,solution,array,is384):

    washArray=array.copy()
    if solution=="BB":
        disp_pattern=[0,0,0,0,0,0,0,0,0,volume*4,0,0]
    if solution=="DB":
        disp_pattern=[0,0,0,0,0,0,0,0,volume*4,0,0,0]
    if solution=="Buff1":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,volume*4,volume*4]
    if solution=="Buff2":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,0,volume*4]

    for col in range(0, 12, 1):
        #Let's find the smallest and largest well in the column
        smallest_well=96
        largest_well=0
        for washWell in washArray:
            if washWell>=col*8+1 and washWell<col*8+9:
                if washWell>largest_well:
                    largest_well=washWell
                if washWell<smallest_well:
                    smallest_well=washWell
        if smallest_well!=96 or largest_well!=0: #meaning if there is a non empty well in the column
            #Either we can dispense only once
            if largest_well-smallest_well<4:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, min(smallest_well, col * 8 + 5), i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    multiDispensePumps(hardware, disp_pattern)
            else:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseDoubleWashes_DB(hardware,volume,solution,array,is384):

    washArray=array.copy()
    if solution=="BB":
        disp_pattern=[0,0,0,0,0,0,0,0,0,volume*4,0,0]
    if solution=="DB":
        disp_pattern=[0,0,0,0,0,0,0,0,volume*4,volume*4,0,0]
    if solution=="Buff1":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,volume*4,0]
    if solution=="Buff2":
        disp_pattern=[0,0,0,0,0,0,0,0,0,0,0,volume*4]

    for col in range(0, 12, 1):
        #Let's find the smallest and largest well in the column
        smallest_well=96
        largest_well=0
        for washWell in washArray:
            if washWell>=col*8+1 and washWell<col*8+9:
                if washWell>largest_well:
                    largest_well=washWell
                if washWell<smallest_well:
                    smallest_well=washWell
        if smallest_well!=96 or largest_well!=0: #meaning if there is a non empty well in the column
            #Either we can dispense only once
            if largest_well-smallest_well<4:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, min(smallest_well, col * 8 + 5), i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    multiDispensePumps(hardware, disp_pattern)
            else:
                if is384:
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,quadrant_nb+1):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)



def removeSupernatant(hardware,vacuumTime):

    goToWell(hardware, 'thermalCamera', 1,0)

    hardware.vacValveOpen()

    wait(hardware, vacuumTime)
    hardware.vacValveClose()

    wait(hardware, 3)

def removeSupernatantPosPressure(hardware, wells, time, plate, vacuum):

    hardware.posPressure.goUp()
    if wells=="excel":
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, 1)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, 1)
        wells_array=activeWells
    else:
        wells_array=wells.copy()
    while wells_array!=[]:
        well_to_go=wells_array[0]
        while 12 - (well_to_go-1)//8 - 1 < hardware.posPressure.rows-1:
            well_to_go-=8
        while 8 - (well_to_go-1)%8 - 1 < hardware.posPressure.cols-1 :
            well_to_go-= 1
        goToWell(hardware,"PosPressure",well_to_go,0)
        hardware.posPressure.apply_pressure(time,plate)
        for rows in range(hardware.posPressure.rows):
            for cols in range(hardware.posPressure.cols):
                if well_to_go+cols+(8*rows) in wells_array:
                    wells_array.remove(well_to_go+cols+(8*rows))

    hardware.posPressure.goUp()

    if vacuum:
        hardware.vacValveOpen()
        wait(hardware,3)
        hardware.vacValveClose()

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

def DBRinseRoutine(hardware):

    return
    rinse_vol=10000 #uL

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, 0, "Rinsing DB line")
    hardware.DBSwitchOpen()
    multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,rinse_vol])
    hardware.DBSwitchClose()
    updateCycleLabel(hardware, 0, "Synthesis End")


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

def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())

