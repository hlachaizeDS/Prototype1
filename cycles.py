from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits

proteinase=0
dispDBTime = 0.11
dispBBTime = 0.09
dispBuff1Time=0.155
dispBuff2Time=0.13
dispWater50=0.16

enz_vol=25
nuc_vol=25




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

            waitAndStir(hardware, BBTime)
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
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedOneEnz_ProtK(hardware,is384):

    protK_every=30

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

            waitAndStir(hardware, BBTime)
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

        #Eventually ProtK
        if (cycle%protK_every==0 and cycle!=120):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 3*60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            updateCycleLabel(hardware, cycle, "ProtKWash")
            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashDisp')
            waitAndStir(hardware, BBTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

            waitAndStir(hardware, BBTime)
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
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedFourEnz(hardware,is384):
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

            waitAndStir(hardware, BBTime)
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
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedFourEnz_W1_ProtK(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wells_buff1=wellListFromColumns([2,4,6,8,10,12])
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

            waitAndStir(hardware, BBTime)
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

        #Wash1

        updateCycleLabel(hardware, cycle, "W1")
        dispenseDoubleWashes_Buff1(hardware, 50, 'Buff1', wells_buff1, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, 30)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedFourEnz_ProtK(hardware,is384):
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

            waitAndStir(hardware, BBTime)
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

        #Wash1

        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, 50, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, 30)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedTwoEnz_LowDensity(hardware,is384):
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

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')


        dispensePumpsDiffCols(hardware, [25,40,25,40,25,40,25,40,25,40,25,40], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50,80,50,80,50,80,50,80,50,80,50,80], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycle_Sep_Co_DMSO(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wells_buff2=wellListFromColumns([2,4,6,8,10,12])

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

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], nucleo_arrays[5], nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
        dispenseDoubleWashes_Buff2(hardware, 25, 'Buff2', wells_buff2, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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


def ElongationCycle_P5_valid(hardware,is384):
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

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], [well for well in nucleo_arrays[1] if well%2==1], [well for well in nucleo_arrays[2] if well%2==1], nucleo_arrays[3], nucleo_arrays[4],[well for well in nucleo_arrays[1] if well%2==0],[well for well in nucleo_arrays[2] if well%2==0],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #hardware.initialisation()
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


def ElongationCycleSeparatedTwoEnz_ProtK(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    protK_every=15

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

            waitAndStir(hardware, BBTime)
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

        # Eventually ProtK
        if (cycle % protK_every == 0):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 3 * 60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            updateCycleLabel(hardware, cycle, "ProtKWash")
            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashDisp')
            waitAndStir(hardware, BBTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedTwoEnz_ProtKScreen(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wells_every_5=wellListFromColumns([1,2,7,8])
    wells_every_15=wellListFromColumns([3,4,9,10])
    wells_every_30=wellListFromColumns([5,6,11,12])

    wells_with_wash=wellListFromColumns([1,3,5,7,9,11])
    wells_no_wash=wellListFromColumns([2,4,6,8,10,12])

    wells_30s=wellListFromHalfColumns([1,3,5,7,9,11,13,15,17,19,21,23])
    wells_3min=wellListFromHalfColumns([2,4,6,8,10,12,14,16,18,20,22,24])

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

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in activeWells if well % 2 == 1], [well for well in activeWells if well % 2 == 0],
                      nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7],
                      nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # Eventually ProtK
        if (cycle % 30 == 0):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1', inter([wells_3min,union([wells_every_5,wells_every_15,wells_every_30])]), is384)
            waitAndStir(hardware, 150)
            dispenseWashes(hardware, 50, 'Buff1', inter([wells_30s,union([wells_every_5,wells_every_15,wells_every_30])]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 30)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        elif (cycle % 15 == 0):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1',
                           inter([wells_3min, union([wells_every_5, wells_every_15])]), is384)
            dispenseWashes(hardware, 50, 'BB',
                           union([wells_every_30]), is384)
            waitAndStir(hardware, 150)
            dispenseWashes(hardware, 50, 'Buff1',
                           inter([wells_30s, union([wells_every_5, wells_every_15])]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 30)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        elif (cycle % 5 == 0):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1',
                           inter([wells_3min, union([wells_every_5])]), is384)
            dispenseWashes(hardware, 50, 'BB',
                           union([wells_every_30, wells_every_15]), is384)
            waitAndStir(hardware, 150)
            dispenseWashes(hardware, 50, 'Buff1',
                           inter([wells_30s, union([wells_every_5])]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 30)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        if (cycle % 5 == 0):
            updateCycleLabel(hardware, cycle, "ProtKWash")
            dispenseWashes(hardware, BBVolume2, 'BB', wells_with_wash, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashDisp')
            waitAndStir(hardware, BBTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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


def ElongationCycleSeparatedTwoEnz_forDifferentSizes(hardware,is384):
    #Wash during EB and all steps for finished oligos
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
        ended_wells = nucleo_arrays[0]

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        dispenseWashes(hardware,50,"BB",ended_wells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        dispenseWashes(hardware, 50, "BB", ended_wells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        dispenseWashes(hardware, 50, "BB", ended_wells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycleSeparatedTwoEnz_forDifferentSizes_PK(hardware,is384):
    #Wash during EB and all steps for finished oligos
    title = easygui.enterbox("Name of the run ?")

    protK_every=15

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

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        dispenseWashes(hardware,50,"BB",ended_wells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # Eventually ProtK
        if (cycle % protK_every == 0):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 3 * 60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            updateCycleLabel(hardware, cycle, "ProtKWash")
            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashDisp')
            waitAndStir(hardware, BBTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        dispenseWashes(hardware, 50, "BB", ended_wells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        dispenseWashes(hardware, 50, "BB", ended_wells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycle_IncCo_EDTA(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wells_std=wellListFromColumns([1,3,5,7,9,11])
    wells_CoEDTA=wellListFromColumns([2,4,6,8,10,12])

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

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], wells_std, wells_CoEDTA, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, 25, 'Buff1', wells_CoEDTA, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycle_Capping_First_Cycle(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wells_first_half=wellListFromColumns([1,2,3,4,5,6])
    wells_second_half=wellListFromColumns([7,8,9,10,11,12])

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
            updateCycleLabel(hardware, cycle, "Wash1")
            dispenseWashes(hardware, 100, 'Buff1', usedWells, is384)
            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)
            updateCycleLabel(hardware, cycle, "Wash2")
            dispenseWashes(hardware, 100, 'Buff1', usedWells, is384)
            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)
            updateCycleLabel(hardware, cycle, "Wash3")
            dispenseWashes(hardware, 100, 'Buff1', usedWells, is384)
            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)
            updateCycleLabel(hardware, cycle, "end")
            input("allez")




        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], inter([wells_first_half,[well for well in activeWells if well%2==1]]), inter([wells_first_half,[well for well in activeWells if well%2==0]]), inter([wells_first_half,nucleo_arrays[1]]), inter([wells_first_half,nucleo_arrays[2]]), inter([wells_first_half,nucleo_arrays[3]]), inter([wells_first_half,nucleo_arrays[4]]),nucleo_arrays[7],nucleo_arrays[8],is384)
        waitAndStir(hardware, 20)
        dispenseWashes(hardware,20,"Buff1",wells_first_half,is384)
        waitAndStir(hardware, 30)

        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      inter([wells_second_half, [well for well in activeWells if well % 2 == 1]]),
                      inter([wells_second_half, [well for well in activeWells if well % 2 == 0]]),
                      inter([wells_second_half, nucleo_arrays[1]]), inter([wells_second_half, nucleo_arrays[2]]),
                      inter([wells_second_half, nucleo_arrays[3]]), inter([wells_second_half, nucleo_arrays[4]]),
                      nucleo_arrays[7], nucleo_arrays[8], is384)
        waitAndStir(hardware, 20)
        dispenseWashes(hardware, 20, "Buff1", wells_second_half, is384)
        waitAndStir(hardware, 30)

        removeSupernatant(hardware, VacuumTime)

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        input()

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


def ElongationCycleSeparatedTwoEnz_DoubleEB(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wells_W2=wellListFromColumns([1,3,5,7,9,11])
    wells_ProtK=wellListFromColumns([2,4,6,8,10,12])

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

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsDiffCols(hardware,[12.5,12.5,25,25,12.5,12.5,25,25,12.5,12.5,25,25],[well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftFirstPremixDisp')
        waitAndStir(hardware, 120)
        removeSupernatant(hardware, VacuumTime)

        dispenseDoubleWashes_Buff1(hardware,50,"Buff1",wells_ProtK,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWashDispBtwnEBs')
        waitAndStir(hardware, 30)
        removeSupernatant(hardware, VacuumTime)

        dispensePumpsDiffCols(hardware, [12.5, 12.5, 25, 25, 12.5, 12.5, 25, 25, 12.5, 12.5, 25, 25],
                              [well for well in activeWells if well % 2 == 1],
                              [well for well in activeWells if well % 2 == 0], nucleo_arrays[1], nucleo_arrays[2],
                              nucleo_arrays[3], nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftSecondPremixDisp')
        waitAndStir(hardware, 120)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftSecondPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, 25, 'Buff2', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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


def RNAProcess(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    wellsStdEBandDB=wellListFromColumns([1,2,3,4,5,6,7,8,10,11,12])
    wellsDoubleEBandDB=wellListFromColumns([9])

    wellsPAP500=wellListFromHalfColumns([7,8,16,17,18])
    wellsPAP150=wellListFromHalfColumns([9,10,11,12,13,14,15])

    wash_vol=150
    wash_incub=30

    water_vol=150
    water_incub=30

    elongation_vol=25
    elongation_incub=420

    DB_vol=50
    DB_incub=600

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
            removeSupernatant(hardware, VacuumTime)

        # Wash Buffer 1
        updateCycleLabel(hardware, cycle, "WB1")
        dispenseWashes(hardware, wash_vol, 'BB',usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Disp')
        waitAndStir(hardware, wash_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB1Vac')

        # Water 1
        updateCycleLabel(hardware, cycle, "Water1")
        dispenseWashes(hardware, water_vol, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Disp')
        waitAndStir(hardware, water_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater1Vac')

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [elongation_vol,elongation_vol,elongation_vol,elongation_vol,elongation_vol,elongation_vol], [well for well in activeWells if well in wellsPAP500 and well in wellsStdEBandDB], [well for well in activeWells if well in wellsPAP150 and well in wellsStdEBandDB], [well for well in nucleo_arrays[1] if well in wellsStdEBandDB], [well for well in nucleo_arrays[2] if well in wellsStdEBandDB], [well for well in nucleo_arrays[3] if well in wellsStdEBandDB], [well for well in nucleo_arrays[4] if well in wellsStdEBandDB],is384)
        dispensePumps(hardware, [elongation_vol*2,elongation_vol*2,elongation_vol*2,elongation_vol*2,elongation_vol*2,elongation_vol*2], [well for well in activeWells if well in wellsPAP500 and well in wellsDoubleEBandDB], [well for well in activeWells if well in wellsPAP150 and well in wellsDoubleEBandDB], [well for well in nucleo_arrays[1] if well in wellsDoubleEBandDB], [well for well in nucleo_arrays[2] if well in wellsDoubleEBandDB], [well for well in nucleo_arrays[3] if well in wellsDoubleEBandDB], [well for well in nucleo_arrays[4] if well in wellsDoubleEBandDB],is384)
        dispenseWashes(hardware,50,'BB',ended_wells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, elongation_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # Wash Buffer 2
        updateCycleLabel(hardware, cycle, "WB2")
        dispenseWashes(hardware, wash_vol, 'BB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Disp')
        waitAndStir(hardware, wash_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWB2Vac')

        # Water 2
        updateCycleLabel(hardware, cycle, "Water2")
        dispenseWashes(hardware, water_vol, 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Disp')
        waitAndStir(hardware, water_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWater2Vac')

        #DB
        updateCycleLabel(hardware, cycle, "DB")
        dispenseWashes(hardware, DB_vol, 'DB', [well for well in activeWells if well in wellsStdEBandDB], is384)
        dispenseWashes(hardware, DB_vol*2, 'DB', [well for well in activeWells if well in wellsDoubleEBandDB], is384)
        dispenseWashes(hardware, 50, 'BB', ended_wells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBDisp')
        waitAndStir(hardware, DB_incub)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDBInc')

        removeSupernatant(hardware, VacuumTime)
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


def ElongationCycle_SpecialLong(hardware,is384):
    #only washes if wells are finished
    #protK

    protK_every=15
    WashOnlyEB=wellListFromHalfColumns([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    WashAllSteps=wellListFromHalfColumns([])

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
        ended_wells = nucleo_arrays[0]
        usedWells=getUsedWells(sequences)
        active_wells=getActiveWells(sequences,cycle)
        activeWellsButX=getActiveWellsButX(sequences,cycle)
        endedWellsPlusX=getEndedWellsPlusX(sequences,cycle)

        #print(nucleo_arrays)
        enz_vol = EBVolume
        nuc_vol = NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWellsButX if well%2==1], [well for well in activeWellsButX if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        dispenseWashes(hardware,50,"BB",ended_wells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        #Eventually ProtK
        if (cycle % protK_every == 0 and cycle != 200):
            updateCycleLabel(hardware, cycle, "ProtK")
            dispenseWashes(hardware, 50, 'Buff1', active_wells, is384)

            dispenseWashes(hardware, 50, 'BB', ended_wells,
                               is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKDisp')
            waitAndStir(hardware, 3 * 60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

            updateCycleLabel(hardware, cycle, "ProtKWash")
            dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashDisp')
            waitAndStir(hardware, BBTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtKWashVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', active_wells, is384)
        dispenseWashes(hardware, BBVolume2, 'BB', list(set(ended_wells) & set(WashAllSteps)), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', active_wells, is384)
        dispenseWashes(hardware, BBVolume2, 'BB', list(set(ended_wells) & set(WashAllSteps)), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', active_wells, is384)
        dispenseWashes(hardware, BBVolume2, 'BB', list(set(ended_wells) & set(WashAllSteps)), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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



def ElongationDegenerate(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread

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
        [ended_wells,A_wells,C_wells,G_wells,T_wells]=splitSequencesDegenerate(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispenseAllDegenerate(hardware,[enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],[[well, 1] for well in activeWells if well % 2 == 1],[[well, 1] for well in activeWells if well % 2 == 0], A_wells, C_wells, G_wells, T_wells, is384)
        #The 1 next to enzyme wells is only to make it like the nucs
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()

def ElongationCycleTwoEnz_ColsDiffVol(hardware,volsPerCol,is384):
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

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispenseWashesColDiffVols(hardware, volsPerCol, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsColDiffVols(hardware, [vol/2 for vol in volsPerCol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, volsPerCol, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, volsPerCol, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, volsPerCol, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
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

def ElongationCycle_HS_25ulWashes(hardware,is384):

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

            waitAndStir(hardware, BBTime)
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

        #First Water Wash
        updateCycleLabel(hardware, cycle, "Water1")
        dispenseWashes(hardware, 25, 'BB', usedWells, is384)


        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWaterDisp')
        waitAndStir(hardware, 5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWaterInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWaterVac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB',usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')


        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, 50, 'BB',usedWells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        # Second Water Wash
        # updateCycleLabel(hardware, cycle, "Water2")
        # dispenseWashes(hardware, 25, 'BB', wellListFromColumns([2, 4, 6, 8, 10, 12]), is384)
        # dispenseWashes(hardware, 25, 'Buff1', wellListFromColumns([3, 7, 11]), is384)
        # TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWaterDisp')
        # waitAndStir(hardware, 5)
        # TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWaterInc')
        #
        # removeSupernatant(hardware, VacuumTime)
        # TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftWaterVac')

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


def stirrerTest(hardware,is384):


    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + "Shaker_Zeroposition_Test"

    counter=1
    while 1:
        print(str(counter)+" cycles")
        sleep(2)
        waitAndStir(hardware, 1)
        sleep(1)
        TT.snapshot_in_cycle(thermalImages, folder_path, 1, 'cycle'+ str(counter))
        counter+=1




def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())



if __name__ == "__main__":
    wells=[1,2,4,7,9,16,18,16,10]


