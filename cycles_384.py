from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits

def Testing_384(hardware,is384):


    # We read the excel and get the parameters back
    synthesis_sheet=getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences_384=getSequences_384(synthesis_sheet)
    nucleo_arrays=splitSequences(sequences_384,1)
    print(nucleo_arrays)
    usedWells=getUsedWells(sequences_384)
    activeWells=getActiveWells(sequences_384,1)

    #print(nucleo_arrays)
    enz_vol = EBVolume
    nuc_vol = NucsVolume
    #dispensePumps_384(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%4 in [1,2] ], [well for well in activeWells if well%4 in [3,0]], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8])
    dispenseWashes_384(hardware, DBVolume1, 'DB', usedWells)

def ElongationCycle_TwoEnz_W1_384(hardware):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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
        synthesis_sheet=getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences=getSequences_384(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_384(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%4 in [1,2]], [well for well in activeWells if well%4 in [3,0]], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8])

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes_384(hardware, BBVolume1, 'Buff1', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes_384(hardware, DBVolume1, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes_384(hardware, DBVolume2, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)
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

    dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_384_2and3minElong(hardware):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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
        synthesis_sheet=getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences=getSequences_384(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        wells_2min=wellListFromColumns_384([1,2,5,6,9,10,13,14,17,18,21,22])
        wells_3min=wellListFromColumns_384([3,4,7,8,11,12,15,16,19,20,23,24])
        dispensePumps_384(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in inter([activeWells,wells_3min]) if well%4 in [1,2]], [well for well in inter([activeWells,wells_3min]) if well%4 in [3,0]], inter([wells_3min,nucleo_arrays[1]]), inter([wells_3min,nucleo_arrays[2]]), inter([wells_3min,nucleo_arrays[3]]), inter([wells_3min,nucleo_arrays[4]]),nucleo_arrays[7],nucleo_arrays[8])
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftFirstPremixDisp')
        waitAndStir(hardware, 1*60)
        dispensePumps_384(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                          [well for well in inter([activeWells, wells_2min]) if well % 4 in [1, 2]],
                          [well for well in inter([activeWells, wells_2min]) if well % 4 in [3, 0]],
                          inter([wells_2min, nucleo_arrays[1]]), inter([wells_2min, nucleo_arrays[2]]),
                          inter([wells_2min, nucleo_arrays[3]]), inter([wells_2min, nucleo_arrays[4]]),
                          nucleo_arrays[7], nucleo_arrays[8])
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 2*60)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes_384(hardware, BBVolume1, 'Buff1', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes_384(hardware, DBVolume1, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes_384(hardware, DBVolume2, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)
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

    dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_384_LowDensityLowScale(hardware):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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
        synthesis_sheet=getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences=getSequences_384(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_DiffColVol_384(hardware, [12.5,12.5,6.25,6.25,12.5,12.5,6.25,6.25,12.5,12.5,6.25,6.25,12.5,12.5,6.25,6.25,12.5,12.5,6.25,6.25,12.5,12.5,6.25,6.25], [well for well in activeWells if well%4 in [1,2]], [well for well in activeWells if well%4 in [3,0]], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8])

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes_DiffColVol_384(hardware, [25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5], 'Buff1', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes_DiffColVol_384(hardware, [25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5], 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes_DiffColVol_384(hardware, [15,15,7.5,7.5,15,15,7.5,7.5,15,15,7.5,7.5,15,15,7.5,7.5,15,15,7.5,7.5,15,15,7.5,7.5], 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes_DiffColVol_384(hardware, [25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5], 'BB', usedWells)
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

    dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_384_Buff2attheEnd(hardware):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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
        synthesis_sheet=getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences=getSequences_384(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_384(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%4 in [1,2]], [well for well in activeWells if well%4 in [3,0]], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8])

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes_384(hardware, BBVolume1, 'Buff1', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes_384(hardware, DBVolume1, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes_384(hardware, DBVolume2, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)
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

    multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,0,0,0,2000])
    dispenseWashes_384(hardware, BBVolume2, 'Buff2', usedWells)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes_384(hardware, BBVolume2, 'Buff2', usedWells)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_384_WB2forSubs(hardware):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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
        synthesis_sheet=getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences=getSequences_384(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes_384(hardware, BBVolume2, 'BB', usedWells)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps_384(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%4 in [1,2]], [well for well in activeWells if well%4 in [3,0]], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8])

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes_384(hardware, BBVolume1, 'Buff1', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes_384(hardware, DBVolume1, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes_384(hardware, DBVolume2, 'DB', usedWells)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        CR50wells = wellListFromColumns_384([1,2,9,10,17,18])
        dispenseWashesDouble_384(hardware, BBVolume2, 'BB','Buff2', CR50wells)
        CR15wells=wellListFromColumns_384([3,4,11,12,19,20])
        CR30wells=wellListFromColumns_384([7,8,15,16,23,24])
        dispensePumps_384(hardware,[0,0,0,0,0,0,25,25],[],[],[],[],[],[],CR15wells,CR30wells,max_vol=12.5)
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


    CR50wells = wellListFromColumns_384([1, 2, 9, 10, 17, 18])
    dispenseWashesDouble_384(hardware, 25, 'BB', 'Buff2', CR50wells)
    CR15wells = wellListFromColumns_384([3, 4, 11, 12, 19, 20])
    CR30wells = wellListFromColumns_384([7, 8, 15, 16, 23, 24])
    dispensePumps_384(hardware, [0, 0, 0, 0, 0, 0, 25, 25], [], [], [], [], [], [], CR15wells, CR30wells,max_vol=12.5)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())

if __name__ == "__main__":
    wells=[1,2,4,7,9,16,18,16,10]