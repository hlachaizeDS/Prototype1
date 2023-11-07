from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits


def ElongationCycleSeparatedOneEnz(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def ElongationCycleOneEnz_W1(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def ElongationCycleOneEnz_TwoDB_W1(hardware,is384):
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

            dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def ElongationCycleOneEnz_W1_10minSomeCycles(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    cycles_10_min=[1]
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

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        if cycle in cycles_10_min:
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


def ElongationCycleSeparatedTwoEnz(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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
        waitAndStir(hardware, WB1Time)
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

def ElongationCycleTwoEnz_W1_DBActiveOnly(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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


def ElongationCycleTwoEnz_W1(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def ElongationCycleTwoEnz_W1_LongB6_Tblsht(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1 and well in wellListFromColumns([4,5,6,7])], [well for well in activeWells if well%2==0 or well in wellListFromColumns([8,9,10])], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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


def ElongationCycleTwoEnz_DiffVolWB2_W1(hardware,is384):
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

            dispenseWashesColDiffVols(hardware,[40,20,50,30,40,20,50,30,40,20,50,30],'BB',usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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
        dispenseWashesColDiffVols(hardware, [40, 20, 50, 30, 40, 20, 50, 30, 40, 20, 50, 30], 'BB', usedWells, is384)

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

    dispenseWashesColDiffVols(hardware, [40, 20, 50, 30, 40, 20, 50, 30, 40, 20, 50, 30], 'BB', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def ElongationCycleTwoEnz_EndedWells_W1(hardware,is384):
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

        if (cycle>52):
            dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([10, 11, 12]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixEndedDisp')
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
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
        if cycle>52:
            dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([10, 11, 12]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1EndedDisp')
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        if cycle>52:
            dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([10, 11, 12]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2EndedDisp')
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

def ElongationCycle_TwoEnz_4IncEBTime_W1(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in well1 if well % 2 == 1],
                      [well for well in well1 if well % 2 == 0],
                      inter([well1,nucleo_arrays[1]]),
                      inter([well1,nucleo_arrays[2]]),
                      inter([well1,nucleo_arrays[3]]),
                      inter([well1,nucleo_arrays[4]]),is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        updateCycleLabel(hardware, cycle, "Premix2")
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in well3 if well % 2 == 1],
                      [well for well in well3 if well % 2 == 0],
                      inter([well3, nucleo_arrays[1]]),
                      inter([well3, nucleo_arrays[2]]),
                      inter([well3, nucleo_arrays[3]]),
                      inter([well3, nucleo_arrays[4]]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')

        updateCycleLabel(hardware, cycle, "Premix3")
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in well4 if well % 2 == 1],
                      [well for well in well4 if well % 2 == 0],
                      inter([well4, nucleo_arrays[1]]),
                      inter([well4, nucleo_arrays[2]]),
                      inter([well4, nucleo_arrays[3]]),
                      inter([well4, nucleo_arrays[4]]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc3')

        updateCycleLabel(hardware, cycle, "Premix4")
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in well2 if well % 2 == 1],
                      [well for well in well2 if well % 2 == 0],
                      inter([well2, nucleo_arrays[1]]),
                      inter([well2, nucleo_arrays[2]]),
                      inter([well2, nucleo_arrays[3]]),
                      inter([well2, nucleo_arrays[4]]), is384)

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

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoElongTime_TwoWB2_W1(hardware,is384):
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

        welllonger=[well for well in activeWells if well%2==0]
        wellstd=[well for well in activeWells if well%2==1]

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in welllonger], [],
                      inter([welllonger,nucleo_arrays[1]]),
                      inter([welllonger,nucleo_arrays[2]]),
                      inter([welllonger,nucleo_arrays[3]]),
                      inter([welllonger,nucleo_arrays[4]]),is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 10)

        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in wellstd], [],
                      inter([wellstd,nucleo_arrays[1]]),
                      inter([wellstd,nucleo_arrays[2]]),
                      inter([wellstd,nucleo_arrays[3]]),
                      inter([wellstd,nucleo_arrays[4]]),is384)

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
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1,3,5,7,9,11]),is384)
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

def ElongationCycleTwoEnz_W1_2WB2(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

        # Wash2
        updateCycleLabel(hardware, cycle, "Wash")
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


def ElongationCycleTwoEnz_W1_MerckMocks(hardware,is384):
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

        nucswells=wellListFromHalfColumns([1,2,5,6,7,8,9,10,13,14,15,16,17,18,21,22,23,24])
        enzwells=wellListFromHalfColumns([1,2,3,5,6,7,9,10,13,14,16,17,18,20,21,22,23,24])
        DBwells=wellListFromHalfColumns([1,2,3,4,5,6,8,9,10,13,14,15,17,18,19,20,21,22,23,24])

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in activeWells if well%2==1 and well in enzwells],
                      [well for well in activeWells if well%2==0 and well in enzwells],
                      inter([nucleo_arrays[1],nucswells]),
                      inter([nucleo_arrays[2],nucswells]),
                      inter([nucleo_arrays[3],nucswells]),
                      inter([nucleo_arrays[4],nucswells]),is384)

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
        dispenseWashes(hardware, DBVolume1, 'DB', DBwells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', DBwells, is384)
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


def ElongationCycleTwoEnz_W1_DiffVols(hardware,is384):
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

        dispensePumpsColDiffVols(hardware, [50,50,50,50,50,50,50,50,50,50,50,50], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [100,50,100,50,100,50,100,50,100,50,100,50], 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [100,100,100,100,100,100,100,100,100,100,100,100], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [60,30,60,30,60,30,60,30,60,30,60,30], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [100,50,100,50,100,50,100,50,100,50,100,50], 'BB', usedWells,is384)
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


def ElongationCycleTwoEnz_W1_ExtraFinalW2(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

    finalwash=0
    while finalwash<10:
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1,3,5,7,9,11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExBBDisp')
        waitAndStir(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExBBInc')
        removeSupernatant(hardware, VacuumTime)
        finalwash=finalwash+1

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def ElongationCycleTwoEnz_W1_DBforactive(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def ElongationCycleTwoEnz_W1_DBandElongTime(hardware,is384):
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
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in activeWells if well%2==1 and well in wells_4min],
                      [well for well in activeWells if well%2==0 and well in wells_4min],
                      inter([wells_4min,nucleo_arrays[1]]),
                      inter([wells_4min,nucleo_arrays[2]]),
                      inter([wells_4min,nucleo_arrays[3]]),
                      inter([wells_4min,nucleo_arrays[4]]),is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, 2*60)

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in activeWells if well % 2 == 1 and well in wells_2min],
                      [well for well in activeWells if well % 2 == 0 and well in wells_2min],
                      inter([wells_2min, nucleo_arrays[1]]),
                      inter([wells_2min, nucleo_arrays[2]]),
                      inter([wells_2min, nucleo_arrays[3]]),
                      inter([wells_2min, nucleo_arrays[4]]), is384)

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
        wells_DB_30s=wellListFromColumns([1,2,5,6,9,10])
        wells_DB_5s=wellListFromColumns([3,4,7,8,11,12])
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', wells_DB_30s, is384)
        waitAndStir(hardware,25)
        dispenseWashes(hardware, DBVolume1, 'DB', wells_DB_5s, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', wells_DB_30s, is384) #changed it afterwards
        waitAndStir(hardware, 25)
        dispenseWashes(hardware, DBVolume2, 'DB', wells_DB_5s, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

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


def ElongationCycleTwoEnz_W1_PK_hightemp_gly(hardware,is384):
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

        wells2min=wellListFromColumns([1,3,5,7,9,11])
        wells4min=wellListFromColumns([2,4,6,8,10,12])
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in activeWells if well%2==1 and well in wells4min],
                      [well for well in activeWells if well%2==0 and well in wells4min],
                      inter([wells4min,nucleo_arrays[1]]),
                      inter([wells4min,nucleo_arrays[2]]),
                      inter([wells4min,nucleo_arrays[3]]),
                      inter([wells4min,nucleo_arrays[4]]), is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftFirstPremixDisp')
        waitAndStir(hardware, 2*60)

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in activeWells if well % 2 == 1 and well in wells2min],
                      [well for well in activeWells if well % 2 == 0 and well in wells2min],
                      inter([wells2min, nucleo_arrays[1]]),
                      inter([wells2min, nucleo_arrays[2]]),
                      inter([wells2min, nucleo_arrays[3]]),
                      inter([wells2min, nucleo_arrays[4]]), is384)

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


