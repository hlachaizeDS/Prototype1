from elementaryFunctions import *
from excelRead import *
import datetime
import easygui

proteinase=0
dispDBTime = 0.12
dispBBTime = 0.105
dispBuff1Time=0.155
dispBuff2Time=0.13
dispWater50=0.16


from quartetControlSave import saveQuartetControlFile,force2digits

def ElongationCycle(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    thermalImages=1
    if thermalImages:
        TT=hardware.parent.rightFrame.thermalThread

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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

        updateCycleLabel(hardware,cycle,"")


        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)

        if (cycle==1):
            updateCycleLabel(hardware, cycle, "First Wash")
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)


        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePremixes(hardware, dispTime, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        for wellM in nucleo_arrays[5]:
            goToWell(hardware,"M",wellM,0)
            dispense(hardware,"M",dispM)
        for wellN in nucleo_arrays[6]:
            goToWell(hardware,"N",wellN,0)
            dispense(hardware,"N",dispN)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        if (proteinase==1):
            if (cycle%25==0):
                print('Proteinase')
                dispenseWashes(hardware, dispBuff1Time, 'Buff1', usedWells, is384)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDProtDisp')
                waitAndStir(hardware, 60)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtInc')

                removeSupernatant(hardware, VacuumTime)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftProtVac')

        #DB1
        updateCycleLabel(hardware,cycle,"DB1")
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages,folder_path, cycle, 'AftBBVac')

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


