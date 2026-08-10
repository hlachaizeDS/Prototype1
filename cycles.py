from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits
import inspect

proteinase=0
dispDBTime = 0.11
dispBBTime = 0.09
dispBuff1Time=0.155
dispBuff2Time=0.13
dispWater50=0.16

enz_vol=25 #utile ? QS
nuc_vol=25 #utile ? QS




def ElongationCycleSeparatedOneEnz(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def TwoDiffNucs(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Nucs")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        wells_MO=wellListFromColumns([1,3,5,7,9,11])
        wells_Fresh=wellListFromColumns([2,4,6,8,10,12])

        dispensePumps(hardware, [nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      inter([nucleo_arrays[1],wells_MO]),
                      inter([nucleo_arrays[2],wells_MO]),
                      inter([nucleo_arrays[1],wells_Fresh]),
                      inter([nucleo_arrays[2],wells_Fresh]),
                      inter([nucleo_arrays[3],wells_Fresh]),
                      inter([nucleo_arrays[4],wells_Fresh]),
                      inter([nucleo_arrays[3],wells_MO]),
                      inter([nucleo_arrays[4],wells_MO]),
                      is384)

        updateCycleLabel(hardware, cycle, "Enz")

        dispenseWashes(hardware, enz_vol, 'Buff2', usedWells, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_W1_10minSomeCycles(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    cycles_10min = [1]

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10min:
            waitAndStir(hardware, 10 * 60)
        else:
            waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_W1_10minSomeCycles_NoLastDB(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    cycles_10min = [81]
    cycles_NoDB = [81]

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10min:
            waitAndStir(hardware, 10 * 60)
        else:
            waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        if cycle not in cycles_NoDB:
            updateCycleLabel(hardware, cycle, "DB1")
            dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        if cycle not in cycles_NoDB:
            updateCycleLabel(hardware, cycle, "DB2")
            dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_EnzviaQ(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol], nucleo_arrays[5], nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],activeWells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedTwoEnz(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedTwoEnzDBactive(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedFourEnz(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedFourEnzQ(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 50],
                            [], [], [], [], [], [], [], [], usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps_Q(hardware, [0, 0, 0, 0,0, 0, 0, 0,50],
                    [],[],[],[],[],[],[],[],usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedFourEnz_B4(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # Extra Wash
        updateCycleLabel(hardware, cycle, "ExtraWash")
        dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraWashDisp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraWashInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraWashVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationTwoEnz_10minSomeCycles(hardware,is384):

    cycles_10min=[4,18,28]

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10min:
            waitAndStir(hardware, 10*60)
        else:
            waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationOneEnz_10minSomeCycles(hardware,is384):

    cycles_10min=[16,17]
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10min:
            waitAndStir(hardware, 10*60)
        else:
            waitAndStir(hardware, Elong_time)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_EDTAspike_FourIncW1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        dispenseWashes(hardware, 20, 'Buff2', usedWells, is384)
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftEDTAInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        well1=wellListFromColumns([1,5,9])
        well2=wellListFromColumns([2,6,10])
        well3=wellListFromColumns([3,7,11])
        well4=wellListFromColumns([4,8,12])
        updateCycleLabel(hardware, cycle, "W1.1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', well4, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp1')
        waitAndStir(hardware, 23)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc1')
        updateCycleLabel(hardware, cycle, "W1.2")
        dispenseWashes(hardware, BBVolume1, 'Buff1', well2, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp2')
        waitAndStir(hardware, 13)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc2')
        updateCycleLabel(hardware, cycle, "W1.3")
        dispenseWashes(hardware, BBVolume1, 'Buff1', well3, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp3')
        waitAndStir(hardware, 13)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc3')
        updateCycleLabel(hardware, cycle, "W1.4")
        dispenseWashes(hardware, BBVolume1, 'Buff1', well1, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp4')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc4')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoStepsWB2_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoWB2(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)
            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]),is384)
            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1


    dispensePumps(hardware, [0,0,0,0,0,0,50,0], [], [], [], [], [], [],usedWells,[],is384)
    waitAndStir(hardware, DB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0], [], [], [], [], [], [], usedWells, [], is384)
    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_FourDiffWB1_OneStepDB_TwoStepsWB2_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, 50, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps_Q(hardware,[0,BBVolume1,0,0,0,0,BBVolume1,BBVolume1,BBVolume1],[], [well for well in activeWells if well%4==1],[],[],[],[], [well for well in activeWells if well%4==2], [well for well in activeWells if well%4==3], [well for well in activeWells if well%4==0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        dispenseWashes(hardware, 80, 'DB', wellListFromColumns([2,4,6,8,10,12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

               #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc2')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, 50, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_Xn_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePumps(hardware, [enz_vol,50,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], activeWells, endedWells, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,50,0,0,0,0,0,0], [],usedWells, [],[],[],[], [],[], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0,50,0,0,0,0,0,0], [],usedWells, [],[],[],[], [],[], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_DiffVolCol_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)
            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
            #dispenseWashesColDiffVols(hardware,[BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2],'BB',usedWells,is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispenseWashes(hardware, BBVolume2,'Buff2', endedWells, is384)
        dispensePumpsDiffCols(hardware,[enz_vol,enz_vol*0.6,enz_vol,enz_vol,enz_vol*0.6,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol*0.6],[well for well in activeWells if well%2==1],[well for well in activeWells if well%2==0],nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware,[BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1*0.6],'Buff1', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware,[DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1*0.6],'DB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware,[DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2*0.6],'DB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware,[BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1*0.6],'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def TwoEnz_DiffVolCol_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)
            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)
            #dispenseWashesColDiffVols(hardware,[BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2],'BB',usedWells,is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePumpsDiffCols(hardware,[enz_vol,enz_vol*0.5,enz_vol*0.5,enz_vol,enz_vol*0.5,enz_vol*0.5,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol],[well for well in activeWells if well%2==1],[well for well in activeWells if well%2==0],nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in endedWells if well%2==1],[well for well in endedWells if well%2==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware,[DBVolume1,DBVolume1,DBVolume1*0.5,DBVolume1,DBVolume1,DBVolume1*0.5,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1],'DB', inter([activeWells, wellListFromColumns([1,2,3,4,5,6,7,8])]), is384)
        dispenseDoubleWashes_DB(hardware,DBVolume1,'DB',inter([activeWells, wellListFromColumns([9,11])]),is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware,[DBVolume2,DBVolume2,DBVolume1*0.5,DBVolume2,DBVolume2,DBVolume1*0.5,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2],'DB', inter([activeWells, wellListFromColumns([1,2,3,4,5,6,7,8])]),is384)
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', inter([activeWells, wellListFromColumns([9,11])]),
                                is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume1, 'Buff2', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, BBVolume2], [], [], [], [], [], [],
                  [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, BBVolume2], [], [], [], [], [], [],
                  [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_Xbuff2_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispenseWashes(hardware, BBVolume2, 'Buff2', endedWells, is384)
        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], nucleo_arrays[5], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware,BBVolume2,'Buff2',usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware,BBVolume2,'Buff2',usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_EndedWellsCR0_hardocded_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        if cycle==53:
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
        if cycle==101:
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 1000, 0, 0, 0, 0, 0, 0])
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)
        if cycle in list(range(101,200+1)):
            dispensePumps(hardware,[0,0,0,0,0,0,50,0], [],[],[],[],[],[],[well for well in endedWells if well in wellListFromColumns([7,8])],[], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixEnded')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Ended')
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1EndedWells')
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2EndedWells')
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBEnded')
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_EndedWellsWash_Long (hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        ended_wells=getEndedWellsPlusX(sequences, cycle)
        pH65=inter([activeWells,wellListFromHalfColumns([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])])
        pH74=inter([activeWells,wellListFromHalfColumns([22,23,24])])


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume
        #'Buff2' = CR50 pH 7.4
        #'Buff1' = CR50 pH 6.5
        #'BB" = wash1
        #'N' = CR0
        #'O' = H20

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],[], [well for well in usedWells], [],[], [], [], [], [], is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)




        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        #dispenseWashes(hardware, BBVolume1, 'Buff2', endedWells, is384)
        #TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixEnded')
        dispensePumps(hardware, [enz_vol,50,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells], [well for well in ended_wells], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], [],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        if cycle > 52:
            dispenseWashes(hardware, DBVolume1, 'DB', wellListFromHalfColumns([10,11,12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1EndedWells')
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        if cycle > 52:
            dispenseWashes(hardware, DBVolume1, 'DB', wellListFromHalfColumns([10,11,12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2EndedWells')
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        if cycle > 52:
            dispenseWashes(hardware, DBVolume1, 'Buff1', wellListFromHalfColumns([13, 14, 15]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBEndedWells')
        dispenseWashes(hardware, BBVolume2, 'Buff1', pH65, is384)
        dispenseWashes(hardware, BBVolume2, 'Buff2', pH74, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        if (cycle == 52):
            input('Merci Henri de prélever la résine + ADN des 3 premières demi colonnes :-) ')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol], [],
                  [well for well in usedWells], [], [], [], [], [], [], is384)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftCR0Disp')
    waitAndStir(hardware, DB2Time)
    removeSupernatant(hardware, VacuumTime)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftCR0Vac')
    dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol], [],
                  [well for well in usedWells], [], [], [], [], [], [], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_EndedWellsCR0_hardocded_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        if cycle==53:
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
        if cycle==101:
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 1000, 0, 0, 0, 0, 0, 0])
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)
        if cycle in list(range(101,200+1)):
            dispensePumps(hardware,[0,0,0,0,0,0,50,0], [],[],[],[],[],[],[well for well in endedWells if well in wellListFromColumns([7,8])],[], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixEnded')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Ended')
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1EndedWells')
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2EndedWells')
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        if cycle > 200:
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6, 7, 8, 9, 10]), is384)
        if cycle in list(range(53,200+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5, 6]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBEnded')
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_plus48cyWB2_W1(hardware, is384):

        title = easygui.enterbox("Name of the run ?")

        # Save Quartet Control File
        saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
        if saveQuartet:
            saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

        thermalImages = 1
        if thermalImages:
            TT = hardware.parent.rightFrame.thermalThread
        else:
            TT = FakeThermalImageThread()

        # Set up recording file for thermal snapshots
        now = datetime.datetime.now()
        folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
            now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
            now.second) + "_" + title

        TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

        cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

        while cycle != 0:

            updateCycleLabel(hardware, cycle, "")

            # We read the excel and get the parameters back
            synthesis_sheet = getExcelSheet(path)
            getParameters(synthesis_sheet)
            sequences = getSequences(synthesis_sheet)
            nucleo_arrays = splitSequences(sequences, cycle)
            usedWells = getUsedWells(sequences)
            activeWells = getActiveWells(sequences, cycle)

            # print(nucleo_arrays)
            enz_vol = EBVolume
            nuc_vol = NucsVolume

            if (cycle == 1):
                removeSupernatant(hardware, VacuumTime)

                dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells, is384)

                waitAndStir(hardware, WB2Time)
                removeSupernatant(hardware, VacuumTime)

            # Premix
            updateCycleLabel(hardware, cycle, "Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

            dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                          [well for well in activeWells if well % 2 == 1],
                          [well for well in activeWells if well % 2 == 0], nucleo_arrays[1], nucleo_arrays[2],
                          nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, Elong_time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

            # W1
            updateCycleLabel(hardware, cycle, "W1")
            dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
            waitAndStir(hardware, WB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

            # DB1
            updateCycleLabel(hardware, cycle, "DB1")
            dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            # DB2
            updateCycleLabel(hardware, cycle, "DB2")
            dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

            # Wash
            updateCycleLabel(hardware, cycle, "Wash")
            dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

            # We carry on with next cycle or we end the loop
            nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
            if len(nucleo_arrays_nextcycle[0]) == len(sequences):
                cycle = 0
            else:
                cycle += 1

        for cycle in range(47):
            cycle=cycle+53
            updateCycleLabel(hardware, cycle, "Wash")
            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, Elong_time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

            dispenseDoubleWashes_Buff1(hardware,BBVolume2,'Buff1',wellListFromColumns([1,3,5,7,9,11]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
            waitAndStir(hardware, WB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

            dispenseDoubleWashes_Buff1(hardware,BBVolume2,'Buff1',wellListFromColumns([1,3,5,7,9,11]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            dispenseDoubleWashes_Buff1(hardware,BBVolume2,'Buff1',wellListFromColumns([1,3,5,7,9,11]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        for i in range(3):
            updateCycleLabel(hardware, cycle, "Wash")
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([1, 2, 5, 6, 9, 10]), is384)
            dispenseWashes(hardware, BBVolume2, 'Buff1', wellListFromColumns([3, 4, 7, 8, 11, 12]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([1, 2, 5, 6, 9, 10]), is384)
        dispenseWashes(hardware, BBVolume2, 'Buff1', wellListFromColumns([3, 4, 7, 8, 11, 12]), is384)

        goToWell(hardware, 'thermalCamera', 1, 0)
        updateCycleLabel(hardware, cycle, "Synthesis End")
        hardware.arduinoControl.stopHeating()
        DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_FourDB_W1(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, 0, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      activeWells,
                      [], nucleo_arrays[1], nucleo_arrays[2],
                      nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispensePumps_Q(hardware, [0, DBVolume1, 0, 0, 0, 0, DBVolume1, DBVolume1, DBVolume1],
                        [],
                        [well for well in activeWells if well % 4 == 1], [], [], [], [],
                        [well for well in activeWells if well % 4 == 2],
                        [well for well in activeWells if well % 4 == 3],
                        [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispensePumps_Q(hardware, [0, DBVolume2, 0, 0, 0, 0, DBVolume2, DBVolume2, DBVolume2],
                        [],
                        [well for well in activeWells if well % 4 == 1], [], [], [], [],
                        [well for well in activeWells if well % 4 == 2],
                        [well for well in activeWells if well % 4 == 3],
                        [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1


    dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_DiffFourW1_XtraWash(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)
        CR50 = inter([activeWells, wellListFromColumns([4,5,6,7])])
        TH30 = inter([activeWells, wellListFromColumns([8,9])])


        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol, 0,nuc_vol, nuc_vol, nuc_vol, nuc_vol, 0, 0, 0],
                      activeWells,
                      [], nucleo_arrays[1], nucleo_arrays[2],
                      nucleo_arrays[3], nucleo_arrays[4], [], [], [], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps_Q(hardware, [0, BBVolume1,0, 0, 0, 0, BBVolume1, BBVolume1, BBVolume1],[],
                        [well for well in CR50 if well%4==1],[],[],[],[],
                        [well for well in CR50 if well%4==2],
                        [well for well in CR50 if well%4==3],
                        [well for well in CR50 if well%4==0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp1')
        dispenseWashes(hardware, BBVolume1, 'BB', TH30 , is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp2')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff1', CR50, is384)
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([8]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, BBVolume1], [],
                     [], [], [], [],[],[],[],usedWells, is384)


    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_DiffFourW1(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)
        CR50 = inter([activeWells, wellListFromColumns([4,5,6,7])])
        TH30 = inter([activeWells, wellListFromColumns([8,9])])


        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol, 0,nuc_vol, nuc_vol, nuc_vol, nuc_vol, 0, 0, 0],
                      activeWells,
                      [], nucleo_arrays[1], nucleo_arrays[2],
                      nucleo_arrays[3], nucleo_arrays[4], [], [], [], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps_Q(hardware, [0, BBVolume1,0, 0, 0, 0, BBVolume1, BBVolume1, BBVolume1],[],
                        [well for well in CR50 if well%4==1],[],[],[],[],
                        [well for well in CR50 if well%4==2],
                        [well for well in CR50 if well%4==3],
                        [well for well in CR50 if well%4==0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp1')
        dispenseWashes(hardware, BBVolume1, 'BB', TH30 , is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp2')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff1', CR50, is384)
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([8]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, BBVolume1], [],
                     [], [], [], [],[],[],[],usedWells, is384)


    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_DiffFourW1_3IncW1(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)


        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol, 0,nuc_vol, nuc_vol, nuc_vol, nuc_vol, 0, 0, 0],
                      activeWells,
                      [], nucleo_arrays[1], nucleo_arrays[2],
                      nucleo_arrays[3], nucleo_arrays[4], [], [], [], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells , is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp1')
        dispensePumps_Q(hardware, [0, BBVolume1,0, 0, 0, 0, BBVolume1, BBVolume1, BBVolume1],[],
                        [well for well in wellListFromColumns([2, 5, 8, 11]) if well%4==1],[],[],[],[],
                        [well for well in wellListFromColumns([2, 5, 8, 11]) if well%4==2],
                        [well for well in wellListFromColumns([2, 5, 8, 11]) if well%4==3],
                        [well for well in wellListFromColumns([2, 5, 8, 11]) if well%4==0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp2')
        waitAndStir(hardware, 48)
        dispensePumps_Q(hardware, [0, BBVolume1,0, 0, 0, 0, BBVolume1, BBVolume1, BBVolume1],[],
                        [well for well in wellListFromColumns([3, 6, 9, 12]) if well%4==1],[],[],[],[],
                        [well for well in wellListFromColumns([3, 6, 9, 12]) if well%4==2],
                        [well for well in wellListFromColumns([3, 6, 9, 12]) if well%4==3],
                        [well for well in wellListFromColumns([3, 6, 9, 12]) if well%4==0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp3')
        waitAndStir(hardware, 28)
        dispensePumps_Q(hardware, [0, BBVolume1, 0, 0, 0, 0, BBVolume1, BBVolume1, BBVolume1], [],
                        [well for well in wellListFromColumns([1, 4, 7, 10]) if well % 4 == 1], [], [], [], [],
                        [well for well in wellListFromColumns([1, 4, 7, 10]) if well % 4 == 2],
                        [well for well in wellListFromColumns([1, 4, 7, 10]) if well % 4 == 3],
                        [well for well in wellListFromColumns([1, 4, 7, 10]) if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp4')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    dispenseWashes(hardware,BBVolume2, 'Buff2', usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware,BBVolume2, 'Buff2', usedWells, is384)


    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_2DiffWB2_2WB2Steps_W1(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)
            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 5, 9]), is384)
            dispenseDoubleWashes_Buff1(hardware, 30, 'Buff1', wellListFromColumns([3, 7, 11]), is384)
            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in activeWells if well % 2 == 1],
                      [well for well in activeWells if well % 2 == 0], nucleo_arrays[1], nucleo_arrays[2],
                      nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')
        removeSupernatant(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        updateCycleLabel(hardware, cycle, "Wash2")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 5, 9]), is384)
        dispenseDoubleWashes_Buff1(hardware, 30, 'Buff1', wellListFromColumns([3, 7, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc2')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 5, 9]), is384)
    dispenseDoubleWashes_Buff1(hardware, 30, 'Buff1', wellListFromColumns([3, 7, 11]), is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_FourdiffWB2_W1_X(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWellsButX(sequences, cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
                      [],
                      [well for well in activeWells if well % 4 == 1], [], [], [], [],
                      [well for well in activeWells if well % 4 == 2],
                      [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware, BBVolume1, 'Buff2', endedWells, is384)
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
        activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)


        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
            [],
            [well for well in activeWells if well % 4 == 1], [], [], [], [],
            [well for well in activeWells if well % 4 == 2],
            [well for well in activeWells if well % 4 == 3],
            [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1


    dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
        [],
        [well for well in activeWells if well % 4 == 1], [], [], [], [],
        [well for well in activeWells if well % 4 == 2],
        [well for well in activeWells if well % 4 == 3],
        [well for well in activeWells if well % 4 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_noMN_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells = getActiveWellsButX(sequences, cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, BBVolume2, 0], [], [], [], [], [], [], [well for well in endedWells if well%2==1], [well for well in endedWells if well%2==0],  [], is384 )
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware,[0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[],[well for well in usedWells if well%2==1], [well for well in usedWells if well%2==0], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware,[0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[],[well for well in usedWells if well%2==1], [well for well in usedWells if well%2==0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_ExtraWash30cycles_W1X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        if (cycle%30==0):
            updateCycleLabel(hardware, cycle, "ExtraW")
            multiDispensePumpsQ(hardware,[0,400,0,0,0,0,400,400,0,0,0,0,400])
            dispensePumps_Q(hardware,[0,BBVolume2,0,0,0,0,BBVolume2,BBVolume2,BBVolume2],[],[well for well in inter([[well for well in activeWells if well%4==1],wellListFromColumns([1,2,3,4,7,8,9,10])])],[],[],[],[],[well for well in inter([[well for well in activeWells if well%4==2],wellListFromColumns([1,2,3,4,7,8,9,10])])],[well for well in inter([[well for well in activeWells if well%4==3],wellListFromColumns([1,2,3,4,7,8,9,10])])],[well for well in inter([[well for well in activeWells if well%4==0],wellListFromColumns([1,2,3,4,7,8,9,10])])],is384)
            dispenseWashes(hardware, BBVolume1, 'Buff1', [well for well in wellListFromColumns([5,11])], is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraWDisp')
            waitAndStir(hardware, 60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraWInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraWVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,0,0,0,1000,0])
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoWB2_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,50,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],endedWells, nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', inter(wellListFromColumns([1,3,7,9]),activeWells), is384)
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', inter(wellListFromColumns([3,9]),activeWells), is384)
        dispensePumps_Q(hardware,[0,0,0,0,0,0,0,50,50],[],[],[],[],[],[],[],inter(wellListFromColumns([5,11]),activeWells),inter(wellListFromColumns([6,12]),activeWells), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time),
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0],
                  [], [],[], [], [], [], usedWells, [],
                  is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoVolFourDiffWB1_W1X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,50,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],endedWells, nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', inter(wellListFromColumns([1,3,7,9]),activeWells), is384)
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', inter(wellListFromColumns([3,9]),activeWells), is384)
        dispensePumps_Q(hardware,[0,0,0,0,0,0,0,50,50],[],[],[],[],[],[],[],inter(wellListFromColumns([5,11]),activeWells),inter(wellListFromColumns([6,12]),activeWells), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time),
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0],
                  [], [],[], [], [], [], usedWells, [],
                  is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, 50, 'BB', usedWells, is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware,BBVolume2,'Buff2',endedWells,is384)
        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3],
                        nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], nucleo_arrays[10], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_TwoDB_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3],
                        nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], nucleo_arrays[10], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_ElongTime_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume
        unevenCol = wellListFromColumns([1, 3, 5, 7, 9, 11])
        evenCol = wellListFromColumns([2, 4, 6, 8, 10, 12])

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix

        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware,BBVolume2,'Buff2',endedWells,is384)

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        inter([evenCol,activeWells]),
                        inter([evenCol,nucleo_arrays[6]]),
                        inter([evenCol,nucleo_arrays[1]]),
                        inter([evenCol,nucleo_arrays[2]]),
                        inter([evenCol,nucleo_arrays[3]]),
                        inter([evenCol,nucleo_arrays[4]]),
                        inter([evenCol,nucleo_arrays[7]]),
                        inter([evenCol,nucleo_arrays[8]]),
                        inter([evenCol,nucleo_arrays[10]]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        inter([unevenCol,activeWells]),
                        inter([unevenCol,nucleo_arrays[6]]),
                        inter([unevenCol,nucleo_arrays[1]]),
                        inter([unevenCol,nucleo_arrays[2]]),
                        inter([unevenCol,nucleo_arrays[3]]),
                        inter([unevenCol,nucleo_arrays[4]]),
                        inter([unevenCol,nucleo_arrays[7]]),
                        inter([unevenCol,nucleo_arrays[8]]),
                        inter([unevenCol,nucleo_arrays[10]]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 170)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_TwelveNucs_TwoDiffWB2_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)
        wellsHalf=wellListFromColumns([1,2,7,8])
        wellsFull=wellListFromColumns([3,4,5,6,9,10,11,12])


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware,BBVolume2, 'Buff1',wellListFromColumns([1,3,5,7,9,11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                        [well for well in wellsFull],
                        inter([wellsFull,nucleo_arrays[6]]),
                        inter([wellsFull,nucleo_arrays[1]]),
                        inter([wellsFull,nucleo_arrays[2]]),
                        inter([wellsFull,nucleo_arrays[3]]),
                        inter([wellsFull,nucleo_arrays[4]]),
                        inter([wellsFull,nucleo_arrays[7]]),
                        inter([wellsFull,nucleo_arrays[8]]),
                        inter([wellsFull,nucleo_arrays[10]]),
                        is384)
        dispensePumps_Q(hardware, [enz_vol,nuc_vol/2,nuc_vol/2,nuc_vol/2,nuc_vol/2,nuc_vol/2,nuc_vol/2,nuc_vol/2,nuc_vol/2],
                        [well for well in wellsHalf],
                        inter([wellsHalf,nucleo_arrays[1]]),
                        inter([wellsHalf,nucleo_arrays[1]]),
                        inter([wellsHalf,nucleo_arrays[2]]),
                        inter([wellsHalf,nucleo_arrays[3]]),
                        inter([wellsHalf,nucleo_arrays[4]]),
                        inter([wellsHalf,nucleo_arrays[2]]),
                        inter([wellsHalf,nucleo_arrays[3]]),
                        inter([wellsHalf,nucleo_arrays[4]]),is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1,3,5,7,9,11]),is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnzCrossed_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')


    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]


        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, union([inter([ColToWell([1,2,3,4,5,6]), [well for well in activeWellsButX if well % 2 == 1]]), inter([ColToWell([7,8,9,10,11,12]), [well for well in activeWellsButX if well % 2 == 0]])])],
            "N": [EBVolume, union([inter([ColToWell([1,2,3,4,5,6]), [well for well in activeWellsButX if well % 2 == 0]]), inter([ColToWell([7,8,9,10,11,12]), [well for well in activeWellsButX if well % 2 == 1]])])],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [50, [well for well in X_wells if well % 2 == 1]],
            "P": [50, [well for well in X_wells if well % 2 == 0]],
            "Q": [NucsVolume, Q_wells]
            }, is384, max_vol=25)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FiveWB2_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')


    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]


        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,wellListFromColumns([1, 6, 7, 8, 9, 10])],
                                              "N": [50, wellListFromColumns([2, 11])],
                                              "O": [50, wellListFromColumns([3, 12])],
                                              "P": [50, wellListFromColumns([4])],
                                              "Q": [50, wellListFromColumns([5])],
                                              },is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, activeWellsButX],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, inter([activeWellsButX, wellListFromColumns([1, 6, 7, 8, 9, 10])])],
                                           "N": [BBVolume2, inter([activeWellsButX, wellListFromColumns([2, 11])])],
                                           "O": [BBVolume2, inter([activeWellsButX, wellListFromColumns([3, 12])])],
                                           "P": [BBVolume2, inter([activeWellsButX, wellListFromColumns([4])])],
                                           "Q": [BBVolume2, inter([activeWellsButX, wellListFromColumns([5])])],
                                           }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_InkjetB5_TwoG_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        start=time.time()
        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [50, A_wells],
            "N": [50, C_wells],
            "O": [50, G_wells],
            "P": [50, P_wells],
            "Q": [50, T_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoG_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        start=time.time()
        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [NucsVolume, [well for well in O_wells if well % 2 == 1]],
            "P": [NucsVolume, [well for well in O_wells if well % 2 == 0]],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2":100})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)



def Synthesis_TwoDiffEnz_LongWB1_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        start=time.time()
        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([1,2,3,4,6,8,10,12]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([1,2,3,4,6,8,10,12]) if well % 2 == 0]])],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([5,7,9,11]) if well % 2 == 1]])],
            "P": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([5,7,9,11]) if well % 2 == 0]])],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        if cycle<53 or cycle in [100,150,200,250,300,350,400,447]:
            waitAndStir(hardware, 300)
        else:
            waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_IncVol_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        start=time.time()
        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [[EBVolume,EBVolume*1.4,EBVolume,EBVolume,EBVolume,EBVolume*1.4,EBVolume*1.4,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume], [well for well in activeWellsButX if well % 2 == 1]],
            "N": [[EBVolume,EBVolume*1.4,EBVolume,EBVolume,EBVolume,EBVolume*1.4,EBVolume*1.4,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume], [well for well in activeWellsButX if well % 2 == 0]],
            "A": [[NucsVolume,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume*1.4,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume], A_wells],
            "C": [[NucsVolume,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume*1.4,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume], C_wells],
            "G": [[NucsVolume,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume*1.4,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume], G_wells],
            "T": [[NucsVolume,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume*1.4,NucsVolume*1.4,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume], T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1*1.4,BBVolume1*1.4,BBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1*1.4,DBVolume1*1.4,DBVolume1,DBVolume1,DBVolume1,DBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume2,DBVolume2,DBVolume1,DBVolume2,DBVolume2,DBVolume2,DBVolume2*1.4,DBVolume2*1.4,DBVolume1,DBVolume2,DBVolume2,DBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [[BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2*1.4,BBVolume2,BBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_RedVol_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        start=time.time()
        full=time.time()
        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [[EBVolume*0.5,EBVolume*0.5,EBVolume,EBVolume,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5], [well for well in activeWellsButX if well % 2 == 1]],
            "N": [[EBVolume*0.5,EBVolume*0.5,EBVolume,EBVolume,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5], [well for well in activeWellsButX if well % 2 == 0]],
            "A": [[EBVolume*0.5,EBVolume*0.5,EBVolume,EBVolume,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5], A_wells],
            "C": [[EBVolume*0.5,EBVolume*0.5,EBVolume,EBVolume,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5], C_wells],
            "G": [[EBVolume*0.5,EBVolume*0.5,EBVolume,EBVolume,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5], G_wells],
            "T": [[EBVolume*0.5,EBVolume*0.5,EBVolume,EBVolume,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5,EBVolume*0.5], T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume1*0.5,BBVolume1*0.5,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1*0.5,BBVolume1*0.5,BBVolume1,BBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume1*0.5,DBVolume1*0.5,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1*0.5,DBVolume1*0.5,DBVolume1*0.5,DBVolume1*0.5,DBVolume1,DBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume2*0.5,DBVolume2*0.5,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2*0.5,DBVolume2*0.5,DBVolume2*0.5,DBVolume2*0.5,DBVolume2,DBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [[BBVolume2*0.5,BBVolume2*0.5,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    #print('End ',full)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FiveDB_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, activeWellsButX],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        if (cycle==26):
            for i in range(20):
                multi_dispense_in_wells(hardware, {"N": [DBVolume1, [well for well in activeWellsButX if well % 4 == 1]],
                                                   "O": [DBVolume1, [well for well in activeWellsButX if well % 4 == 2]],
                                                   "P": [DBVolume1, [well for well in activeWellsButX if well % 4 == 3]],
                                                   "Q": [DBVolume1, [well for well in activeWellsButX if well % 4 == 0]]}, is384)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBFloodDisp')
                waitAndStir(hardware, 120)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBFloodInc')
                removeSupernatant(hardware, VacuumTime)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBFloodVac')

        else:
            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PDR_Synthesis_TwoDiffEnzMN_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PDR_Synthesis_OneEnz_TwoWB2_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")
    easygui.msgbox(msg="Do you test two WB2 ?", title="WB2 comparison",ok_button="Yes", image=None, root=None)

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff1": [50, wellListFromHalfColumns([1,4,5,8,9,12,14,15,18,19,22,23])],
                                              "Buff2":[50, wellListFromHalfColumns([2,3,6,7,10,11,13,16,17,20,21,24])]}, is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [50, [well for well in X_wells if well % 2 == 1]],
                                           "P": [50, [well for well in X_wells if well % 2 == 0]],
                                           "Q": [NucsVolume, Q_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, inter([activeWellsButX,wellListFromHalfColumns([1,4,5,8,9,12,14,15,18,19,22,23])])],
                                           "Buff2": [BBVolume2, inter([activeWellsButX,wellListFromHalfColumns([2,3,6,7,10,11,13,16,17,20,21,24])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"O": 100, "P": 100})
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                       "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftLastBBDisp')
    waitAndStir(hardware, 20)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftLastBBInc')
    removeSupernatant(hardware, 20)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftLastBBVac')
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                       "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def PDR_Synthesis_OneEnz_TwoWB1_Xop(hardware, is384):

    title = easygui.enterbox("Name of the run ?")
    easygui.msgbox(msg="Do you test two WB1 ?", title="WB1 comparison", ok_button="Yes", image=None, root=None)

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title, inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells, A_wells, C_wells, G_wells, T_wells, M_wells, N_wells, O_wells, P_wells, X_wells, Q_wells] \
            = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                            "A": [NucsVolume, A_wells],
                                            "C": [NucsVolume, C_wells],
                                            "G": [NucsVolume, G_wells],
                                            "T": [NucsVolume, T_wells],
                                            "O": [50, [well for well in X_wells if well % 2 == 1]],
                                            "P": [50, [well for well in X_wells if well % 2 == 0]],
                                            "Q": [NucsVolume, Q_wells]
                                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX, wellListFromHalfColumns([1, 4, 5, 8, 9, 12, 14, 15, 18, 19, 22, 23])])],
                                            "Buff2": [BBVolume1, inter([activeWellsButX, wellListFromHalfColumns([2, 3, 6, 7, 10, 11, 13, 16, 17, 20, 21, 24])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    multi_dispense(hardware, {"O": 100, "P": 100})
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                       "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftLastBBDisp')
    waitAndStir(hardware, 20)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftLastBBInc')
    removeSupernatant(hardware, 20)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftLastBBVac')
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                       "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def Synthesis_TwoEnz_ThreeWB2_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"O": [50,[well for well in wellListFromColumns([4,8,12]) if well % 2 == 1]],
                                              "P": [50, [well for well in wellListFromColumns([4,8,12]) if well % 2 == 0]]},is384)
            multi_dispense_in_wells(hardware, {"Buff1": [50,wellListFromColumns([1,2,5,6,9,10])],
                                               "Buff2": [50,wellListFromColumns([3,7,11])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
            "M": [EBVolume,wellListFromColumns([6,7,8])],
            "N": [EBVolume,wellListFromColumns([5])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([5,6,7,8])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([5,6,7,8])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([5,6,7,8])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([5,6,7,8])])],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 27)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume,wellListFromColumns([10,11,12])],
            "N": [EBVolume,wellListFromColumns([9])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([9,10,11,12])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([9,10,11,12])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([9,10,11,12])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([9,10,11,12])])],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 27)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume,wellListFromColumns([2,3,4])],
            "N": [EBVolume,wellListFromColumns([1])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([1,2,3,4])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([1,2,3,4])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([1,2,3,4])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([1,2,3,4])])],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 87)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware,
                                {"O": [BBVolume2, [well for well in wellListFromColumns([4, 8, 12]) if well % 2 == 1]],
                                 "P": [BBVolume2, [well for well in wellListFromColumns([4, 8, 12]) if well % 2 == 0]]}, is384)
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, wellListFromColumns([1, 2, 5, 6, 9, 10])],
                                           "Buff2": [BBVolume2, wellListFromColumns([3, 7, 11])]}, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Inkjetbaseperbase(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"BB":[50,ended_wells],
            "N": [NucsVolume, N_wells],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_TwoDB_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
            "M": [EBVolume, union([[well for well in wellListFromColumns([1,2,3,4]) if well % 4 == 1], wellListFromColumns([5,6])])],
            "N": [EBVolume, union([[well for well in wellListFromColumns([1,2,3,4]) if well % 4 == 2], wellListFromColumns([7,8])])],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [EBVolume, union([[well for well in wellListFromColumns([1,2,3,4]) if well % 4 == 3],wellListFromColumns([9,10])])],
            "P": [EBVolume, union([[well for well in wellListFromColumns([1,2,3,4]) if well % 4 == 0],wellListFromColumns([11,12])])],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, wellListFromColumns([5,7,9,11])],
                                           "BB": [DBVolume1, wellListFromColumns([1,2,3,4,6,8,10,12])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, wellListFromColumns([5,7,9,11])],
                                           "BB": [DBVolume2, wellListFromColumns([1,2,3,4,6,8,10,12])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_4ElongTime_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 1],wellListFromColumns([2,3,7])])],
            "N": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 0],wellListFromColumns([2,3,7])])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([2,3,7])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([2,3,7])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([2,3,7])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([2,3,7])])],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 19)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 1],
                                                                  wellListFromColumns([6])])],
                                           "N": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 0],
                                                                  wellListFromColumns([6])])],
                                           "A": [NucsVolume, inter([A_wells, wellListFromColumns([6])])],
                                           "C": [NucsVolume, inter([C_wells, wellListFromColumns([6])])],
                                           "G": [NucsVolume, inter([G_wells, wellListFromColumns([6])])],
                                           "T": [NucsVolume, inter([T_wells, wellListFromColumns([6])])],
                                           "O": [NucsVolume, O_wells],
                                           "P": [NucsVolume, P_wells],
                                           "Q": [NucsVolume, Q_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 19)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 1],
                                                                  wellListFromColumns([4])])],
                                           "N": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 0],
                                                                  wellListFromColumns([4])])],
                                           "A": [NucsVolume, inter([A_wells, wellListFromColumns([4])])],
                                           "C": [NucsVolume, inter([C_wells, wellListFromColumns([4])])],
                                           "G": [NucsVolume, inter([G_wells, wellListFromColumns([4])])],
                                           "T": [NucsVolume, inter([T_wells, wellListFromColumns([4])])],
                                           "O": [NucsVolume, O_wells],
                                           "P": [NucsVolume, P_wells],
                                           "Q": [NucsVolume, Q_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 19)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 1],
                                                                  wellListFromColumns([5])])],
                                           "N": [EBVolume, inter([[well for well in activeWellsButX if well % 2 == 0],
                                                                  wellListFromColumns([5])])],
                                           "A": [NucsVolume, inter([A_wells, wellListFromColumns([5])])],
                                           "C": [NucsVolume, inter([C_wells, wellListFromColumns([5])])],
                                           "G": [NucsVolume, inter([G_wells, wellListFromColumns([5])])],
                                           "T": [NucsVolume, inter([T_wells, wellListFromColumns([5])])],
                                           "O": [NucsVolume, O_wells],
                                           "P": [NucsVolume, P_wells],
                                           "Q": [NucsVolume, Q_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp4')
        waitAndStir(hardware, 90)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc4')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        if (cycle % 50 == 0):
            waitAndStir(hardware, 300)
        else:
            waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_TwoWB1_TwoWB2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FourWB2_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"N":[50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 1],wellListFromColumns([5])])],
                                              "O": [50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 2],wellListFromColumns([6])])],
                                              "P": [50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 3],wellListFromColumns([7])])],
                                              "Q": [50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 0],wellListFromColumns([8])])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, activeWellsButX],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"N":[50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 1],wellListFromColumns([5])])],
                                              "O": [50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 2],wellListFromColumns([6])])],
                                              "P": [50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 3],wellListFromColumns([7])])],
                                              "Q": [50, union([[well for well in wellListFromColumns([1,2,3,4,9,10,11,12]) if well % 4 == 0],wellListFromColumns([8])])]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    hardware.arduinoControl.stopHeating()
    removeSupernatant(hardware, 60)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 60)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    #hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_TwoWB1_FourWB2_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"N":[50,[well for well in usedWells if well % 4 == 1]],
                                              "O": [50, [well for well in usedWells if well % 4 == 2]],
                                              "P": [50, [well for well in usedWells if well % 4 == 3]],
                                              "Q": [50, [well for well in usedWells if well % 4 == 0]]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, activeWellsButX],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff1": [BBVolume1, inter([activeWellsButX, wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"N":[BBVolume2,[well for well in activeWellsButX if well % 4 == 1]],
                                              "O": [BBVolume2, [well for well in activeWellsButX if well % 4 == 2]],
                                              "P": [BBVolume2, [well for well in activeWellsButX if well % 4 == 3]],
                                              "Q": [BBVolume2, [well for well in activeWellsButX if well % 4 == 0]]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    hardware.arduinoControl.stopHeating()
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    #hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_HalfVol_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [[EBVolume,EBVolume,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume,EBVolume], [well for well in activeWellsButX if well % 2 == 1]],
            "N": [[EBVolume,EBVolume,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume/2,EBVolume,EBVolume], [well for well in activeWellsButX if well % 2 == 0]],
            "A": [[NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume], A_wells],
            "C": [[NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume], C_wells],
            "G": [[NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume], G_wells],
            "T": [[NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume], T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume1,BBVolume1,BBVolume1,BBVolume1/2,BBVolume1,BBVolume1/2,BBVolume1,BBVolume1/2,BBVolume1,BBVolume1/2,BBVolume1,BBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume1,DBVolume1,DBVolume1,DBVolume1/2,DBVolume1,DBVolume1/2,DBVolume1,DBVolume1/2,DBVolume1,DBVolume1/2,DBVolume1,DBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume2,DBVolume2,DBVolume2,DBVolume2/2,DBVolume2,DBVolume2/2,DBVolume2,DBVolume2/2,DBVolume2,DBVolume2/2,DBVolume2,DBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [[BBVolume2,BBVolume2,BBVolume2,BBVolume2/2,BBVolume2,BBVolume2/2,BBVolume2,BBVolume2/2,BBVolume2,BBVolume2/2,BBVolume2,BBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_ROPtest_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)


        if (cycle<53):
            #Premix
            updateCycleLabel(hardware,cycle,"Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

            multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
                "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                "A": [NucsVolume, A_wells],
                "C": [NucsVolume, C_wells],
                "G": [NucsVolume, G_wells],
                "T": [NucsVolume, T_wells],
                "O": [NucsVolume, O_wells],
                "P": [NucsVolume, P_wells],
                "Q": [NucsVolume, Q_wells]
                }, is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, Elong_time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

            # W1
            updateCycleLabel(hardware, cycle, "W1")
            multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
            waitAndStir(hardware, WB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

            #DB1
            updateCycleLabel(hardware, cycle, "DB1")
            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            #DB2
            updateCycleLabel(hardware, cycle, "DB2")
            multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

            #Wash
            updateCycleLabel(hardware, cycle, "W2")
            multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        if (cycle > 52):
            # Premix
            updateCycleLabel(hardware, cycle, "Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

            multi_dispense_in_wells(hardware, {"Buff2": [50, inter([X_wells,wellListFromColumns([1,2,4,5,6,7,8,10,11,12])])],
                                               "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                               "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                               "A": [NucsVolume, A_wells],
                                               "C": [NucsVolume, C_wells],
                                               "G": [NucsVolume, G_wells],
                                               "T": [NucsVolume, T_wells],
                                               "O": [EBVolume, [well for well in wellListFromColumns([3,9]) if well % 2 == 1]],
                                               "P": [EBVolume, [well for well in wellListFromColumns([3,9]) if well % 2 == 0]],
                                               "Q": [NucsVolume, [well for well in wellListFromColumns([3,9])]]
                                               }, is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, Elong_time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

            # W1
            updateCycleLabel(hardware, cycle, "W1")
            multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, union([activeWellsButX, wellListFromColumns([4,10])])],
                                               "Buff2": [50, inter([X_wells, wellListFromColumns([1,2,3,5,6,7,8,9,11,12])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
            waitAndStir(hardware, WB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

            # DB1
            updateCycleLabel(hardware, cycle, "DB1")
            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, union([activeWellsButX, wellListFromColumns([5,11])])],
                                               "Buff2": [50, inter([X_wells,wellListFromColumns([1,2,3,4,6,7,8,9,10,12])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            # DB2
            updateCycleLabel(hardware, cycle, "DB2")
            multi_dispense_in_wells(hardware, {"DB": [DBVolume2, union([activeWellsButX, wellListFromColumns([5,11])])],
                                               "Buff2": [50, inter([X_wells,wellListFromColumns([1,2,3,4,6,7,8,9,10,12])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

            # Wash
            updateCycleLabel(hardware, cycle, "W2")
            multi_dispense_in_wells(hardware, {"BB": [BBVolume2, union([activeWellsButX, wellListFromColumns([6,12])])],
                                               "Buff2": [50, inter([X_wells,wellListFromColumns([1,2,3,4,5,7,8,9,10,11])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PDR_OneEnz_EightNucs_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")
    easygui.msgbox(msg="Do you test nucs ?", title="Nucs comparison", ok_button="Yes", image=None, root=None)

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, activeWellsButX],
            "N": [NucsVolume, N_wells],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2": 100})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_2DB_Xbuff2_Rev(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [NucsVolume, T_wells],
            "N": [NucsVolume, G_wells],
            "A": [BBVolume1, [well for well in X_wells if well % 4 == 1]],
            "C": [BBVolume1, [well for well in X_wells if well % 4 == 2]],
            "G": [BBVolume1, [well for well in X_wells if well % 4 == 3]],
            "T": [BBVolume1, [well for well in X_wells if well % 4 == 0]],
            "O": [NucsVolume, C_wells],
            "P": [NucsVolume, A_wells],
            "Q": [EBVolume, activeWellsButX]
            }, is384, reverse_order=1)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384, reverse_order=1)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, [well for well in inter([activeWellsButX, wellListFromColumns([1, 3, 5, 7, 9, 11])])]],
                                           "BB": [DBVolume1, [well for well in inter([activeWellsButX, wellListFromColumns([2, 4, 6, 8, 10, 12])])]]},is384, reverse_order=1)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {
            "DB": [DBVolume2, [well for well in inter([activeWellsButX, wellListFromColumns([1, 3, 5, 7, 9, 11])])]],
            "BB": [DBVolume2, [well for well in inter([activeWellsButX, wellListFromColumns([2, 4, 6, 8, 10, 12])])]]},
                                is384, reverse_order=1)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384, reverse_order=1)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBuff2Disp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBuff2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBuff2Vac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"A": [BBVolume2, [well for well in usedWells if well % 4 == 1]],
                                       "C": [BBVolume2, [well for well in usedWells if well % 4 == 2]],
                                       "G": [BBVolume2, [well for well in usedWells if well % 4 == 3]],
                                       "T": [BBVolume2, [well for well in usedWells if well % 4 == 0]]
                                       }, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"A": [BBVolume2, [well for well in usedWells if well % 4 == 1]],
                                       "C": [BBVolume2, [well for well in usedWells if well % 4 == 2]],
                                       "G": [BBVolume2, [well for well in usedWells if well % 4 == 3]],
                                       "T": [BBVolume2, [well for well in usedWells if well % 4 == 0]]
                                       }, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xbuff2_RevTest(hardware, is384):

        title = easygui.enterbox("Name of the run ?")

        # Save Quartet Control File
        saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
        if saveQuartet:
            saveQuartetControlFile(title, inspect.getsource(inspect.currentframe()))

        thermalImages = 1
        if thermalImages:
            TT = hardware.parent.rightFrame.thermalThread
        else:
            TT = FakeThermalImageThread()

        # Set up recording file for thermal snapshots
        now = datetime.datetime.now()
        folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
            now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
            now.second) + "_" + title

        TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

        # Lines
        uneven_enzyme = "M"
        even_enzyme = "N"
        A = "A"
        C = "C"
        G = "G"
        T = "T"
        O = "O"
        P = "P"
        Q = "Q"
        DB = "DB"
        Wash1 = "Buff1"
        Wash2 = "BB"
        Buff2 = "Buff2"

        cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

        while cycle != 0:

            updateCycleLabel(hardware, cycle, "")

            # We read the excel and get the parameters back
            synthesis_sheet = getExcelSheet(path)
            getParameters(synthesis_sheet)
            sequences = getSequences(synthesis_sheet)
            [ended_wells, A_wells, C_wells, G_wells, T_wells, M_wells, N_wells, O_wells, P_wells, X_wells, Q_wells] \
                = splitSequences(sequences, cycle)
            usedWells = getUsedWells(sequences)
            activeWells = getActiveWells(sequences, cycle)
            activeWellsButX = [well for well in activeWells if well not in X_wells]

            # print(nucleo_arrays)
            enz_vol = EBVolume
            nuc_vol = NucsVolume

            if (cycle == 1):
                removeSupernatant(hardware, VacuumTime)

                multi_dispense_in_wells(hardware, {"BB": [BBVolume2, usedWells]}, is384)

                waitAndStir(hardware, WB2Time)
                removeSupernatant(hardware, VacuumTime)

            # Premix
            updateCycleLabel(hardware, cycle, "Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

            multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, X_wells],
                                               "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                               "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                               "A": [NucsVolume, A_wells],
                                               "C": [NucsVolume, C_wells],
                                               "G": [NucsVolume, G_wells],
                                               "T": [NucsVolume, T_wells],
                                               "O": [NucsVolume, O_wells],
                                               "P": [NucsVolume, P_wells],
                                               "Q": [NucsVolume, Q_wells]
                                               }, is384, reverse_order=1)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, Elong_time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

            # W1
            updateCycleLabel(hardware, cycle, "W1")
            multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
            waitAndStir(hardware, WB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

            # DB1
            updateCycleLabel(hardware, cycle, "DB1")
            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            # DB2
            updateCycleLabel(hardware, cycle, "DB2")
            multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

            # Wash
            updateCycleLabel(hardware, cycle, "W2")
            multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

            # We carry on with next cycle or we end the loop
            nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
            if len(nucleo_arrays_nextcycle[0]) == len(sequences):
                cycle = 0
            else:
                cycle += 1

        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)
        waitAndStir(hardware, WB2Time)
        removeSupernatant(hardware, VacuumTime)
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

        goToWell(hardware, 'thermalCamera', 1, 0)
        updateCycleLabel(hardware, cycle, "Synthesis End")
        hardware.arduinoControl.stopHeating()
        DBRinseRoutine(hardware)

def Synthesis_OneEnz_EightNucs_4ElongTime_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[BBVolume2,X_wells],
            "M": [EBVolume, inter([activeWellsButX,wellListFromColumns([5,6,7,8])])],
            "N": [NucsVolume, inter([N_wells,wellListFromColumns([5,6,7,8])])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([5,6,7,8])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([5,6,7,8])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([5,6,7,8])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([5,6,7,8])])],
            "O": [NucsVolume, inter([O_wells,wellListFromColumns([5,6,7,8])])],
            "P": [NucsVolume, inter([P_wells,wellListFromColumns([5,6,7,8])])],
            "Q": [NucsVolume, inter([Q_wells,wellListFromColumns([5,6,7,8])])]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, inter([activeWellsButX,wellListFromColumns([9,10,11,12])])],
            "N": [NucsVolume, inter([N_wells,wellListFromColumns([9,10,11,12])])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([9,10,11,12])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([9,10,11,12])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([9,10,11,12])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([9,10,11,12])])],
            "O": [NucsVolume, inter([O_wells,wellListFromColumns([9,10,11,12])])],
            "P": [NucsVolume, inter([P_wells,wellListFromColumns([9,10,11,12])])],
            "Q": [NucsVolume, inter([Q_wells,wellListFromColumns([9,10,11,12])])]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, inter([activeWellsButX,wellListFromColumns([1,2,3,4])])],
            "N": [NucsVolume, inter([N_wells,wellListFromColumns([1,2,3,4])])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([1,2,3,4])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([1,2,3,4])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([1,2,3,4])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([1,2,3,4])])],
            "O": [NucsVolume, inter([O_wells,wellListFromColumns([1,2,3,4])])],
            "P": [NucsVolume, inter([P_wells,wellListFromColumns([1,2,3,4])])],
            "Q": [NucsVolume, inter([Q_wells,wellListFromColumns([1,2,3,4])])]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 180)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
            "P": [EBVolume, [well for well in activeWellsButX if well % 4 == 0]],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_TwoWB1_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
            "P": [EBVolume, [well for well in activeWellsButX if well % 4 == 0]],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff2": [BBVolume1, inter([activeWellsButX, wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_ThreeEnzMixed_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
            "P": [EBVolume*0.5, [well for well in activeWellsButX if well % 4 == 0]],
            "Q": [EBVolume*0.5, [well for well in activeWellsButX if well % 4 == 0]],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 60)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_TwoWB2_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff1":[BBVolume2, wellListFromColumns([1,2,3,4,5,7,9,11])],
                                              "Buff2": [BBVolume2, wellListFromColumns([6,8,10,12])]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[BBVolume2,X_wells],
            "M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
            "P": [EBVolume, [well for well in activeWellsButX if well % 4 == 0]],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, inter([activeWellsButX, wellListFromColumns([1,2,3,4,5,7,9,11])])],
                                           "Buff2": [BBVolume2, inter([activeWellsButX, wellListFromColumns([6,8,10,12])])]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, usedWells]}, is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    start=time.time()

    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]],
                            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_TwoDB_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    start=time.time()

    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff2":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
                            "M": [EBVolume, inter([wellListFromColumns([3,4,5,6,9,10,11,12]),[well for well in activeWellsButX if well % 2 == 1]])],
                            "N": [EBVolume, inter([wellListFromColumns([3,4,5,6,9,10,11,12]),[well for well in activeWellsButX if well % 2 == 0]])],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            "O": [EBVolume, inter([wellListFromColumns([1,2,7,8]),[well for well in activeWellsButX if well % 2 == 1]])],
                            "P": [EBVolume, inter([wellListFromColumns([1,2,7,8]),[well for well in activeWellsButX if well % 2 == 0]])]}, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([1,2,4,6,7,8,10,12])])],
                                           "BB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([3,5,9,11])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX, wellListFromColumns([1,2,4,6,7,8,10,12])])],
                                           "BB": [DBVolume2, inter([activeWellsButX, wellListFromColumns([3,5,9,11])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Degenerate_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    start=time.time()

    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        [ended_wells_deg, A_wells_deg, C_wells_deg, G_wells_deg, T_wells_deg] = splitSequencesDegenerate(sequences, cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        O_wells = [well for well in X_wells if well % 2 == 1]
        P_wells = [well for well in X_wells if well % 2 == 0]
        M_wells = [well for well in activeWellsButX if well % 2 == 1]
        N_wells = [well for well in activeWellsButX if well % 2 == 0]

        multi_dispense_in_wells_degenerate(hardware,
                                           {"O":[[50]*len(O_wells),O_wells],
                                            "P":[[50]*len(P_wells),P_wells],
                            "M": [[EBVolume]*len(M_wells), M_wells],
                            "N": [[EBVolume]*len(N_wells), N_wells],
                            "A": [[NucsVolume/well_divide[1] for well_divide in A_wells_deg], [well_divide[0] for well_divide in A_wells_deg]],
                            "C": [[NucsVolume/well_divide[1] for well_divide in C_wells_deg], [well_divide[0] for well_divide in C_wells_deg]],
                            "G": [[NucsVolume/well_divide[1] for well_divide in G_wells_deg], [well_divide[0] for well_divide in G_wells_deg]],
                            "T": [[NucsVolume/well_divide[1] for well_divide in T_wells_deg], [well_divide[0] for well_divide in T_wells_deg]]
                            }, is384,None, 0, 1)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        print('Cycle ',cycle,time.time()-start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    print('End ',time.time()-start)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def Synthesis_TwoEnz_TwoWB2_2G_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff1":[50, wellListFromColumns([1,2,4,5,6,9,10,11])],
                                              "Buff2": [50, wellListFromColumns([3,7,8,12])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]],
                            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            "Q": [NucsVolume, Q_wells]
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, inter([activeWellsButX,wellListFromColumns([1,2,4,5,6,9,10,11])])],
                                           "Buff2": [BBVolume2, inter([activeWellsButX,wellListFromColumns([3,7,8,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"O": 100, "P": 100})
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_ThreeWB2_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff1": [[BBVolume2/2,BBVolume2,0,BBVolume2/2,BBVolume2,0,BBVolume2/2,BBVolume2,0,BBVolume2/2,BBVolume2,0], wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])],
                                              "Buff2": [[BBVolume2/2,0,BBVolume2,BBVolume2/2,0,BBVolume2,BBVolume2/2,0,BBVolume2,BBVolume2/2,0,BBVolume2], wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]],
                            "M": [EBVolume, inter([activeWellsButX,wellListFromColumns([4,5,6,10,11,12])])],
                            "N": [EBVolume, inter([activeWellsButX,wellListFromColumns([1,2,3,7,8,9])])],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume2/2,BBVolume2,0,BBVolume2/2,BBVolume2,0,BBVolume2/2,BBVolume2,0,BBVolume2/2,BBVolume2,0], inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])])],
                                           "Buff2": [[BBVolume2/2,0,BBVolume2,BBVolume2/2,0,BBVolume2,BBVolume2/2,0,BBVolume2,BBVolume2/2,0,BBVolume2], inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])])]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_ThreeWB1_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB": [50, usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]],
                            "M": [EBVolume, inter([activeWellsButX,wellListFromColumns([1,2,3,7,8,9])])],
                            "N": [EBVolume, inter([activeWellsButX,wellListFromColumns([4,5,6,10,11,12])])],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume1*0.5,BBVolume1,0,BBVolume1*0.5,BBVolume1,0,BBVolume1*0.5,BBVolume1,0,BBVolume1*0.5,BBVolume1,0], inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])])],
                                           "Buff2": [[BBVolume1*0.5,0,BBVolume1,BBVolume1*0.5,0,BBVolume1,BBVolume1*0.5,0,BBVolume1,BBVolume1*0.5,0,BBVolume1], inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
                                           "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xbb(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"BB":[50,ended_wells],
                                           "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_Laura_Dismutase_2D(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + hardware.instrument_name + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        wells_std_3min30=[33,34,37,38,41,42,45,46]
        wells_ppase005_3min30=[35,39,43,47]
        wells_ppase001_3min30=[36,40,44,48]
        wells_ppi_3min30=[34,38,42,46]
        columns_3min30=[5,6]

        multi_dispense_in_wells(hardware, {"M": [EBVolume, wells_std_3min30],
                                           "N": [EBVolume, wells_ppase005_3min30],
                                           "O": [EBVolume, wells_ppase001_3min30],
                                           "Q": [4, wells_ppi_3min30],
                                           "A": [NucsVolume, inter([A_wells,columns_3min30])],
                                           "C": [NucsVolume, inter([C_wells,columns_3min30])],
                                           "G": [NucsVolume, inter([G_wells,columns_3min30])],
                                           "T": [NucsVolume, inter([T_wells,columns_3min30])],
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremix3min30Disp')
        waitAndStir(hardware, 3*60)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremix3min30Inc')

        wells_std_30s = [49,50,53,54,57,58,61,62]
        wells_ppase005_30s = [51,55,59,63]
        wells_ppase001_30s = [52,56,60,64]
        wells_ppi_30s = [50,54,58, 62]
        columns_30s = [7, 8]

        multi_dispense_in_wells(hardware, {"M": [EBVolume, wells_std_30s],
                                           "N": [EBVolume, wells_ppase005_30s],
                                           "O": [EBVolume, wells_ppase001_30s],
                                           "Q": [4, wells_ppi_30s],
                                           "A": [NucsVolume, inter([A_wells, columns_30s])],
                                           "C": [NucsVolume, inter([C_wells, columns_30s])],
                                           "G": [NucsVolume, inter([G_wells, columns_30s])],
                                           "T": [NucsVolume, inter([T_wells, columns_30s])],
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremix30sDisp')
        waitAndStir(hardware, 30)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremix30sInc')



        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware,{"P":500})
    multi_dispense_in_wells(hardware, {"P": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"P": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def Synthesis_TwoEnz_ThreeElongTime_ThreeWB2_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff1":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q": [50, X_wells],
                            "M": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([5,6,7,8]) if well % 2 == 1]])],
                            "N": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([5,6,7,8]) if well % 2 == 0]])],
                            "A": [NucsVolume, inter([A_wells,wellListFromColumns([5,6,7,8])])],
                            "C": [NucsVolume, inter([C_wells,wellListFromColumns([5,6,7,8])])],
                            "G": [NucsVolume, inter([G_wells,wellListFromColumns([5,6,7,8])])],
                            "T": [NucsVolume, inter([T_wells,wellListFromColumns([5,6,7,8])])],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 32)

        multi_dispense_in_wells(hardware, {"Q" : [50, X_wells],
                            "M": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([9,10,11,12]) if well % 2 == 1]])],
                            "N": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([9,10,11,12]) if well % 2 == 0]])],
                            "A": [NucsVolume, inter([A_wells,wellListFromColumns([9,10,11,12])])],
                            "C": [NucsVolume, inter([C_wells,wellListFromColumns([9,10,11,12])])],
                            "G": [NucsVolume, inter([G_wells,wellListFromColumns([9,10,11,12])])],
                            "T": [NucsVolume, inter([T_wells,wellListFromColumns([9,10,11,12])])],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 32)

        multi_dispense_in_wells(hardware, {"Q" : [50, X_wells],
                            "M": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([1,2,3,4]) if well % 2 == 1]])],
                            "N": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([1,2,3,4]) if well % 2 == 0]])],
                            "A": [NucsVolume, inter([A_wells,wellListFromColumns([1,2,3,4])])],
                            "C": [NucsVolume, inter([C_wells,wellListFromColumns([1,2,3,4])])],
                            "G": [NucsVolume, inter([G_wells,wellListFromColumns([1,2,3,4])])],
                            "T": [NucsVolume, inter([T_wells,wellListFromColumns([1,2,3,4])])],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 88)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume2,0,BBVolume2/2,0,BBVolume2,0,BBVolume2/2,0,BBVolume2,0,BBVolume2/2,0], inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff2": [[0,BBVolume2,BBVolume2/2,0,0,BBVolume2,BBVolume2/2,0,0,BBVolume2,BBVolume2/2,0], inter([activeWellsButX, wellListFromColumns([2,3,6,7,10,11])])],
                                           "O": [BBVolume2, inter([activeWellsButX, [well for well in wellListFromColumns([4,8,12]) if well % 2 == 1]])],
                                           "P": [BBVolume2, inter([activeWellsButX, [well for well in wellListFromColumns([4,8,12]) if well % 2 == 0]])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q" : [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q" : [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_Inkjet_Tblshoot(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff2":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        wells_std_bases=wellListFromHalfColumns([5,8,9,11])
        wells_inkjet_bases=wellListFromHalfColumns([6,7,10,12])

        multi_dispense_in_wells(hardware, {
                            "A": [50, A_wells],
                            "C": [50, C_wells],
                            "G": [50, G_wells],
                            "T": [50, T_wells],
                            "N": [50, N_wells],
                            "O": [50, O_wells],
                            "P": [50, P_wells],
                            "Q": [50, Q_wells],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")

        wells_DB_std=wellListFromColumns([3,4,6])
        wells_DB_inkjet=wellListFromColumns([5])

        multi_dispense_in_wells(hardware, {
            "DB": [DBVolume1, wells_DB_std],
            "BB": [DBVolume1, wells_DB_inkjet]},
        is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {
            "DB": [DBVolume2, wells_DB_std],
            "BB": [DBVolume2, wells_DB_inkjet]},
                                is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]},is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_ThreeEnz_TwoWB1_TwoWB2_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff1": [50, wellListFromColumns([1,4,7,8])],
                                              "Buff2": [50, wellListFromColumns([2,3,5,6,9,10,11,12])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
                            "M": [EBVolume, inter([activeWellsButX,wellListFromColumns([1,4,7,8])])],
                            "N": [EBVolume, inter([activeWellsButX, wellListFromColumns([2,5,9,10])])],
                            "O": [EBVolume, inter([activeWellsButX, wellListFromColumns([3,6,11,12])])],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, inter([activeWellsButX,wellListFromColumns([2,3,5,6,9,10,11,12])])]}, is384)
        multi_dispense_in_wells(hardware, {"P": [BBVolume1, inter([activeWellsButX,wellListFromColumns([1,4,7,8])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, inter([activeWellsButX, wellListFromColumns([1,4,7,8])])],
                                           "Buff2": [BBVolume2, inter([activeWellsButX, wellListFromColumns([2,3,5,6,9,10,11,12])])]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware,{"Q": 200})
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoWB1_TwoWB2_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff1": [50, wellListFromColumns([1,2,4,6,7,8,10,12])],
                                              "Buff2": [50, wellListFromColumns([3,5,9,11])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q": [50,X_wells],
                            "M": [EBVolume, inter([activeWellsButX, wellListFromColumns([1,3,4,6,7,9,10,12])])],
                            "N": [EBVolume, inter([activeWellsButX, wellListFromColumns([2,5,8,11])])],
                            "A": [NucsVolume, A_wells],
                            "C": [NucsVolume, C_wells],
                            "G": [NucsVolume, G_wells],
                            "T": [NucsVolume, T_wells],
                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume1, inter([activeWellsButX,wellListFromColumns([1,2,3,6,7,8,9,12])])],
                                           "O": [BBVolume1, inter([activeWellsButX,[well for well in wellListFromColumns([4,5,10,11]) if well % 2 == 0]])],
                                           "P": [BBVolume1, inter([activeWellsButX,[well for well in wellListFromColumns([4,5,10,11]) if well % 2 == 1]])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, inter([activeWellsButX,wellListFromColumns([1,2,4,6,7,8,10,12])])],
                                           "Buff2": [BBVolume2, inter([activeWellsButX,wellListFromColumns([3,5,9,11])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware,{"Q": 200})
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoWB1_DB1Time_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]],
                                           "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff2": [BBVolume1, inter([activeWellsButX, wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        if (cycle < 148):
            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([5,6,11,12])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
            waitAndStir(hardware, 9)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')

            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([3,4,9,10])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
            waitAndStir(hardware, 9)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')

            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([1,2,7,8])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
            waitAndStir(hardware, 12)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')
        if (cycle > 147):
            multi_dispense_in_wells(hardware,
                                    {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([5, 6, 11, 12])])]},
                                    is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
            waitAndStir(hardware, 5)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')

            multi_dispense_in_wells(hardware,
                                    {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([3, 4, 9, 10])])]},
                                    is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
            waitAndStir(hardware, 5)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')

            multi_dispense_in_wells(hardware,
                                    {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([1, 2, 7, 8])])]},
                                    is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
            waitAndStir(hardware, 6)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoWB1_DB1Time_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]],
                                           "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff2": [BBVolume1, inter([activeWellsButX, wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        if (cycle < 148):
            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([5,6,11,12])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
            waitAndStir(hardware, 9)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')

            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([1,2,7,8])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
            waitAndStir(hardware, 9)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')

            multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([3, 4, 9, 10])])]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
            waitAndStir(hardware, 12)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')
        if (cycle > 147):
            multi_dispense_in_wells(hardware,
                                    {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([5, 6, 11, 12])])]},
                                    is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
            waitAndStir(hardware, 5)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')

            multi_dispense_in_wells(hardware,
                                    {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([1, 2, 7, 8])])]},
                                    is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
            waitAndStir(hardware, 5)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')

            multi_dispense_in_wells(hardware,
                                    {"DB": [DBVolume1, inter([activeWellsButX, wellListFromColumns([3, 4, 9, 10])])]},
                                    is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
            waitAndStir(hardware, 6)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_EBTime_TwoWB1_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        multi_dispense_in_wells(hardware, {"O":[50,[well for well in X_wells if well % 2 == 1]],
                                           "P":[50,[well for well in X_wells if well % 2 == 0]]}, is384)
        multi_dispense_in_wells(hardware,{
            "M": [EBVolume, [well for well in inter([wellListFromColumns([3,4]),activeWellsButX]) if well % 2 == 1]],
            "N": [EBVolume, [well for well in inter([wellListFromColumns([3,4]),activeWellsButX]) if well % 2 == 0]],
            "A": [NucsVolume, inter([wellListFromColumns([3,4]),A_wells])],
            "C": [NucsVolume, inter([wellListFromColumns([3,4]),C_wells])],
            "G": [NucsVolume, inter([wellListFromColumns([3,4]),G_wells])],
            "T": [NucsVolume, inter([wellListFromColumns([3,4]),T_wells])],
            }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 14)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, [well for well in inter([wellListFromColumns([5, 6, 7]), activeWellsButX]) if well % 2 == 1]],
            "N": [EBVolume, [well for well in inter([wellListFromColumns([5, 6, 7]), activeWellsButX]) if well % 2 == 0]],
            "A": [NucsVolume, inter([wellListFromColumns([5, 6, 7]), A_wells])],
            "C": [NucsVolume, inter([wellListFromColumns([5, 6, 7]), C_wells])],
            "G": [NucsVolume, inter([wellListFromColumns([5, 6, 7]), G_wells])],
            "T": [NucsVolume, inter([wellListFromColumns([5, 6, 7]), T_wells])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 14)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, [well for well in inter([wellListFromColumns([1,2]),activeWellsButX]) if well % 2 == 1]],
            "N": [EBVolume, [well for well in inter([wellListFromColumns([1,2]),activeWellsButX]) if well % 2 == 0]],
            "A": [NucsVolume, inter([wellListFromColumns([1,2]),A_wells])],
            "C": [NucsVolume, inter([wellListFromColumns([1,2]),C_wells])],
            "G": [NucsVolume, inter([wellListFromColumns([1,2]),G_wells])],
            "T": [NucsVolume, inter([wellListFromColumns([1,2]),T_wells])],
            }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 180)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX,wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff2": [BBVolume1, inter([activeWellsButX,wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 ==1]],
                                       "P": [50, [well for well in usedWells if well % 2 ==0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoWB1_2xWB2_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q": [BBVolume2,X_wells],
                                           "M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
                                           "P": [EBVolume, [well for well in activeWellsButX if well % 4 == 0]]
                                            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "Buff2": [BBVolume1, inter([activeWellsButX, wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc2')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FourWB1_TwoWB2_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,wellListFromColumns([1,3,5,7,9,11])],
                                              "Buff1":[50,wellListFromColumns([2,4,6,8,10,12])]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, activeWellsButX],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "Buff2": [BBVolume2, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"N": [BBVolume1, [well for well in activeWellsButX if well % 4 == 1]],
                                           "O": [BBVolume1, [well for well in activeWellsButX if well % 4 == 2]],
                                           "P": [BBVolume1, [well for well in activeWellsButX if well % 4 == 3]],
                                           "Q": [BBVolume1, [well for well in activeWellsButX if well % 4 == 0]],
                                           }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB":[BBVolume2,wellListFromColumns([1,3,5,7,9,11])],
                                              "Buff1":[BBVolume2,wellListFromColumns([2,4,6,8,10,12])]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FourWB1_XtraWash_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, activeWellsButX],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "Buff2": [BBVolume2, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")

        if cycle in [50,100,150,200,250,300,347]:
            multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftXtraW1Disp')
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftXtraW1Inc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftXtraW1Vac')

        multi_dispense_in_wells(hardware, {"N": [BBVolume1, [well for well in  activeWellsButX if well % 4 ==1]],
                                           "O": [BBVolume1, [well for well in  activeWellsButX if well % 4 ==2]],
                                           "P": [BBVolume1, [well for well in  activeWellsButX if well % 4 ==3]],
                                           "Q": [BBVolume1, [well for well in  activeWellsButX if well % 4 ==0]],
                                           }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PSPWashes_96OP_extraH20andEtOH_Input(hardware, is384):
    title = easygui.enterbox("Name of the PSP ?")
    TT = hardware.parent.rightFrame.thermalThread
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_PSP_" + title

    TT.snapshot_in_cycle(1, folder_path, 1, 'BeforeAnything')

    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet(path)
    getParameters(synthesis_sheet)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    vacuum_time = 30  # s

    # LINES
    TSTPK = "M"
    LB = "N"
    H20 = "DB"
    ETH = "Buff1"
    ISOP = "BB"

    # STEPS
    PREWASH_H2O_1 = 1
    PREWASH_TSTPK = 1
    PREWASH_H2O_2 = 1
    PREWASH_IPA = 1
    PREDRYING = 1
    LIBERATION = 1
    PRECIPITATION = 1
    DESALTING = 1
    DRYING = 1

    input("Press enter")
    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)
            input("Press enter")

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)
            input("Press enter")

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 200, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60, 700)
            removeSupernatant(hardware, vacuum_time)
            input("Press enter")

        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)
            input("Press enter")

        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            dispenseWashes(hardware, 200, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60, 700)
            removeSupernatant(hardware, vacuum_time)
            input("Press enter")

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)
            input("Press enter")

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')
        input("Press enter")

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        multiDispensePumps(hardware, [0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        dispensePumps(hardware, [0, 50, 0, 0, 0, 0, 0, 0], [], usedWells, [], [], [], [], [], [], is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware, 1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')

    if PRECIPITATION:
        updateCycleLabel(hardware, 1, "Precipitation")
        multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
        dispenseWashes(hardware, 200, ISOP, usedWells, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp_200')
        wait(hardware, 10 * 60)
        removeSupernatant(hardware, 40)
        waitAndStir(hardware, 5, 1100)

    if DESALTING:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Desalting")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)
        waitAndStir(hardware, 5, 1100)

        for nb in range(1):
            updateCycleLabel(hardware, nb + 1, "Desalting_IPA")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_IPA_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)
        waitAndStir(hardware, 5, 1100)

    if DRYING:
        updateCycleLabel(hardware, 1, "Drying")
        removeSupernatant(hardware, 15 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Drying')
        hardware.arduinoControl.stopHeating()

    updateCycleLabel(hardware, 0, "PSP Done")

def Synthesis_FourEnz_TwoDB_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,11,12])])]],
                                           "N": [EBVolume, [well for well in inter([activeWellsButX,wellListFromColumns([8])])]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [EBVolume, [well for well in inter([activeWellsButX,wellListFromColumns([9])])]],
                                           "P": [EBVolume, [well for well in inter([activeWellsButX,wellListFromColumns([10])])]],
                                           "Q": [BBVolume2, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, [well for well in inter([activeWellsButX, wellListFromColumns([1,2,3,4,6,7,8,9,10,11])])]],
                                           "BB": [DBVolume1, [well for well in inter([activeWellsButX, wellListFromColumns([5,12])])]]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, [well for well in inter([activeWellsButX, wellListFromColumns([1,2,3,4,6,7,8,9,10,11])])]],
                                           "BB": [DBVolume2, [well for well in inter([activeWellsButX, wellListFromColumns([5,12])])]]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_FourEnz_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
                                           "P": [EBVolume, [well for well in activeWellsButX if well % 4 == 0]],
                                           "Buff2": [50, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2": 100})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoDB_TwoX(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        activeWellsButXQ = [well for well in activeWells if well not in union([X_wells , Q_wells])]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, [well for well in activeWellsButXQ if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButXQ if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
            "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]],
            "Q": [BBVolume2, Q_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButXQ]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButXQ,wellListFromColumns([8,9,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButXQ,wellListFromColumns([10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButXQ,wellListFromColumns([8,9,11])])],
                                           "BB": [DBVolume2, inter([activeWellsButXQ,wellListFromColumns([10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButXQ]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoDB_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
            "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([1,3,5,7,9,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([1,3,5,7,9,11])])],
                                           "BB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PDR_Synthesis_TwoEnz_TwoDB_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")
    easygui.msgbox(msg="Do you test two DB ?", title="DB comparison", ok_button="Yes", image=None, root=None)

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
            "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromHalfColumns([1,4,5,8,9,12,13,16,18,19,22,23])])],
                                            "BB": [DBVolume1, inter([activeWellsButX,wellListFromHalfColumns([2,3,6,7,10,11,14,15,17,20,21,24])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX,wellListFromHalfColumns([1,4,5,8,9,12,13,16,18,19,22,23])])],
                                            "BB": [DBVolume2, inter([activeWellsButX,wellListFromHalfColumns([2,3,6,7,10,11,14,15,17,20,21,24])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PDR_Synthesis_TwoEnz_TwoDB_FullColumn_Xop(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"
    Buff2 = "Buff2"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
            "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([1,3,5,7,9,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([1,3,5,7,9,11])])],
                                           "BB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([2,4,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]]
                                       }, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_EightDiffWB1_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        ended_wells = getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{Wash2:[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {Wash2: [BBVolume2, ended_wells]}, is384)
        multi_dispense_in_wells(hardware, {uneven_enzyme: [EBVolume, activeWellsButX], A: [nuc_vol, A_wells]}, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {
            C: [BBVolume1, [well for well in activeWellsButX if well % 8 == 1]],
            G: [BBVolume1, [well for well in activeWellsButX if well % 8 == 2]],
            T: [BBVolume1, [well for well in activeWellsButX if well % 8 == 3]],
            Q: [BBVolume1, [well for well in activeWellsButX if well % 8 == 4 or well % 8 == 0]],
            even_enzyme: [BBVolume1, [well for well in activeWellsButX if well % 8 == 5]],
            O: [BBVolume1, [well for well in activeWellsButX if well % 8 == 6]],
            P: [BBVolume1, [well for well in activeWellsButX if well % 8 == 7]],
            }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {DB: [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {DB: [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {Wash2: [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_4EBIncTime_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[50,X_wells],
            "M": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([3,7,11]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([3,7,11]) if well % 2 == 0]])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([3,4,7,8,11,12])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([3,4,7,8,11,12])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([3,4,7,8,11,12])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([3,4,7,8,11,12])])],
            "O": [EBVolume, inter([activeWellsButX,wellListFromColumns([4,8,12])])],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 9)

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([1,5,9]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([1,5,9]) if well % 2 == 0]])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([1,5,9])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([1,5,9])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([1,5,9])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([1,5,9])])],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            "Q": [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 9)

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([2,6,10]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([2,6,10]) if well % 2 == 0]])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([2,6,10])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([2,6,10])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([2,6,10])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([2,6,10])])],
            O: [NucsVolume, O_wells],
            P: [NucsVolume, P_wells],
            Q: [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 88)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_4EBIncTime_ExtraPK_Xq(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Q":[50,X_wells],
            "M": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([7]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX,[well for well in wellListFromColumns([7]) if well % 2 == 0]])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([7])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([7])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([7])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([7])])],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 18)

        multi_dispense_in_wells(hardware, {
               "M": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([5]) if well % 2 == 1]])],
               "N": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([5]) if well % 2 == 0]])],
               "A": [NucsVolume, inter([A_wells, wellListFromColumns([5])])],
               "C": [NucsVolume, inter([C_wells, wellListFromColumns([5])])],
               "G": [NucsVolume, inter([G_wells, wellListFromColumns([5])])],
               "T": [NucsVolume, inter([T_wells, wellListFromColumns([5])])],
               "O": [NucsVolume, O_wells],
               "P": [NucsVolume, P_wells],
               }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        if (cycle < 449):
            waitAndStir(hardware, 18)
        else :
            waitAndStir(hardware, 7)

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([4,8,9]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([4,8,9]) if well % 2 == 0]])],
            "A": [NucsVolume, inter([activeWellsButX,A_wells,wellListFromColumns([4,8,9])])],
            "C": [NucsVolume, inter([activeWellsButX,C_wells,wellListFromColumns([4,8,9])])],
            "G": [NucsVolume, inter([activeWellsButX,G_wells,wellListFromColumns([4,8,9])])],
            "T": [NucsVolume, inter([activeWellsButX,T_wells,wellListFromColumns([4,8,9])])],
            "O": [NucsVolume, O_wells],
            "P": [NucsVolume, P_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 18)

        multi_dispense_in_wells(hardware, {
            "M": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([6]) if well % 2 == 1]])],
            "N": [EBVolume, inter([activeWellsButX, [well for well in wellListFromColumns([6]) if well % 2 == 0]])],
            "A": [NucsVolume, inter([A_wells,wellListFromColumns([6])])],
            "C": [NucsVolume, inter([C_wells,wellListFromColumns([6])])],
            "G": [NucsVolume, inter([G_wells,wellListFromColumns([6])])],
            "T": [NucsVolume, inter([T_wells,wellListFromColumns([6])])],
            O: [NucsVolume, O_wells],
            P: [NucsVolume, P_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp4')
        waitAndStir(hardware, 118)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        if (cycle % 50 == 0):
            waitAndStir(hardware, 300)
        else :
            waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_OneStepDB_FourTimeDB_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{Wash2:[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[BBVolume2,X_wells],
            uneven_enzyme: [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
            even_enzyme: [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
            A: [NucsVolume, A_wells],
            C: [NucsVolume, C_wells],
            G: [NucsVolume, G_wells],
            T: [NucsVolume, T_wells],
            O: [NucsVolume, O_wells],
            P: [NucsVolume, P_wells],
            Q: [NucsVolume, Q_wells]
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {Wash1: [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB
        updateCycleLabel(hardware, cycle, "DB")
        multi_dispense_in_wells(hardware, {DB: [DBVolume1, wellListFromColumns([2, 6, 10])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        waitAndStir(hardware, 51)
        multi_dispense_in_wells(hardware, {DB: [DBVolume1, wellListFromColumns([4, 8, 12])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, 51)
        multi_dispense_in_wells(hardware, {DB: [DBVolume1, wellListFromColumns([3, 7, 11])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
        waitAndStir(hardware, 51)
        multi_dispense_in_wells(hardware, {DB: [DBVolume1, wellListFromColumns([1, 5, 9])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp4')
        waitAndStir(hardware, 26)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {Wash2: [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_TwoWB1_OneStepTwoDB_ThreeTimeDB_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff1":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[BBVolume2,X_wells],
            "M": [EBVolume, activeWellsButX],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"N": [BBVolume1, [well for well in activeWellsButX if well % 4 == 1]],
                                           "O": [BBVolume1, [well for well in activeWellsButX if well % 4 == 2]],
                                           "P": [BBVolume1, [well for well in activeWellsButX if well % 4 == 3]],
                                           "Q": [BBVolume1, [well for well in activeWellsButX if well % 4 == 0]]
                                           }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB
        updateCycleLabel(hardware, cycle, "DB")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([3,9])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([4,10])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        waitAndStir(hardware, 24)
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([5,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([6,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, 24)
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([1,7])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([2,8])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
        waitAndStir(hardware, 86)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_TwoWB1_TwoDB_ThreeTimeDB1_Xbuff2(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{"Buff1":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"Buff2":[BBVolume2,X_wells],
            "M": [EBVolume, activeWellsButX],
            "A": [NucsVolume, A_wells],
            "C": [NucsVolume, C_wells],
            "G": [NucsVolume, G_wells],
            "T": [NucsVolume, T_wells],
            }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"N": [BBVolume1, [well for well in activeWellsButX if well % 4 == 1]],
                                           "O": [BBVolume1, [well for well in activeWellsButX if well % 4 == 2]],
                                           "P": [BBVolume1, [well for well in activeWellsButX if well % 4 == 3]],
                                           "Q": [BBVolume1, [well for well in activeWellsButX if well % 4 == 0]]
                                           }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([1,7])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([2,8])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        waitAndStir(hardware, 8)
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([5,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([6,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, 12)
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([3,9])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([4,10])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
        waitAndStir(hardware, 7)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX, wellListFromColumns([1,3,5,7,9,11])])],
                                           "BB": [DBVolume2, inter([activeWellsButX, wellListFromColumns([2,4,6,8,10,12])])]
                                           }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume2, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_DiffVolCol_X(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    #Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells (sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware,{Wash2:[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {uneven_enzyme: [[EBVolume*0.7,EBVolume,EBVolume*0.5,EBVolume*0.6,EBVolume*0.7,EBVolume,EBVolume*0.5,EBVolume,EBVolume*0.7,EBVolume,EBVolume*0.5,EBVolume*0.6], [well for well in activeWellsButX if well % 2 == 1]],
                                           even_enzyme: [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           A: [NucsVolume, A_wells],
                                           C: [NucsVolume, C_wells],
                                           G: [NucsVolume, G_wells],
                                           T: [NucsVolume, T_wells],
                                           O: [BBVolume2, X_wells],
                                           P: [NucsVolume, P_wells],
                                           Q: [NucsVolume, Q_wells]
                                           }, is384)
        
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {Wash1: [[BBVolume1*0.7,BBVolume1,BBVolume1*0.5,BBVolume1*0.6,BBVolume1*0.7,BBVolume1,BBVolume1*0.5,BBVolume1,BBVolume1*0.7,BBVolume1,BBVolume1*0.5,BBVolume1*0.6], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {DB: [[DBVolume1*0.7,DBVolume1,DBVolume1*0.5,DBVolume1*0.6,DBVolume1*0.7,DBVolume1,DBVolume1*0.5,DBVolume1,DBVolume1*0.7,DBVolume1,DBVolume1*0.5,DBVolume1*0.6], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {DB: [[DBVolume2*0.7,DBVolume2,DBVolume2*0.5,DBVolume2*0.6,DBVolume2*0.7,DBVolume2,DBVolume2*0.5,DBVolume2,DBVolume2*0.7,DBVolume2,DBVolume2*0.5,DBVolume2*0.6], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {Wash2: [[BBVolume2*0.7,BBVolume2,BBVolume2*0.5,BBVolume2*0.6,BBVolume2*0.7,BBVolume2,BBVolume2*0.5,BBVolume2,BBVolume2*0.7,BBVolume2,BBVolume2*0.5,BBVolume2*0.6], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {O: [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {O: [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_DiffVolCol_DoubleWB2_XPK_Xbuff2(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title, inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    # Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells, A_wells, C_wells, G_wells, T_wells, M_wells, N_wells, O_wells, P_wells, X_wells, Q_wells] \
            = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware, {"BB": [BBVolume2, usedWells]}, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [[EBVolume, EBVolume*0.5, EBVolume * 1, EBVolume * 0.6, EBVolume * 0.6, EBVolume*0.5, EBVolume * 0.5,
                                                EBVolume, EBVolume * 0.6, EBVolume*0.6, EBVolume * 0.5, EBVolume * 0.5], [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [[EBVolume, EBVolume*0.5, EBVolume * 1, EBVolume * 0.6, EBVolume * 0.6, EBVolume*0.5, EBVolume * 0.5,
                                                EBVolume, EBVolume * 0.6, EBVolume*0.6, EBVolume * 0.5, EBVolume * 0.5], [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [[NucsVolume, NucsVolume*0.5, NucsVolume * 1, NucsVolume * 0.6, NucsVolume * 0.6, NucsVolume*0.5, NucsVolume * 0.5,
                                                NucsVolume, NucsVolume * 0.6, NucsVolume*0.6, NucsVolume * 0.5, NucsVolume * 0.5], A_wells],
                                           "C": [[NucsVolume, NucsVolume*0.5, NucsVolume * 1, NucsVolume * 0.6, NucsVolume * 0.6, NucsVolume*0.5, NucsVolume * 0.5,
                                                NucsVolume, NucsVolume * 0.6, NucsVolume*0.6, NucsVolume * 0.5, NucsVolume * 0.5], C_wells],
                                           "G": [[NucsVolume, NucsVolume*0.5, NucsVolume * 1, NucsVolume * 0.6, NucsVolume * 0.6, NucsVolume*0.5, NucsVolume * 0.5,
                                                NucsVolume, NucsVolume * 0.6, NucsVolume*0.6, NucsVolume * 0.5, NucsVolume * 0.5], G_wells],
                                           "T": [[NucsVolume, NucsVolume*0.5, NucsVolume * 1, NucsVolume * 0.6, NucsVolume * 0.6, NucsVolume*0.5, NucsVolume * 0.5,
                                                NucsVolume, NucsVolume * 0.6, NucsVolume*0.6, NucsVolume * 0.5, NucsVolume * 0.5], T_wells],
                                           "Q": [BBVolume2, Q_wells],
                                           "Buff2": [BBVolume2, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        if cycle in [50,100,150,200,250,300,350,400,448]:
            multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, usedWells]}, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftpKDisp')
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftpKInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftpKVac')

        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume1, BBVolume1*0.5, BBVolume1, BBVolume1 * 0.6, BBVolume1, BBVolume1*0.5, BBVolume1,
                                                    BBVolume1, BBVolume1 * 0.6, BBVolume1, BBVolume1 * 0.5, BBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume1, DBVolume1*0.5, DBVolume1, DBVolume1 * 0.6, DBVolume1, DBVolume1*0.5, DBVolume1,
                                                DBVolume1, DBVolume1 * 0.6, DBVolume1, DBVolume1 * 0.5, DBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume2, 20, DBVolume2, 20, DBVolume2, 20, DBVolume2,
                                                DBVolume2, 20, DBVolume2, 20, DBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [[BBVolume2, BBVolume2*0.5, BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2*0.5, BBVolume2,
                                                BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.5, BBVolume2 *1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        multi_dispense_in_wells(hardware, {
            "BB": [[BBVolume2, BBVolume2 * 0.5, BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.5, BBVolume2,
                    BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.5, BBVolume2 * 1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc2')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoDB_DiffVolCol_X(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title, inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    # Lines
    uneven_enzyme = "M"
    even_enzyme = "N"
    A = "A"
    C = "C"
    G = "G"
    T = "T"
    O = "O"
    P = "P"
    Q = "Q"
    DB = "DB"
    Wash1 = "Buff1"
    Wash2 = "BB"

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        [ended_wells, A_wells, C_wells, G_wells, T_wells, M_wells, N_wells, O_wells, P_wells, X_wells, Q_wells] \
            = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, usedWells]}, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {
                                           "M": [[EBVolume* 0.5, EBVolume* 0.5, EBVolume * 0.5, EBVolume * 0.5, EBVolume* 0.5, EBVolume* 0.5, EBVolume,
             EBVolume, EBVolume, EBVolume, EBVolume, EBVolume], [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [[EBVolume* 0.5, EBVolume* 0.5, EBVolume * 0.5, EBVolume * 0.5, EBVolume* 0.5, EBVolume* 0.5, EBVolume,
             EBVolume, EBVolume, EBVolume, EBVolume, EBVolume], [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [[EBVolume* 0.5, EBVolume* 0.5, EBVolume * 0.5, EBVolume * 0.5, EBVolume* 0.5, EBVolume* 0.5, EBVolume,
             EBVolume, EBVolume, EBVolume, EBVolume, EBVolume], A_wells],
                                           "C": [[EBVolume* 0.5, EBVolume* 0.5, EBVolume * 0.5, EBVolume * 0.5, EBVolume* 0.5, EBVolume* 0.5, EBVolume,
             EBVolume, EBVolume, EBVolume, EBVolume, EBVolume], C_wells],
                                           "G": [[EBVolume* 0.5, EBVolume* 0.5, EBVolume * 0.5, EBVolume * 0.5, EBVolume* 0.5, EBVolume* 0.5, EBVolume,
             EBVolume, EBVolume, EBVolume, EBVolume, EBVolume], G_wells],
                                           "T": [[EBVolume* 0.5, EBVolume* 0.5, EBVolume * 0.5, EBVolume * 0.5, EBVolume* 0.5, EBVolume* 0.5, EBVolume,
             EBVolume, EBVolume, EBVolume, EBVolume, EBVolume], T_wells],
                                           "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                           "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]],
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [
            [BBVolume1, BBVolume1 * 0.5, BBVolume1 * 0.5, BBVolume1, BBVolume1, BBVolume1, BBVolume1,
             BBVolume1, BBVolume1, BBVolume1, BBVolume1, BBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {
                "DB": [[DBVolume1, DBVolume1 * 0.5, DBVolume1, DBVolume1, DBVolume1, DBVolume1, DBVolume1,
             DBVolume1, DBVolume1, DBVolume1, DBVolume1, DBVolume1], [well for well in inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,7,9,11])])]],
                "BB": [[DBVolume1, DBVolume1 * 0.5, DBVolume1, DBVolume1, DBVolume1, DBVolume1, DBVolume1,
             DBVolume1, DBVolume1, DBVolume1, DBVolume1, DBVolume1], [well for well in inter([activeWellsButX,wellListFromColumns([6,8,10,12])])]]
             }, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {
            "DB": [[DBVolume2, DBVolume2 * 0.84, DBVolume2, DBVolume2, DBVolume2, DBVolume2, DBVolume2,
                  DBVolume2, DBVolume2, DBVolume2, DBVolume2, DBVolume2], [well for well in inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,7,9,11])])]],
            "BB": [[DBVolume2, DBVolume2 * 0.84, DBVolume2, DBVolume2, DBVolume2, DBVolume2, DBVolume2,
                    DBVolume2, DBVolume2, DBVolume2, DBVolume2, DBVolume2], [well for well in inter([activeWellsButX,wellListFromColumns([6,8,10,12])])]]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"Buff2": [
            [BBVolume2, BBVolume2 * 0.5, BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2,
             BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                           "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]],}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in usedWells if well % 2 == 1]],
                                           "P": [BBVolume2, [well for well in usedWells if well % 2 == 0]],}, is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_CR0inX(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        X_wells=nucleo_arrays[9]
        usedWells=getUsedWells(sequences)
        activeWellsButX=getActiveWellsButX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWellsButX if well%2==1], [well for well in activeWellsButX if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)
        dispenseWashes(hardware, 50, 'Buff2', X_wells, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWellsButX, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWellsButX, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWellsButX, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWellsButX,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    for i in range(2):
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        waitAndStir(hardware, 10)
        removeSupernatant(hardware, VacuumTime)

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_ElongVol_ElongTime_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix

        well15 = wellListFromColumns([10, 11])
        well1 = wellListFromColumns([3, 7, 9, 12])
        well2 = wellListFromColumns([1, 5])
        well3 = wellListFromColumns([2, 6])
        well4 = wellListFromColumns([4, 8])

        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [15, 15, 15, 15, 15, 15, 15, 15, 15],
                        [well for well in well15],
                        inter([well15, nucleo_arrays[6]]),
                        inter([well15, nucleo_arrays[1]]),
                        inter([well15, nucleo_arrays[2]]),
                        inter([well15, nucleo_arrays[3]]),
                        inter([well15, nucleo_arrays[4]]),
                        inter([well15, nucleo_arrays[7]]),
                        inter([well15, nucleo_arrays[8]]),
                        inter([well15, nucleo_arrays[10]]),
                        is384)
        dispensePumps_Q(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                        [well for well in well1],
                        inter([well1,nucleo_arrays[6]]),
                        inter([well1,nucleo_arrays[1]]),
                        inter([well1,nucleo_arrays[2]]),
                        inter([well1,nucleo_arrays[3]]),
                        inter([well1,nucleo_arrays[4]]),
                        inter([well1,nucleo_arrays[7]]),
                        inter([well1,nucleo_arrays[8]]),
                        inter([well1,nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        [well for well in well2],
                        inter([well2, nucleo_arrays[6]]),
                        inter([well2, nucleo_arrays[1]]),
                        inter([well2, nucleo_arrays[2]]),
                        inter([well2, nucleo_arrays[3]]),
                        inter([well2, nucleo_arrays[4]]),
                        inter([well2, nucleo_arrays[7]]),
                        inter([well2, nucleo_arrays[8]]),
                        inter([well2, nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        [well for well in well3],
                        inter([well3, nucleo_arrays[6]]),
                        inter([well3, nucleo_arrays[1]]),
                        inter([well3, nucleo_arrays[2]]),
                        inter([well3, nucleo_arrays[3]]),
                        inter([well3, nucleo_arrays[4]]),
                        inter([well3, nucleo_arrays[7]]),
                        inter([well3, nucleo_arrays[8]]),
                        inter([well3, nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        [well for well in well4],
                        inter([well4, nucleo_arrays[6]]),
                        inter([well4, nucleo_arrays[1]]),
                        inter([well4, nucleo_arrays[2]]),
                        inter([well4, nucleo_arrays[3]]),
                        inter([well4, nucleo_arrays[4]]),
                        inter([well4, nucleo_arrays[7]]),
                        inter([well4, nucleo_arrays[8]]),
                        inter([well4, nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp4')
        waitAndStir(hardware, 110)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc4')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_ElongVol_ElongTime_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix

        well15 = wellListFromColumns([10, 11])
        well1 = wellListFromColumns([3, 7, 9, 12])
        well2 = wellListFromColumns([1, 5])
        well3 = wellListFromColumns([2, 6])
        well4 = wellListFromColumns([4, 8])

        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [15, 15, 15, 15, 15, 15, 15, 15, 15],
                        [well for well in well15],
                        inter([well15, nucleo_arrays[6]]),
                        inter([well15, nucleo_arrays[1]]),
                        inter([well15, nucleo_arrays[2]]),
                        inter([well15, nucleo_arrays[3]]),
                        inter([well15, nucleo_arrays[4]]),
                        inter([well15, nucleo_arrays[7]]),
                        inter([well15, nucleo_arrays[8]]),
                        inter([well15, nucleo_arrays[10]]),
                        is384)
        dispensePumps_Q(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                        [well for well in well1],
                        inter([well1,nucleo_arrays[6]]),
                        inter([well1,nucleo_arrays[1]]),
                        inter([well1,nucleo_arrays[2]]),
                        inter([well1,nucleo_arrays[3]]),
                        inter([well1,nucleo_arrays[4]]),
                        inter([well1,nucleo_arrays[7]]),
                        inter([well1,nucleo_arrays[8]]),
                        inter([well1,nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        [well for well in well2],
                        inter([well2, nucleo_arrays[6]]),
                        inter([well2, nucleo_arrays[1]]),
                        inter([well2, nucleo_arrays[2]]),
                        inter([well2, nucleo_arrays[3]]),
                        inter([well2, nucleo_arrays[4]]),
                        inter([well2, nucleo_arrays[7]]),
                        inter([well2, nucleo_arrays[8]]),
                        inter([well2, nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        [well for well in well3],
                        inter([well3, nucleo_arrays[6]]),
                        inter([well3, nucleo_arrays[1]]),
                        inter([well3, nucleo_arrays[2]]),
                        inter([well3, nucleo_arrays[3]]),
                        inter([well3, nucleo_arrays[4]]),
                        inter([well3, nucleo_arrays[7]]),
                        inter([well3, nucleo_arrays[8]]),
                        inter([well3, nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        [well for well in well4],
                        inter([well4, nucleo_arrays[6]]),
                        inter([well4, nucleo_arrays[1]]),
                        inter([well4, nucleo_arrays[2]]),
                        inter([well4, nucleo_arrays[3]]),
                        inter([well4, nucleo_arrays[4]]),
                        inter([well4, nucleo_arrays[7]]),
                        inter([well4, nucleo_arrays[8]]),
                        inter([well4, nucleo_arrays[10]]),
                        is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp4')
        waitAndStir(hardware, 110)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc4')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_EndedN_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,50,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], activeWells, endedWells, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoDiffEnz_TwoDiffWB1_TwoDiffWB2_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1,2,5,6,9,10]), is384)
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([3,4,7,8,11,12]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if (well%4==2 or well%4==3 or well%4==0)], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', wellListFromColumns([1,2,4,5,6,8,9,10,12]), is384)
        dispensePumps(hardware, [0,0,0,0,0,0, BBVolume1, BBVolume1], [],[], [], [], [], [],[well for well in wellListFromColumns([3,7,11]) if well%2==1], [well for well in wellListFromColumns([3,7,11]) if well%2==0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1, 2, 5, 6, 9, 10]), is384)
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([3, 4, 7, 8, 11, 12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1, 2, 5, 6, 9, 10]), is384)
    dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([3, 4, 7, 8, 11, 12]), is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoDiffEnz_TwoDiffWB1_TwoDiffDB_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps_Q(hardware, [0,0,0,0,0,0, BBVolume1, 0, BBVolume1], [],[], [], [], [], [],[well for well in usedWells if (well%4==1 or well%4==2)], [], [well for well in usedWells if (well%4==3 or well%4==0)], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1,'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2,'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_24Ended_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)
        endedwells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1',wellListFromColumns([1,3,5,7,9,11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        well147=inter([wellListFromColumns([5,6,7,8,9,10,11,12]),activeWells])
        well52=inter([wellListFromColumns([1,3,5,7,9,11]),activeWells])
        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePumps(hardware, [enz_vol,50,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in well147], [well for well in endedwells], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [well for well in wellListFromColumns([1,3])], [well for well in wellListFromColumns([2,4])],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', [well for well in well52] ,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [enz_vol, 50, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                  [], usedWells, [],[],[],[],[],[], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoWB1_OneStepDB_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1.1")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([9,10]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        waitAndStir(hardware, 54)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')

        updateCycleLabel(hardware, cycle, "DB1.2")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([1,2]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, 24)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')

        updateCycleLabel(hardware, cycle, "DB1.3")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([11,12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
        waitAndStir(hardware, 24)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')

        updateCycleLabel(hardware, cycle, "DB1.4")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([5,6]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp4')
        waitAndStir(hardware, 24)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc4')

        updateCycleLabel(hardware, cycle, "DB1.5")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([7,8]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp5')
        waitAndStir(hardware, 24)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc5')

        updateCycleLabel(hardware, cycle, "DB1.6")
        dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([3,4]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp6')
        waitAndStir(hardware, 54)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc6')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def TwoEnz_FourElongTime(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix

        well1 = wellListFromColumns([1,5,9])
        well2 = wellListFromColumns([2,6,10])
        well3 = wellListFromColumns([3,7,11])
        well4 = wellListFromColumns([4,8,12])

        updateCycleLabel(hardware,cycle,"Premix1")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix1')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol],
                      [],
                      [],
                      inter([well1,nucleo_arrays[1]]),
                      inter([well1,nucleo_arrays[2]]),
                      inter([well1,nucleo_arrays[3]]),
                      inter([well1,nucleo_arrays[4]]),
                      [well for well in well1 if well % 2 == 1],
                      [well for well in well1 if well % 2 == 0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        updateCycleLabel(hardware, cycle, "Premix2")
        dispensePumps(hardware, [0, 0, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                      [],
                      [],
                      inter([well3, nucleo_arrays[1]]),
                      inter([well3, nucleo_arrays[2]]),
                      inter([well3, nucleo_arrays[3]]),
                      inter([well3, nucleo_arrays[4]]),
                      [well for well in well3 if well % 2 == 1],
                      [well for well in well3 if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        updateCycleLabel(hardware, cycle, "Premix3")
        dispensePumps(hardware, [0, 0, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                      [],
                      [],
                      inter([well4, nucleo_arrays[1]]),
                      inter([well4, nucleo_arrays[2]]),
                      inter([well4, nucleo_arrays[3]]),
                      inter([well4, nucleo_arrays[4]]),
                      [well for well in well4 if well % 2 == 1],
                      [well for well in well4 if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        updateCycleLabel(hardware, cycle, "Premix4")
        dispensePumps(hardware, [0, 0, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                      [],
                      [],
                      inter([well2, nucleo_arrays[1]]),
                      inter([well2, nucleo_arrays[2]]),
                      inter([well2, nucleo_arrays[3]]),
                      inter([well2, nucleo_arrays[4]]),
                      [well for well in well2 if well % 2 == 1],
                      [well for well in well2 if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp4')
        waitAndStir(hardware, 100)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc4')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac4')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoStepsWB2FourVol_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [40, 20, 50, 30, 40, 20, 50, 30,40, 20, 50, 30], 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        dispenseWashesColDiffVols(hardware, [40, 20, 50, 30, 40, 20, 50, 30,40, 20, 50, 30], 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc2')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_TwoDB_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware,[0,BBVolume2,0,0,0,0,0,0],[],usedWells,[],[],[],[],[],[],is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware,[0,BBVolume2,0,0,0,0,0,0],[],usedWells,[],[],[],[],[],[],is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_4onlyDB1Time_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        well5 = wellListFromColumns([1, 5, 9])
        well3 = wellListFromColumns([2, 6, 10])
        well2 = wellListFromColumns([3, 7, 11])
        well4 = wellListFromColumns([4, 8, 12])
        updateCycleLabel(hardware, cycle, "DB1.1")
        dispenseWashes(hardware, DBVolume1, 'DB', well2, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        waitAndStir(hardware, 25)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')
        updateCycleLabel(hardware, cycle, "DB1.2")
        dispenseWashes(hardware, DBVolume1, 'DB', well5, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, 25)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')
        updateCycleLabel(hardware, cycle, "DB1.3")
        dispenseWashes(hardware, DBVolume1, 'DB', well3, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
        waitAndStir(hardware, 25)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')
        updateCycleLabel(hardware, cycle, "DB1.4")
        dispenseWashes(hardware, DBVolume1, 'DB', well4, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp4')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc4')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoDB_HalfPlateLessVol_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashesColDiffVols(hardware,[BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2*0.6,BBVolume2*0.6,BBVolume2*0.6,BBVolume2*0.6,BBVolume2*0.6,BBVolume2*0.6],'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsDiffCols(hardware,[enz_vol,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol,enz_vol*0.6,enz_vol*0.6,enz_vol*0.6,enz_vol*0.6,enz_vol*0.6,enz_vol*0.6],[well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7],
                      nucleo_arrays[8], is384)


        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware,[BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1*0.6,BBVolume1*0.6,BBVolume1*0.6,BBVolume1*0.6,BBVolume1*0.6,BBVolume1*0.6],'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5]), is384)
        dispenseDoubleWashes_DB(hardware, DBVolume1*0.6, 'DB', wellListFromColumns([7,9,11]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5]), is384)
        dispenseDoubleWashes_DB(hardware, DBVolume2*0.6, 'DB', wellListFromColumns([7,9,11]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware,
                                  [BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2 * 0.6,
                                   BBVolume2 * 0.6, BBVolume2 * 0.6, BBVolume2 * 0.6, BBVolume2 * 0.6, BBVolume2 * 0.6],
                                  'Buff2', usedWells, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashesColDiffVols(hardware,[BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2, BBVolume2 * 0.6,
                               BBVolume2 * 0.6, BBVolume2 * 0.6, BBVolume2 * 0.6, BBVolume2 * 0.6, BBVolume2 * 0.6],
                              'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoDB_Xop(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, BBVolume2, BBVolume2],
                      [well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [well for well in endedWells if well % 2 == 1], [well for well in endedWells if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', inter([activeWells, wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', inter([activeWells, wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[], [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[], [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoDBpart_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, BBVolume2, BBVolume2],
                      [well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [well for well in endedWells if well % 2 == 1], [well for well in endedWells if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', inter([activeWells, wellListFromColumns([1,3,5,7,10])]), is384)
        dispenseWashes(hardware,DBVolume1, 'BB', inter([activeWells, wellListFromColumns([9,12])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', inter([activeWells, wellListFromColumns([1,3,5,7,10])]), is384)
        dispenseWashes(hardware,DBVolume2, 'BB', inter([activeWells, wellListFromColumns([9,12])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[], [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[], [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoDBpart_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, BBVolume2, BBVolume2],
                      [well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [well for well in endedWells if well % 2 == 1], [well for well in endedWells if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', inter([activeWells, wellListFromColumns([1,3,5,7,10])]), is384)
        dispenseWashes(hardware,DBVolume1, 'BB', inter([activeWells, wellListFromColumns([9,12])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', inter([activeWells, wellListFromColumns([1,3,5,7,10])]), is384)
        dispenseWashes(hardware,DBVolume2, 'BB', inter([activeWells, wellListFromColumns([9,12])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[], [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[], [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoDB_EBDBVol_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePumpsDiffCols(hardware, [25, 25, 50, 50, 25, 25, 50, 50,25, 25, 25, 25],
                      [well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7],
                      nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50, 0, 50, 0, 100,0,100,0, 100, 0, 50, 0] , 'DB',activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        dispenseWashesColDiffVols(hardware, [0, 50, 0, 50, 0, 100, 0,100,0,100, 0, 50] , 'BB',activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [30, 0, 30, 0, 60, 0, 60, 0, 30, 0, 60, 0], 'DB',activeWells,  is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp1')
        dispenseWashesColDiffVols(hardware, [0, 30, 0, 30, 0, 60, 0, 60, 0, 30, 0, 60], 'BB',activeWells,  is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp2')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoWB2_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, 50, 50],
                      [well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [well for well in endedWells if well % 2 == 1],
                      [well for well in endedWells if well % 2 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2],[],[],[],[],[],[],[well for well in endedWells if well % 2 == 1],[well for well in endedWells if well % 2 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def FourEnz_TwoWB2_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                      [well for well in activeWells if well % 4 == 1], [well for well in activeWells if well % 4 == 2],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_VolScreenPerStep(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashesColDiffVols(hardware, [50, 50, 50, 70, 50, 50, 50, 70, 50, 50, 50, 70], 'BB', usedWells,
                                      is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsDiffCols(hardware,[35,25,25,25,35,25,25,25,35,25,25,25], [well for well in activeWells], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [50,70,50,50,50,70,50,50,50,70,50,50], 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50,50,70,50,50,50,70,50,50,50,70,50],'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [30,30,42,30,30,30,42,30,30,30,42,30], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [50,50,50,70,50,50,50,70,50,50,50,70], 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashesColDiffVols(hardware, [50,50,50,70,50,50,50,70,50,50,50,70], 'BB', usedWells, is384)
    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PoolTest(hardware,is384):

    cycle=1

    while(1):
        updateCycleLabel(hardware, cycle, "")
        dispenseWashes(hardware,50,"DB",wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12]),0)
        waitAndStir(hardware,5)
        removeSupernatant(hardware,20)
        cycle+=1

def TwoEnz_TwoElongTime2m4m(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        well4min=[well for well in activeWells if well%2==1]
        well2min=[well for well in activeWells if well%2==0]

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0],
                      [well for well in well4min], [],
                      inter([well4min,nucleo_arrays[1]]),
                      inter([well4min,nucleo_arrays[2]]),
                      inter([well4min,nucleo_arrays[3]]),
                      inter([well4min,nucleo_arrays[4]]),
                      [],[],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0],
                      [well for well in well2min], [],
                      inter([well2min,nucleo_arrays[1]]),
                      inter([well2min,nucleo_arrays[2]]),
                      inter([well2min,nucleo_arrays[3]]),
                      inter([well2min,nucleo_arrays[4]]),
                      [],[],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def TwoElongTime_TwoWB2(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        welllonger=[well for well in activeWells if well%2==1]
        wellstd=[well for well in activeWells if well%2==0]

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,0],
                      [well for well in welllonger if well%4==1], [],
                      inter([welllonger,nucleo_arrays[1]]),
                      inter([welllonger,nucleo_arrays[2]]),
                      inter([welllonger,nucleo_arrays[3]]),
                      inter([welllonger,nucleo_arrays[4]]),
                      [well for well in welllonger if well%4==3],[],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 10)

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,0],
                      [well for well in wellstd if well%4==2], [],
                      inter([wellstd,nucleo_arrays[1]]),
                      inter([wellstd,nucleo_arrays[2]]),
                      inter([wellstd,nucleo_arrays[3]]),
                      inter([wellstd,nucleo_arrays[4]]),
                      [well for well in wellstd if well%4==0],[],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([2, 4, 6, 8, 10, 12]),is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, WB2Time)
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_FourDiffVolEnz(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsDiffCols(hardware, [enz_vol*1,enz_vol*1.4,enz_vol*1.2,enz_vol*1.6,enz_vol*1,enz_vol*1.4,enz_vol*1.2,enz_vol*1.6,enz_vol*1,enz_vol*1.4,enz_vol*1.2,enz_vol*1.6], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [50,70,60,80,50,70,60,80,50,70,60,80], 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50, 70, 60, 80, 50, 70, 60, 80, 50, 70, 60, 80], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [30,42,36,48,30,42,36,48,30,42,36,48], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [50, 70, 60, 80, 50, 70, 60, 80, 50, 70, 60, 80], 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_TwoDiffW1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 50], [], [], [], [], [], [], [], [], usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 50], [], [], [], [], [], [], [], [], usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoDiffEnz_TwoDiffW1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix

        wells_B5=wellListFromColumns([1,3,5,7,9,11])
        wells_B6=wellListFromColumns([2,4,6,8,10,12])

        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in wells_B5], [well for well in wells_B6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoWB2_FourDB(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_DB(hardware, BBVolume2, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix

        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[],[],is384)
        dispenseWashes(hardware, enz_vol, 'Buff2', usedWells, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispensePumps(hardware, [DBVolume1,DBVolume1,0,0,0,0,DBVolume1,DBVolume1], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], [], [], [], [],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispensePumps(hardware, [DBVolume2,DBVolume2,0,0,0,0,DBVolume2,DBVolume2], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], [], [], [], [],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_DB(hardware, BBVolume2, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseDoubleWashes_DB(hardware, BBVolume2, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def TwoEnz_IncubEmpty(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        wells_incubEmpty=wellListFromColumns([1,3,5,7,9,11])
        wells_incubStd=wellListFromColumns([2,4,6,8,10,12])
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in activeWells if well%2==1 and well in wells_incubEmpty],
                      [well for well in activeWells if well%2==0 and well in wells_incubEmpty],
                      inter([wells_incubEmpty,nucleo_arrays[1]]),
                      inter([wells_incubEmpty,nucleo_arrays[2]]),
                      inter([wells_incubEmpty,nucleo_arrays[3]]),
                      inter([wells_incubEmpty,nucleo_arrays[4]]),nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftfirstPremixDisp')
        waitAndStir(hardware, 30)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftfirstPremixInc')
        removeSupernatant(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftfirstPremixVac')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in activeWells if well % 2 == 1 and well in wells_incubStd],
                      [well for well in activeWells if well % 2 == 0 and well in wells_incubStd],
                      inter([wells_incubStd, nucleo_arrays[1]]),
                      inter([wells_incubStd, nucleo_arrays[2]]),
                      inter([wells_incubStd, nucleo_arrays[3]]),
                      inter([wells_incubStd, nucleo_arrays[4]]), nucleo_arrays[7], nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftfirstPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftfirstPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_10minsomeCycles(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    cycles_10min=[4,18,28]
    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10min:
            waitAndStir(hardware, 10*60)
        else:
            waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedFourEnz_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells= getActiveWellsButX(sequences,cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware, BBVolume2, 'Buff2', endedWells, is384)
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def FourEnz_TwoDB_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells= getActiveWellsButX(sequences,cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware,
                        [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol,BBVolume2],
                        [well for well in wellListFromColumns([1,2,3,4,5,6,7,8]) if well%4==1] + [well for well in wellListFromColumns([9,10])],
                        [well for well in wellListFromColumns([1,2,3,4,5,6,7,8]) if well%4==2] + [well for well in wellListFromColumns([11,12])],
                        nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],
                        [well for well in wellListFromColumns([1,2,3,4,5,6,7,8]) if well%4==3],
                        [well for well in wellListFromColumns([1,2,3,4,5,6,7,8]) if well%4==0],
                        endedWells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps_Q(hardware, [0,0,0,0,0,0,0,0,BBVolume2], [],[],[],[],[],[],[],[], usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps_Q(hardware, [0,0,0,0,0,0,0,0,BBVolume2], [],[],[],[],[],[],[],[], usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def FourEnz_DiffVol_W1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashesColDiffVols(hardware, [BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2,BBVolume2,BBVolume2],'BB',usedWells,is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashesColDiffVols(hardware,[BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2,BBVolume2,BBVolume2],'Buff2',endedWells,is384)
        dispensePumpsDiffCols(hardware, [enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware,[BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1,BBVolume1,BBVolume1],'Buff1',activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware,[DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1,DBVolume1,DBVolume1],'DB',activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware,[DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2,DBVolume2,DBVolume2],'DB',activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware,
                                  [BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.6,
                                   BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2, BBVolume2, BBVolume2], 'BB',
                                  activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashesColDiffVols(hardware,
                              [BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.6,
                               BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2, BBVolume2, BBVolume2], 'Buff2', usedWells,
                              is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashesColDiffVols(hardware,
                              [BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2 * 0.6,
                               BBVolume2, BBVolume2 * 0.6, BBVolume2, BBVolume2, BBVolume2, BBVolume2], 'Buff2', usedWells,
                              is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_FourDB_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[],[],is384)
        dispenseWashes(hardware, enz_vol, 'Buff2', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispensePumps(hardware, [DBVolume1,DBVolume1,0,0,0,0,DBVolume1,DBVolume1], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], [], [], [], [],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispensePumps(hardware, [DBVolume2, DBVolume2, 0, 0, 0, 0, DBVolume2, DBVolume2],
                      [well for well in activeWells if well % 4 == 1], [well for well in activeWells if well % 4 == 2],
                      [], [], [], [], [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_FourW1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[],[],is384)
        dispenseWashes(hardware, enz_vol, 'Buff2', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps(hardware, [BBVolume1, BBVolume1, 0, 0, 0, 0, BBVolume1, BBVolume1],
                      [well for well in activeWells if well % 4 == 1], [well for well in activeWells if well % 4 == 2],
                      [], [], [], [], [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoDB_TwoWB2(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps(hardware, [BBVolume2, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2],
                          [well for well in activeWells if well % 4 == 1],
                          [well for well in activeWells if well % 4 == 2], [], [],
                          [], [], [well for well in activeWells if well % 4 == 3],
                          [well for well in activeWells if well % 4 == 0], is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[],[],is384)
        dispenseWashes(hardware, enz_vol, 'Buff2', usedWells, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispensePumps(hardware, [BBVolume2, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2],
                      [well for well in activeWells if well % 4 == 1],
                      [well for well in activeWells if well % 4 == 2], [], [],
                      [], [], [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [BBVolume2, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2],
                  [well for well in activeWells if well % 4 == 1],
                  [well for well in activeWells if well % 4 == 2], [], [],
                  [], [], [well for well in activeWells if well % 4 == 3],
                  [well for well in activeWells if well % 4 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoDB_TwoWB1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0], [], [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[],[],is384)
        dispenseWashes(hardware, enz_vol, 'Buff2', usedWells, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps(hardware, [BBVolume1, BBVolume1, 0, 0, 0, 0, BBVolume1, BBVolume1],
                      [well for well in activeWells if well % 4 == 1],
                      [well for well in activeWells if well % 4 == 2], [], [],
                      [], [], [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff1', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def FourEnz_TwoElongTime2m4m(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        wells_2min=wellListFromColumns([1,3,5,7,9,11])
        wells_4min=wellListFromColumns([2,4,6,8,10,12])

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol],
                      [well for well in activeWells if well%4==1 and well in wells_4min],
                      [well for well in activeWells if well%4==2 and well in wells_4min],
                      inter([wells_4min,nucleo_arrays[1]]),
                      inter([wells_4min,nucleo_arrays[2]]),
                      inter([wells_4min,nucleo_arrays[3]]),
                      inter([wells_4min,nucleo_arrays[4]]),
                      [well for well in activeWells if well%4==3 and well in wells_4min],
                      [well for well in activeWells if well%4==0 and well in wells_4min],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 2*60)

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                      [well for well in activeWells if well % 4 == 1 and well in wells_2min],
                      [well for well in activeWells if well % 4 == 2 and well in wells_2min],
                      inter([wells_2min, nucleo_arrays[1]]),
                      inter([wells_2min, nucleo_arrays[2]]),
                      inter([wells_2min, nucleo_arrays[3]]),
                      inter([wells_2min, nucleo_arrays[4]]),
                      [well for well in activeWells if well % 4 == 3 and well in wells_2min],
                      [well for well in activeWells if well % 4 == 0 and well in wells_2min], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftSecondPremixDisp')
        waitAndStir(hardware, 2 * 60)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_W1_PKDifferentPercent(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    cycles_10min = []

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10min:
            waitAndStir(hardware, 10 * 60)
        else:
            waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps(hardware,[0,50,0,0,0,0,50,50], [],
                      [well for well in usedWells if well%8 in [1,4]],
                      [], [], [], [],
                      [well for well in usedWells if well%8 in [2,5,7]],
                      [well for well in usedWells if well%8 in [3,6,0]],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_4IncubTimeDB1_W1(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        well5 = wellListFromColumns([1,5,9])
        well3 = wellListFromColumns([2,6,10])
        well2 = wellListFromColumns([3,7,11])
        well4 = wellListFromColumns([4,8,12])
        updateCycleLabel(hardware, cycle, "DB1.1")
        dispensePumps(hardware,[0,0,0,0,0,0,50,100],[],[],[],[],[],[],[well for well in well3 if well%2==1],[well for well in well3 if well%2==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp1')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc1')
        updateCycleLabel(hardware, cycle, "DB1.2")
        dispensePumps(hardware,[0,0,0,0,0,0,50,100],[],[],[],[],[],[],[well for well in well4 if well%2==1],[well for well in well4 if well%2==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp2')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc2')
        updateCycleLabel(hardware, cycle, "DB1.3")
        dispensePumps(hardware,[0,0,0,0,0,0,50,100],[],[],[],[],[],[],[well for well in well2 if well%2==1],[well for well in well2 if well%2==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp3')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc3')
        updateCycleLabel(hardware, cycle, "DB1.4")
        dispensePumps(hardware,[0,0,0,0,0,0,50,100],[],[],[],[],[],[],[well for well in well5 if well%2==1],[well for well in well5 if well%2==0],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp4')
        waitAndStir(hardware, 58)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc4')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def RNAProcess(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    #WB1 dans Buff1
    #WB2 dans BB
    #Water dans Buff2
    #enzyme in MN
    #WashEDTA dans 0 (for finished wells)

    wash_vol=140
    wash_vol2=75
    wash_incub=30
    wash_nb=1

    water_vol=150
    water_incub=30
    water_nb=1

    elongation_vol=25
    elongation_incub=7*60

    DB_vol=50
    DB_incub=1*60

    vacuum=10

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)
        ended_wells = nucleo_arrays[0]
        ListM = [well for well in activeWells if well % 2 == 1]
        ListN = [well for well in activeWells if well % 2 == 0]


        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if cycle==1:
            removeSupernatant(hardware, vacuum)
            for i in range(2):
                dispenseWashes(hardware, wash_vol, 'BB', usedWells, is384)
                waitAndStir(hardware, wash_incub)
                removeSupernatant(hardware, vacuum)


        # Water 1
        updateCycleLabel(hardware, cycle, "Water1")
        dispenseWashes(hardware, water_vol, 'Buff2', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Disp')
        waitAndStir(hardware, water_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Inc')

        removeSupernatant(hardware, vacuum)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Vac')

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,elongation_vol,elongation_vol,elongation_vol,elongation_vol,elongation_vol,50],nucleo_arrays[5], nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],activeWells,ended_wells,is384)


        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, elongation_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, vacuum)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # Wash Buffer 1
        for nb in range(wash_nb):
            updateCycleLabel(hardware, cycle, "WB1" + str(nb+1))
            dispenseWashes(hardware, wash_vol, 'Buff1', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Disp')
            waitAndStir(hardware, wash_incub)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Inc')

            removeSupernatant(hardware, vacuum)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Vac')

        # Water 2
        updateCycleLabel(hardware, cycle, "Water2")
        dispenseWashes(hardware, water_vol, 'Buff2', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Disp')
        waitAndStir(hardware, water_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Inc')

        removeSupernatant(hardware, vacuum)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Vac')

        #DB
        updateCycleLabel(hardware, cycle, "DB")
        dispenseWashes(hardware, DB_vol, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBDisp')
        waitAndStir(hardware, DB_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBInc')

        removeSupernatant(hardware, vacuum)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBVac')

        # Wash Buffer 2
        for nb in range(wash_nb):
            updateCycleLabel(hardware, cycle, "WB2" + str(nb+1))
            dispenseWashes(hardware, wash_vol, 'BB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Disp')
            waitAndStir(hardware, wash_incub)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Inc')

            removeSupernatant(hardware, vacuum)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Vac')



        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, 150, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def PSPWashes(hardware, is384):

    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet(path)
    getParameters(synthesis_sheet)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    if is384:
        volToDisp=50
    else:
        volToDisp = 100

    #Water Washes
    for i in range(3):
        updateCycleLabel(hardware, i+1, " Water Wash")
        dispenseWashes(hardware,volToDisp,"DB",usedWells,is384)
        waitAndStir(hardware,30)
        removeSupernatant(hardware,VacuumTime+2)
    #TH1X Washes
    for i in range(3):
        updateCycleLabel(hardware, i+1, " TH1X Wash")
        dispenseWashes(hardware,volToDisp,"BB",usedWells,is384)
        waitAndStir(hardware,30)
        removeSupernatant(hardware,VacuumTime+2)

    updateCycleLabel(hardware, 0, "PSP Washes Done")

def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())

def ElongationCycle_TwoEnz_W1_OnlyOneDB(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_DiffFourW1_2stepsWB2_X(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWellsButX(sequences, cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware, BBVolume1, 'Buff2', endedWells, is384)
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],
                      nucleo_arrays[7], nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispensePumps_Q(hardware, [0, BBVolume1, 0, 0, 0, 0, BBVolume1, BBVolume1, BBVolume1], [],
                        [well for well in activeWells if well % 4 == 1], [], [], [], [],
                        [well for well in activeWells if well % 4 == 2],
                        [well for well in activeWells if well % 4 == 3],
                        [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        dispenseWashes(hardware, BBVolume2, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    dispenseWashes(hardware, BBVolume1, 'Buff2', usedWells, is384)


    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def FourEnz_TwoDiffWB1_EndedWellsCR0(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%4==1], [well for well in activeWells if well%4==2], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[well for well in activeWells if well%4==3],[well for well in activeWells if well%4==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware,BBVolume1,'Buff1',wellListFromColumns([9, 10, 11, 12]), is384)
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', wellListFromColumns([1, 3, 5, 7]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 50], [], [], [], [], [], [], [], [], usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps_Q(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 50], [], [], [], [], [], [], [], [], usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_W1_2DB(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],nucleo_arrays[10],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_DiffEnz_TwoWB2_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)
        wellsN=inter([activeWells,wellListFromColumns([9,10,11,12])])
        wellsM=inter([activeWells,wellListFromColumns([1,2,3,4,5,6,7,8])])

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, 50, 0],
                      wellsM, wellsN,
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], endedWells,
                      [], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,0],[],[],[],[],[],[],usedWells,[], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, 0], [], [], [], [], [], [], usedWells, [], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def OneEnz_EightNucs_W1_2WB2_W1X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_Q(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3],
                        nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], nucleo_arrays[10], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_FourdiffWB2_W1_2DB(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences, cycle)

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
                      [],
                      [well for well in activeWells if well % 4 == 1], [], [], [], [],
                      [well for well in activeWells if well % 4 == 2],
                      [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
            usedWells,
            [], nucleo_arrays[1], nucleo_arrays[2],
            nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
            [],
            [well for well in activeWells if well % 4 == 1], [], [], [], [],
            [well for well in activeWells if well % 4 == 2],
            [well for well in activeWells if well % 4 == 3],
            [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1


    dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
        [],
        [well for well in activeWells if well % 4 == 1], [], [], [], [],
        [well for well in activeWells if well % 4 == 2],
        [well for well in activeWells if well % 4 == 3],
        [well for well in activeWells if well % 4 == 0], is384)

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleSeparatedFourEnzQ_X(hardware, is384):
        title = easygui.enterbox("Name of the run ?")

        # Save Quartet Control File
        saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
        if saveQuartet:
            saveQuartetControlFile(title, inspect.getsource(inspect.currentframe()))

        thermalImages = 1
        if thermalImages:
            TT = hardware.parent.rightFrame.thermalThread
        else:
            TT = FakeThermalImageThread()

        # Set up recording file for thermal snapshots
        now = datetime.datetime.now()
        folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
            now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
            now.second) + "_" + title

        TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

        cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

        # dispTime = 0.12 * 2  # 0.10pour 20
        # dispDBTime = 0.06 * 2
        # dispBBTime = 0.06 * 2
        # Elong_time=4*60
        # DBTime=60
        # BBTime=30
        # VacuumTime=20

        while cycle != 0:

            updateCycleLabel(hardware, cycle, "")

            # We read the excel and get the parameters back
            synthesis_sheet = getExcelSheet(path)
            getParameters(synthesis_sheet)
            sequences = getSequences(synthesis_sheet)
            nucleo_arrays = splitSequences(sequences, cycle)
            activeWells = getActiveWellsButX(sequences, cycle)
            endedWells = getEndedWellsPlusX(sequences, cycle)

            # print(nucleo_arrays)
            enz_vol = EBVolume
            nuc_vol = NucsVolume

            if (cycle == 1):
                removeSupernatant(hardware, VacuumTime)

                dispenseWashes(hardware, BBVolume2, 'BB', activeWells, is384)

                waitAndStir(hardware, WB2Time)
                removeSupernatant(hardware, VacuumTime)

            # Premix
            updateCycleLabel(hardware, cycle, "Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

            dispenseWashes(hardware, BBVolume1, 'Buff2', endedWells, is384)
            dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, enz_vol, enz_vol],
                          [well for well in activeWells if well % 4 == 1],
                          [well for well in activeWells if well % 4 == 2], nucleo_arrays[1], nucleo_arrays[2],
                          nucleo_arrays[3], nucleo_arrays[4], [well for well in activeWells if well % 4 == 3],
                          [well for well in activeWells if well % 4 == 0], is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, Elong_time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

            # W1
            updateCycleLabel(hardware, cycle, "W1")
            dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
            waitAndStir(hardware, WB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

            # DB1
            updateCycleLabel(hardware, cycle, "DB1")
            dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            # DB2
            updateCycleLabel(hardware, cycle, "DB2")
            dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, DB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

            # Wash
            updateCycleLabel(hardware, cycle, "Wash")
            dispenseWashes(hardware, BBVolume2, 'BB', activeWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

            # We carry on with next cycle or we end the loop
            nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
            if len(nucleo_arrays_nextcycle[0]) == len(sequences):
                cycle = 0
            else:
                cycle += 1

        dispenseWashes(hardware, BBVolume2, 'BB', activeWells, is384)

        goToWell(hardware, 'thermalCamera', 1, 0)
        updateCycleLabel(hardware, cycle, "Synthesis End")
        hardware.arduinoControl.stopHeating()
        DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_FourdiffWB2_2stepsWB2_W1_X(hardware, is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT = FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    while cycle != 0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet = getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences = getSequences(synthesis_sheet)
        nucleo_arrays = splitSequences(sequences, cycle)
        usedWells = getUsedWells(sequences)
        activeWells = getActiveWellsButX(sequences, cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        # print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle == 1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
                      [],
                      [well for well in activeWells if well % 4 == 1], [], [], [], [],
                      [well for well in activeWells if well % 4 == 2],
                      [well for well in activeWells if well % 4 == 3],
                      [well for well in activeWells if well % 4 == 0], is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        # Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware, BBVolume1, 'Buff2', endedWells, is384)
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
        activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)


        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        # DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
            [],
            [well for well in activeWells if well % 4 == 1], [], [], [], [],
            [well for well in activeWells if well % 4 == 2],
            [well for well in activeWells if well % 4 == 3],
            [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        dispensePumps_Q(hardware, [0, BBVolume2, 0, 0, 0, 0, BBVolume2, BBVolume2, BBVolume2],
                        [],
                        [well for well in activeWells if well % 4 == 1], [], [], [], [],
                        [well for well in activeWells if well % 4 == 2],
                        [well for well in activeWells if well % 4 == 3],
                        [well for well in activeWells if well % 4 == 0], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')
        # We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
        if len(nucleo_arrays_nextcycle[0]) == len(sequences):
            cycle = 0
        else:
            cycle += 1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)
    TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW2Disp')

    goToWell(hardware, 'thermalCamera', 1, 0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_OneEnz_W1_2WB2_ON(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([usedWells,wellListFromColumns([1,3,5,7,9,11])]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware,[enz_vol, 50, nuc_vol, nuc_vol, nuc_vol, nuc_vol, 50, 0], activeWells, inter([endedWells,wellListFromColumns([1, 2, 5, 6, 7, 8, 9, 10, 11, 12])]), nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],inter([endedWells,wellListFromColumns([3, 4])]), [], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        if cycle in list(range(300,336+1)):
            dispenseWashes(hardware, BBVolume2, 'Buff2',wellListFromColumns([8]),is384)
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', inter([usedWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware,  [0, 50, 0, 0, 0, 0, 0, 0], [], usedWells, [], [], [], [], [], [], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_TwoDiffW1_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells = getActiveWellsButX(sequences, cycle)
        endedWells = getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [0,0,0,0,0,0,50,0], [], [], [], [], [], [],endedWells, [],is384)
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', inter([activeWells,wellListFromColumns([1,3,5,7,9,11])]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0,0,0,0,0,0,50,0], [], [], [], [], [], [],usedWells, [],is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_4diffWB_end(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7], nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 5, 9]), is384)
    dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([2, 6, 10]), is384)
    dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([3, 7, 11]), is384)
    dispensePumps(hardware, [0,0,0,0,0,0,50,0], [], [], [], [], [], [], wellListFromColumns([4, 8, 12]), [],is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycleTwoEnz_W1_DiffVols_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume



        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware,BBVolume2,'Buff2',endedWells,is384)
        dispensePumpsDiffCols(hardware, [enz_vol,enz_vol*0.4,enz_vol*0.4,enz_vol*0.7,enz_vol*0.5,enz_vol*0.6,enz_vol*0.5,enz_vol*0.5,enz_vol,enz_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [], [],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [BBVolume1,BBVolume1*0.4,BBVolume1*0.4,BBVolume1*0.7,BBVolume1*0.5,BBVolume1*0.6,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1], 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')


        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [DBVolume1,DBVolume1*0.4,DBVolume1*0.4,DBVolume1*0.7,DBVolume1*0.5,DBVolume1*0.6,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1], 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [DBVolume2,DBVolume2*0.4,DBVolume2*0.4,DBVolume2*0.7,DBVolume2*0.5,DBVolume2*0.6,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2], 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [BBVolume2,BBVolume2*0.4,BBVolume2*0.4,BBVolume2*0.7,BBVolume2*0.5,BBVolume2*0.6,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2], 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def ElongationCycleTwoEnz_W1_DiffVols_pause50cycles_X(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20

    wait(hardware, 60 * 60 * 7 + 15 * 60
         )
    hardware.arduinoControl.startHeating()
    wait(hardware, 1800)
    multiDispensePumps(hardware, [200, 200, 200, 200, 200, 200, 0, 0, 400, 400, 400, 400])

    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWellsButX(sequences,cycle)
        endedWells=getEndedWellsPlusX(sequences, cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume



        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware,BBVolume2,'Buff2',endedWells,is384)
        dispensePumpsDiffCols(hardware, [enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6,enz_vol,enz_vol*0.6], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [], [],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6,BBVolume1,BBVolume1*0.6], 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')
        if cycle==50:
            input("Centrifuge please")
        if cycle==100:
            input("Centrifuge please")
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')


        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6,DBVolume1,DBVolume1*0.6], 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6,DBVolume2,DBVolume2*0.6], 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6,BBVolume2,BBVolume2*0.6], 'BB', activeWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')
        if cycle==50:
            input("Centrifuge please")
        if cycle==100:
            input("Centrifuge please")
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def TwoElongTime_Col_TwoWB2(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))


    while cycle!=0:

        updateCycleLabel(hardware, cycle, "")

        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)

        unevenCol = wellListFromColumns([1, 2, 5, 6, 9, 10])
        evenCol = wellListFromColumns([3, 4, 7, 8, 11, 12])

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, 0, 0],
                      inter([unevenCol, [well for well in activeWells if well%2==1]]), inter([unevenCol, [well for well in activeWells if well%2==0]]),
                      inter([unevenCol, nucleo_arrays[1]]),
                      inter([unevenCol, nucleo_arrays[2]]),
                      inter([unevenCol, nucleo_arrays[3]]),
                      inter([unevenCol, nucleo_arrays[4]]),
                      [], [], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 0)

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,0,0],
                      inter([evenCol, [well for well in activeWells if well%2==1]]), inter([evenCol, [well for well in activeWells if well%2==0]]),
                      inter([evenCol, nucleo_arrays[1]]),
                      inter([evenCol, nucleo_arrays[2]]),
                      inter([evenCol, nucleo_arrays[3]]),
                      inter([evenCol, nucleo_arrays[4]]),
                      [],[], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]),is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, 0], [], [], [], [], [], [], usedWells, [], is384 )

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

if __name__ == "__main__":
    wells=[1,2,4,7,9,16,18,16,10]