def ElongationCycleTwoEnz_W1_Degenerate(hardware,is384):
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
        nucleo_arrays=splitSequencesDegenerate(sequences,cycle)
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

        dispenseAllDegenerate(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [[well,1] for well in activeWells if well%2==1], [[well,1] for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def PoolTest(hardware,is384):

    cycle=1
    while(1):
        updateCycleLabel(hardware, cycle, "")
        cycle+=1
        dispenseWashes(hardware,50,"DB",wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12]),0)
        waitAndStir(hardware,5)
        removeSupernatant(hardware,20)

def RNAProcess(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    WASH_NB_BEFORE_SYNTHESIS=2
    wash_vol=150
    wash_incub=30

    water_vol=150
    water_incub=30

    elongation_vol=25
    elongation_incub=420

    DB_vol=50
    DB_incub=600

    vacuum_time=10

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
        ended_wells = nucleo_arrays[0]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if cycle==1:
            removeSupernatant(hardware, vacuum_time)
            for wash in range(WASH_NB_BEFORE_SYNTHESIS):
                dispenseWashes(hardware, wash_vol, 'BB',usedWells, is384)
                waitAndStir(hardware, wash_incub)
                removeSupernatant(hardware, vacuum_time)

        # Wash Buffer 1
        updateCycleLabel(hardware, cycle, "WB1")
        dispenseWashes(hardware, wash_vol, 'BB',usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Disp')
        waitAndStir(hardware, wash_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Inc')

        removeSupernatant(hardware, vacuum_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Vac')

        # Water 1
        updateCycleLabel(hardware, cycle, "Water1")
        dispenseWashes(hardware, water_vol, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Disp')
        waitAndStir(hardware, water_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Inc')

        removeSupernatant(hardware, vacuum_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Vac')

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [elongation_vol]*6,
                      [well for well in activeWells if well not in nucleo_arrays[6]], nucleo_arrays[6],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, elongation_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, vacuum_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # Wash Buffer 2
        updateCycleLabel(hardware, cycle, "WB2")
        dispenseWashes(hardware, wash_vol, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Disp')
        waitAndStir(hardware, wash_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Inc')

        removeSupernatant(hardware, vacuum_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Vac')

        # Water 2
        updateCycleLabel(hardware, cycle, "Water2")
        dispenseWashes(hardware, water_vol, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Disp')
        waitAndStir(hardware, water_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Inc')

        removeSupernatant(hardware, vacuum_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Vac')

        #DB
        updateCycleLabel(hardware, cycle, "DB")
        dispenseWashes(hardware, DB_vol, 'DB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBDisp')
        waitAndStir(hardware, DB_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBInc')

        removeSupernatant(hardware, vacuum_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBVac')

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


def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())


if __name__ == "__main__":
    wells=[1,2,4,7,9,16,18,16,10]