def ElongationCycleSeparatedOneEnz(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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

        updateCycleLabel(hardware,cycle,"")


        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)

        if (cycle==1):
            updateCycleLabel(hardware, cycle, "First Wash")
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)


        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePremixesAndEnzyme(hardware, dispTime25_nuc, dispTime25_enzyme,activeWells,nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        #DB1
        updateCycleLabel(hardware,cycle,"DB1")
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
    updateCycleLabel(hardware, cycle, "Synthesis end")

    hardware.arduinoControl.stopHeating()

def FJCodonMap(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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

        updateCycleLabel(hardware,cycle,"")


        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)

        if (cycle==1):
            updateCycleLabel(hardware, cycle, "First Wash")
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)


        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePremixesAndEnzyme(hardware, dispTime25_nuc, dispTime25_enzyme,activeWells,nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        #DB1
        updateCycleLabel(hardware,cycle,"DB1")
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
    updateCycleLabel(hardware, cycle, "Synthesis end")

    hardware.arduinoControl.stopHeating()


def FJTaqman(hardware,is384):
    waterWells=[1,9,17,25,33,41,49,57,65,73,81,89]

    title = easygui.enterbox("Name of the run ?")

    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

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

        updateCycleLabel(hardware,cycle,"")


        # We read the excel and get the parameters back
        synthesis_sheet=getExcelSheet(path)
        getParameters(synthesis_sheet)
        sequences=getSequences(synthesis_sheet)
        nucleo_arrays=splitSequences(sequences,cycle)
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)

        #print(nucleo_arrays)

        if (cycle==1):
            updateCycleLabel(hardware, cycle, "First Wash")
            removeSupernatant(hardware, VacuumTime)

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)
            dispenseWashes(hardware, dispWater50, 'Buff1', waterWells, 0)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)

        if cycle!=1 :
            #Premix
            updateCycleLabel(hardware,cycle,"Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
            dispensePremixesAndEnzyme(hardware, dispTime25_nuc, dispTime25_enzyme,activeWells,[], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
            dispenseWashes(hardware,dispWater50,'Buff1',waterWells,0)
        else:
            input("Press Enter to continue...")
            dispenseWashes(hardware, dispWater50, 'Buff1', waterWells, 0)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        #DB1
        updateCycleLabel(hardware,cycle,"DB1")
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        dispenseWashes(hardware, dispWater50, 'Buff1', waterWells, 0)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        dispenseWashes(hardware, dispWater50, 'Buff1', waterWells, 0)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)
        dispenseWashes(hardware, dispWater50, 'Buff1', waterWells, 0)
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
    updateCycleLabel(hardware, cycle, "Synthesis end")

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

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePremixesAndEnzyme(hardware, dispTime25_nuc, dispTime25_enzyme,[well for well in activeWells if well%2==1],[well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        #dispensePremixesAndEnzymeSep(hardware, dispTime25_nuc, dispTime25_enzyme_M,dispTime25_enzyme_N,[well for well in activeWells if well%2==1],[well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)

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

def ElongationCycleSeparatedTwoEnz_384Test(hardware,is384):
    wellnumberThreshold=25

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

            dispenseWashes(hardware, dispBBTime, 'BB', upperThreshold(usedWells,wellnumberThreshold), is384)
            dispenseWashes(hardware, dispBBTime/2, 'BB', underThreshold(usedWells,wellnumberThreshold), is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')
        dispensePremixesAndEnzyme(hardware, dispTime25_nuc, dispTime25_enzyme,upperThreshold([well for well in activeWells if well%2==1],wellnumberThreshold),upperThreshold([well for well in activeWells if well%2==0],wellnumberThreshold), upperThreshold(nucleo_arrays[1],wellnumberThreshold), upperThreshold(nucleo_arrays[2],wellnumberThreshold), upperThreshold(nucleo_arrays[3],wellnumberThreshold), upperThreshold(nucleo_arrays[4],wellnumberThreshold),is384)
        dispensePremixesAndEnzyme(hardware, dispTime25_nuc/2, dispTime25_enzyme/2,underThreshold([well for well in activeWells if well%2==1],wellnumberThreshold),underThreshold([well for well in activeWells if well%2==0],wellnumberThreshold), underThreshold(nucleo_arrays[1],wellnumberThreshold), underThreshold(nucleo_arrays[2],wellnumberThreshold), underThreshold(nucleo_arrays[3],wellnumberThreshold), underThreshold(nucleo_arrays[4],wellnumberThreshold),is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')



        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, dispDBTime, 'DB', upperThreshold(usedWells,wellnumberThreshold), is384)
        dispenseWashes(hardware, dispDBTime/2, 'DB', underThreshold(usedWells,wellnumberThreshold), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, dispDBTime, 'DB', upperThreshold(usedWells,wellnumberThreshold), is384)
        dispenseWashes(hardware, dispDBTime/2, 'DB', underThreshold(usedWells,wellnumberThreshold), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, dispBBTime, 'BB', upperThreshold(usedWells,wellnumberThreshold),is384)
        dispenseWashes(hardware, dispBBTime/2, 'BB', underThreshold(usedWells,wellnumberThreshold),is384)
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

def ElongationAether(hardware,is384):
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
        [ended_wells,A_wells,C_wells,G_wells,T_wells]=splitSequencesAether(sequences,cycle)
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
        dispenseAllAether(hardware, dispTime25_enzyme, [[well, 1] for well in activeWells if well % 2 == 1], [[well, 1] for well in activeWells if well % 2 == 0], A_wells, C_wells, G_wells, T_wells, 0)
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


def ElongationCycleOldTC(hardware,is384):
    title = easygui.enterbox("Name of the run ?")


    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title)

    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_" + title
    TC = hardware.thermalCamera
    TC.snapshot_in_cycle(folder_path, 1, 'BeforeAnything')

    cycle = int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        print(cycle)


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

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)


        #Start of the cycle
        print('Premix')
        TC.snapshot_in_cycle(folder_path, cycle, 'BefPremix')
        dispensePremixes(hardware, dispTime, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        for wellM in nucleo_arrays[5]:
            goToWell(hardware,"M",wellM,0)
            dispense(hardware,"M",dispM)
        for wellN in nucleo_arrays[6]:
            goToWell(hardware,"N",wellN,0)
            dispense(hardware,"N",dispN)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftPremixVac')

        if (proteinase==1):
            if (cycle%5==0):
                print('Proteinase')
                dispenseWashes(hardware, dispBuff1Time, 'Buff1', usedWells, is384)
                TC.snapshot_in_cycle(folder_path, cycle, 'AftDProtDisp')
                waitAndStir(hardware, 120)
                TC.snapshot_in_cycle(folder_path, cycle, 'AftProtInc')

                removeSupernatant(hardware, VacuumTime)
                TC.snapshot_in_cycle(folder_path, cycle, 'AftProtVac')

        print('DB1')
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB1Vac')

        print('DB2')
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB2Vac')

        print('Wash')
        dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)

    hardware.arduinoControl.stopHeating()


def ElongationCycleDiffVolumes(hardware,is384):

    title = easygui.enterbox("Name of the run ?")

    #Save Quartet Control File
    saveQuartetControlFile(title)

    #Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path=str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(now.second) + "_" + title
    TC = hardware.thermalCamera
    TC.snapshot_in_cycle(folder_path, 1, 'BeforeAnything')

    cycle= int(easygui.enterbox("What cycle do you wanna start at ?"))

    #dispTime = 0.12 * 2  # 0.10pour 20
    #dispDBTime = 0.06 * 2
    #dispBBTime = 0.06 * 2
    #Elong_time=4*60
    #DBTime=60
    #BBTime=30
    #VacuumTime=20


    while cycle!=0:

        print(cycle)


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

            dispenseWashes(hardware, dispBBTime, 'BB', usedWells, is384)
            dispenseWashes(hardware, dispBBTime/2, 'BB', [x + 8 for x in usedWells], is384)

            waitAndStir(hardware, BBTime)
            removeSupernatant(hardware, VacuumTime)


        #Start of the cycle
        print('Premix')
        TC.snapshot_in_cycle(folder_path, cycle, 'BefPremix')
        dispensePremixes(hardware, dispTime, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],is384)
        dispensePremixes(hardware, dispTime/2, [x + 8 for x in nucleo_arrays[1]],  [x + 8 for x in nucleo_arrays[2]],  [x + 8 for x in nucleo_arrays[3]],  [x + 8 for x in nucleo_arrays[4]],is384)
        for wellM in nucleo_arrays[5]:
            goToWell(hardware,"M",wellM,0)
            dispense(hardware,"M",dispM)
        for wellN in nucleo_arrays[6]:
            goToWell(hardware,"N",wellN,0)
            dispense(hardware,"N",dispN)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftPremixVac')

        if (proteinase==1):
            if (cycle%5==0):
                print('Proteinase')
                dispenseWashes(hardware, dispBuff1Time, 'Buff1', usedWells, is384)
                TC.snapshot_in_cycle(folder_path, cycle, 'AftDProtDisp')
                waitAndStir(hardware, 120)
                TC.snapshot_in_cycle(folder_path, cycle, 'AftProtInc')

                removeSupernatant(hardware, VacuumTime)
                TC.snapshot_in_cycle(folder_path, cycle, 'AftProtVac')

        print('DB1')
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        dispenseWashes(hardware, dispDBTime/2, 'DB', [x + 8 for x in usedWells], is384)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DBTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB1Vac')

        print('DB2')
        dispenseWashes(hardware, dispDBTime, 'DB', usedWells, is384)
        dispenseWashes(hardware, dispDBTime/2, 'DB', [x + 8 for x in usedWells], is384)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DBTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftDB2Vac')

        print('Wash')
        dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)
        dispenseWashes(hardware, dispBBTime/2, 'BB', [x + 8 for x in usedWells],is384)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, BBTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftBBInc')

        removeSupernatant(hardware, VacuumTime)
        TC.snapshot_in_cycle(folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, dispBBTime, 'BB', usedWells,is384)
    dispenseWashes(hardware, dispBBTime/2, 'BB', [x + 8 for x in usedWells],is384)

    goToWell(hardware, 'thermalCamera', 1,0)

    hardware.arduinoControl.stopHeating()


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
            disp=[0,0,0,0,0,0] #Flag to know if we should dispense
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
                    #multiDispense(hardware, disp, time)
                    # 0.22 for 48uL
                    # 0.48 for 96uL
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)


