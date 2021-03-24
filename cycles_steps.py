from elementaryFunctions import *
from excelRead import *

def dispensePremixes(hardware,time,A_array,C_array,G_array,T_array,is384):

    nuclArrays=[A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy()]
    'we loop for every position possible'
    for col in range(0,12,1):
        for a_well in range(1+14*col,11+(14*col)+1,1):
            c_well=a_well+1
            g_well=a_well+2
            t_well=a_well+3
            wells=[a_well,c_well,g_well,t_well]
            disp=[0,0,0,0] #Flag to know if we should dispense
            for nucl in range(4):
                #print (plateWellToRealWell(wells[nucl]))
                if plateWellToRealWell(wells[nucl]) in nuclArrays[nucl]:
                    disp[nucl]=1
                    nuclArrays[nucl].remove(plateWellToRealWell(wells[nucl]))

            if 1 in disp:
                if is384:
                    for i in range(1,5):
                        goToRealWell(hardware,a_well,i)
                        multiDispense(hardware, disp, time)
                else:
                    goToRealWell(hardware, a_well, 0)
                    multiDispense(hardware, disp, time)
                    # 0.22 for 48uL
                    # 0.48 for 96uL
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispensePremixesAndEnzyme(hardware,time_nuc,time_enz,M_array,N_array,A_array,C_array,G_array,T_array,is384):

    nuclArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy()]
    'we loop for every position possible'
    for col in range(0,12,1):
        for m_well in range(1+18*col,13+(18*col)+1,1):
            n_well=m_well+1
            a_well=m_well+2
            c_well=m_well+3
            g_well=m_well+4
            t_well=m_well+5
            wells=[m_well,n_well,a_well,c_well,g_well,t_well]
            disp=[0,0,0,0,0,0] #Flag to know if we should dispense
            for nucl in range(6):
                #print (plateWellToRealWell(wells[nucl]))
                if plateWellToRealWell6Nozzles(wells[nucl]) in nuclArrays[nucl]:
                    disp[nucl]=1
                    nuclArrays[nucl].remove(plateWellToRealWell6Nozzles(wells[nucl]))
            if 1 in disp:
                if is384:
                    for i in range(1,5):
                        goToRealWell6Nozzles(hardware,m_well,i)
                        multiDispenseWithEnzyme(hardware, disp, time_nuc,time_enz)
                else:
                    goToRealWell6Nozzles(hardware, m_well, 0)
                    multiDispenseWithEnzyme(hardware, disp, time_nuc, time_enz)
                    #multiDispense(hardware, disp, time)
                    # 0.22 for 48uL
                    # 0.48 for 96uL
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispensePremixesAndEnzymeSep(hardware,time_nuc,time_enz_M,time_enz_N,M_array,N_array,A_array,C_array,G_array,T_array,is384):

    nuclArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy()]
    'we loop for every position possible'
    for col in range(0,12,1):
        for m_well in range(1+18*col,13+(18*col)+1,1):
            n_well=m_well+1
            a_well=m_well+2
            c_well=m_well+3
            g_well=m_well+4
            t_well=m_well+5
            wells=[m_well,n_well,a_well,c_well,g_well,t_well]
            disp=[0,0,0,0,0,0] #Flag to know if we should dispense
            for nucl in range(6):
                #print (plateWellToRealWell(wells[nucl]))
                if plateWellToRealWell6Nozzles(wells[nucl]) in nuclArrays[nucl]:
                    disp[nucl]=1
                    nuclArrays[nucl].remove(plateWellToRealWell6Nozzles(wells[nucl]))
            if 1 in disp:
                if is384:
                    for i in range(1,5):
                        goToRealWell6Nozzles(hardware,m_well,i)
                        multiDispenseWithEnzymeSep(hardware, disp, time_nuc,time_enz_M,time_enz_N)
                else:
                    goToRealWell6Nozzles(hardware, m_well, 0)
                    multiDispenseWithEnzymeSep(hardware, disp, time_nuc, time_enz_M,time_enz_N)
                    #multiDispense(hardware, disp, time)
                    # 0.22 for 48uL
                    # 0.48 for 96uL
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispensePumps(hardware,volumes,M_array,N_array,A_array,C_array,G_array,T_array,is384):

    nuclArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy()]
    'we loop for every position possible'
    for col in range(0,12,1):
        for m_well in range(1+18*col,13+(18*col)+1,1):
            n_well=m_well+1
            a_well=m_well+2
            c_well=m_well+3
            g_well=m_well+4
            t_well=m_well+5
            wells=[m_well,n_well,a_well,c_well,g_well,t_well]
            disp=[0,0,0,0,0,0,0,0] #Flag to know if we should dispense
            for nucl in range(6):
                #print (plateWellToRealWell(wells[nucl]))
                if plateWellToRealWell6Nozzles(wells[nucl]) in nuclArrays[nucl]:
                    disp[nucl]=volumes[nucl]
                    nuclArrays[nucl].remove(plateWellToRealWell6Nozzles(wells[nucl]))
            if any(vol!=0 for vol in disp ):
                if is384:
                    for i in range(1,5):
                        goToRealWell6Nozzles(hardware,m_well,i)
                        multiDispensePumps(hardware,disp)
                else:
                    goToRealWell6Nozzles(hardware, m_well, 0)
                    multiDispensePumps(hardware,disp)
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispensePumpsColDiffVols(hardware,volumesPerCol,M_array,N_array,A_array,C_array,G_array,T_array,is384):

    nuclArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy()]
    'we loop for every position possible'
    for col in range(0,12,1):
        for m_well in range(1+18*col,13+(18*col)+1,1):
            n_well=m_well+1
            a_well=m_well+2
            c_well=m_well+3
            g_well=m_well+4
            t_well=m_well+5
            wells=[m_well,n_well,a_well,c_well,g_well,t_well]
            disp=[0,0,0,0,0,0,0,0] #Flag to know if we should dispense
            for nucl in range(6):
                #print (plateWellToRealWell(wells[nucl]))
                if plateWellToRealWell6Nozzles(wells[nucl]) in nuclArrays[nucl]:
                    disp[nucl]=volumesPerCol[col]
                    nuclArrays[nucl].remove(plateWellToRealWell6Nozzles(wells[nucl]))
            if any(vol!=0 for vol in disp ):
                if is384:
                    for i in range(1,5):
                        goToRealWell6Nozzles(hardware,m_well,i)
                        multiDispensePumps(hardware,disp)
                else:
                    goToRealWell6Nozzles(hardware, m_well, 0)
                    multiDispensePumps(hardware,disp)
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)