def dispenseAllAether(hardware,time_enz,M_array,N_array,A_array,C_array,G_array,T_array,is384):

    vol_times=[0.23,0.115,0.076,0.058]

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
                for wellVol in nuclArrays[nucl]:
                    if plateWellToRealWell6Nozzles(wells[nucl])==wellVol[0]:
                        disp[nucl]=wellVol[1]
                        nuclArrays[nucl].remove(wellVol)
            if (1 in disp) or (2 in disp) or (3 in disp) or (4 in disp):
                if is384:
                    for i in range(1,5):
                        goToRealWell6Nozzles(hardware,m_well,i)
                        multiDispenseAether(hardware, disp, time_enz, vol_times[disp[2]-1], vol_times[disp[3]-1], vol_times[disp[4]-1], vol_times[disp[5]-1])
                else:
                    goToRealWell6Nozzles(hardware, m_well, 0)
                    multiDispenseAether(hardware, disp, time_enz, vol_times[disp[2]-1], vol_times[disp[3]-1], vol_times[disp[4]-1], vol_times[disp[5]-1])
                    #multiDispense(hardware, disp, time)
                    # 0.22 for 48uL
                    # 0.48 for 96uL
            hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def dispenseWashes(hardware,time,solution,array,is384):

    washArray=array.copy()

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
                        dispense(hardware, solution, time)
                else:
                    goToWell(hardware, solution, min(smallest_well, col * 8 + 5), 0)
                    dispense(hardware, solution, time)
            else:
                if is384:
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 1, i)
                        dispense(hardware, solution, time)
                    for i in range(1,5):
                        goToWell(hardware, solution, col * 8 + 5, i)
                        dispense(hardware, solution, time)
                else:
                    goToWell(hardware,solution,col*8+1,0)
                    dispense(hardware,solution,time)
                    goToWell(hardware, solution, col * 8 + 5,0)
                    dispense(hardware, solution, time)
        hardware.parent.update()

    goToWell(hardware, "thermalCamera", 1, 0)

def removeSupernatant(hardware,vacuumTime):

    goToWell(hardware, 'thermalCamera', 1,0)

    hardware.vacValveOpen()

    wait(hardware, vacuumTime)
    hardware.vacValveClose()

    wait(hardware, 3)

    #hardware.set_output(7,1)
    #wait(hardware,10)
    #hardware.set_output(7, 0)
    #hardware.vacuum.ventOff()





def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())

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


if __name__ == "__main__":
    wells=[1,2,4,7,9,16,18,16,10]
    print(underThreshold(wells,10))
    print(upperThreshold(wells,10))