def dispenseAllDegenerate(hardware,volumes,M_array,N_array,A_array,C_array,G_array,T_array,is384):


    nuclArrays=[M_array.copy(),N_array.copy(),A_array.copy(),C_array.copy(),G_array.copy(),T_array.copy()]
    'we loop for every position possible'
    for col in range(0,12,1):
        for m_well in range(1+18*col,13+(18*col)+1,1):
            n_well=m_well+1
            a_well=m_well+2
            c_well=m_well+3
            g_well=m_well+4
            t_well=m_well+5
            wells=[m_well,n_well,a_well,c_well,g_well,t_well]
            vols=[0,0,0,0,0,0] #Flag to know if we should dispense
            for nucl in range(6):
                #print (plateWellToRealWell(wells[nucl]))
                for wellVol in nuclArrays[nucl]:
                    if plateWellToRealWell6Nozzles(wells[nucl])==wellVol[0]:
                        vols[nucl]=volumes[nucl]/wellVol[1]
                        nuclArrays[nucl].remove(wellVol)
            if vols!=[0,0,0,0,0,0]:
                if is384:
                    for i in range(1,5):
                        goToRealWell6Nozzles(hardware,m_well,i)
                        multiDispensePumps(hardware,vols)
                else:
                    goToRealWell6Nozzles(hardware, m_well, 0)
                    multiDispensePumps(hardware,vols)
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseWashes(hardware,volume,solution,array,is384):

    washArray=array.copy()

    if solution=="BB":
        disp_pattern=[0,0,0,0,0,0,0,volume*4]
    if solution=="DB":
        disp_pattern=[0,0,0,0,0,0,volume*4,0]

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
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseWashesColDiffVols(hardware,volumesPerCol,solution,array,is384):

    washArray=array.copy()

    for col in range(0, 12, 1):
        #Let's find the smallest and largest well in the column
        if solution == "BB":
            disp_pattern = [0, 0, 0, 0, 0, 0, 0, volumesPerCol[col] * 4]
        if solution == "DB":
            disp_pattern = [0, 0, 0, 0, 0, 0, volumesPerCol[col] * 4, 0]
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
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, disp_pattern)
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, disp_pattern)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    multiDispensePumps(hardware, disp_pattern)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    multiDispensePumps(hardware, disp_pattern)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)


def dispenseWashesDBReduce(hardware,volume,solution,array,is384):

    washArray=array.copy()

    DBVols = [25, 17.5, 18.75, 20]

    if solution=="BB":
        disp_pattern=[0,0,0,0,0,0,0,volume*4]
    if solution=="DB":
        disp_pattern=[0,0,0,0,0,0,volume*4,0]

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

                        multiDispensePumps(hardware,[0,0,0,0,0,0,DBVols[i-1]*4,0])
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    multiDispensePumps(hardware, disp_pattern)
            else:
                if is384:
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        multiDispensePumps(hardware, [0,0,0,0,0,0,DBVols[i-1]*4,0])
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        multiDispensePumps(hardware, [0,0,0,0,0,0,DBVols[i-1]*4,0])
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

def fillPlate(hardware, buffer, vol, is384):

    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet(path)
    getParameters(synthesis_sheet)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    if buffer=="nucs":
        dispensePumps(hardware, [vol, vol, vol, vol, vol, vol],
                      nucleo_arrays[5], nucleo_arrays[6],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], is384)
    elif buffer=="DB":
        dispenseWashes(hardware,vol,"DB",activeWells,is384)
    elif buffer=="BB":
        dispenseWashes(hardware,vol,"BB",activeWells,is384)

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

def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())