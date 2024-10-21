from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits
import inspect

def Synthesis_TwoEnz(hardware,is384):

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

        multi_dispense_in_wells(hardware, {uneven_enzyme: [EBVolume, [well for well in activeWells if well % 2 == 1]],
                                           even_enzyme: [EBVolume, [well for well in activeWells if well % 2 == 0]],
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
        multi_dispense_in_wells(hardware, {Wash1: [BBVolume1, usedWells]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {DB: [DBVolume1, usedWells]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {DB: [DBVolume2, usedWells]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {Wash2: [BBVolume2, usedWells]}, is384)
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

    multi_dispense_in_wells(hardware, {Wash2: [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_X(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                           "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]],
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

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FourWB1_ExtraPkWash_X(hardware,is384):

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
            multi_dispense_in_wells(hardware, {"N": [BBVolume1, [well for well in activeWellsButX if well % 4 == 2]+[well for well in activeWellsButX if well % 4 == 3]+[well for well in activeWellsButX if well % 4 == 0]],
                                               "Q": [BBVolume1, [well for well in activeWellsButX if well % 4 == 1]]
                                               }, is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftpKDisp')
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftpKInc')

            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftpKVac')

        multi_dispense_in_wells(hardware, {"N": [BBVolume1, [well for well in activeWellsButX if well % 4 == 1] + [well for well in activeWellsButX if well % 4 == 2]],
                                           "O": [BBVolume1, [well for well in activeWellsButX if well % 4 == 3]],
                                           "P": [BBVolume1, [well for well in activeWellsButX if well % 4 == 0]]
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

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, X_wells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, X_wells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xp(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "P": [BBVolume2, X_wells],
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

    multi_dispense_in_wells(hardware, {"P": [BBVolume2, X_wells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"P": [BBVolume2, X_wells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xp_AVPrimingO(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if (cycle==10):
            multi_dispense(hardware,{"O": 1000})

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [NucsVolume, O_wells],
                                           "P": [BBVolume2, X_wells],
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

    multi_dispense_in_wells(hardware, {"P": [BBVolume2, usedWells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"P": [BBVolume2, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def Synthesis_TwoEnz_TwoWB1_ExtraWB1_X(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"BB":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "Q": [BBVolume2, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        if cycle % 50 == 0:
            multi_dispense_in_wells(hardware, {
                "Buff1": [BBVolume1, wellListFromColumns([1,3,5,7])],
                "Buff2": [BBVolume1, wellListFromColumns([2,4,6,8])],
                "O": [BBVolume1, [well for well in wellListFromColumns([9, 10, 11, 12]) if well % 2 == 1]],
                "P": [BBVolume1, [well for well in wellListFromColumns([9, 10, 11, 12]) if well % 2 == 0]],
            }, is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraW1Disp')
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraW1Inc')
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftExtraW1Vac')

        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX, wellListFromColumns([1,3,5,6,7,8,9,10,11,12])])],
                                           "Buff2": [BBVolume1, inter([activeWellsButX, wellListFromColumns([2,4])])]}, is384)
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

    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, X_wells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, X_wells]}, is384)

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

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                           "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]],
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

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def PDR_Synthesis_TwoEnz_TwoDB_X(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                           "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]],
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

    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"O": [BBVolume2, [well for well in X_wells if well % 2 == 1]],
                                        "P": [BBVolume2, [well for well in X_wells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoDB_TwoWB2x2_LastWB2_X(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"O": [BBVolume2,[well for well in usedWells if well % 2 ==1]],
                                              "P": [BBVolume2,[well for well in usedWells if well % 2 ==0]]},is384)

            waitAndStir(hardware, WB2Time*2)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
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
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,8,9,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([1,2,3,4,5,6,7,8,9,11])])],
                                           "BB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"O": [BBVolume2,[well for well in activeWellsButX if well % 2 ==1]],
                                              "P": [BBVolume2,[well for well in activeWellsButX if well % 2 ==0]]},is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        multi_dispense_in_wells(hardware, {"O": [BBVolume2,[well for well in activeWellsButX if well % 2 ==1]],
                                              "P": [BBVolume2,[well for well in activeWellsButX if well % 2 ==0]]},is384)
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

    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, [well for well in wellListFromColumns([4,8,9,10,11,12])]],
                                        "O": [BBVolume2, [well for well in wellListFromColumns([1,5])]],
                                        "P": [BBVolume2, [well for well in wellListFromColumns([2,6])]],
                                        "Q": [BBVolume2, [well for well in wellListFromColumns([3,7])]]}, is384)
    waitAndStir(hardware, WB2Time*2)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Buff2": [BBVolume2, [well for well in wellListFromColumns([4,8,9,10,11,12])]],
                                        "O": [BBVolume2, [well for well in wellListFromColumns([1,5])]],
                                        "P": [BBVolume2, [well for well in wellListFromColumns([2,6])]],
                                        "Q": [BBVolume2, [well for well in wellListFromColumns([3,7])]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_FourIncWB1_X(hardware,is384):

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

            multi_dispense_in_wells(hardware,{"Buff2":[BBVolume2,usedWells]},is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 2 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 2 == 0]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [NucsVolume, O_wells],
                                           "P": [NucsVolume, P_wells],
                                           "Q": [BBVolume2, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"O": [BBVolume1, [well for well in activeWellsButX if well % 2 ==1]],
                                           "P": [BBVolume1, [well for well in activeWellsButX if well % 2 ==0]]}, is384)
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX,wellListFromColumns([11,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp1')
        waitAndStir(hardware, 115)
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX,wellListFromColumns([3,4,9,10])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp2')
        waitAndStir(hardware, 25)
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX,wellListFromColumns([7,8])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp3')
        waitAndStir(hardware, 65)
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, inter([activeWellsButX,wellListFromColumns([1,2,5,6])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp4')
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

    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, X_wells]}, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    multi_dispense_in_wells(hardware, {"Q": [BBVolume2, X_wells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

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



def ElongationCycle_OneEnz_W1_X(hardware,is384):
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
        enz_vol=EBVolume
        nuc_vol=NucsVolume

        if (cycle==1):
            removeSupernatant(hardware, VacuumTime)

            dispensePumps(hardware, [0,BBVolume2,0,0,0,0,0,0],[], usedWells,[],[],[],[],[],[],is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumps(hardware, [enz_vol,BBVolume2,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, endedWells, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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

    dispensePumps(hardware, [0,BBVolume2,0,0,0,0,0,0],[], usedWells,[],[],[],[],[],[],is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0,BBVolume2,0,0,0,0,0,0],[], usedWells,[],[],[],[],[],[],is384)


    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_OneEnz_W1_10minsomeCycles(hardware,is384):

    cycles_10min = [1]

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




def ElongationTwoEnz_HighScale_10minSomeCycles(hardware,is384):

    cycles_10min=[]

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

        # W1 (=BB)
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

        #Wash (=BB)
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
        dispenseWashes(hardware, BBVolume2, 'Buff2', endedWells,is384)
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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
    waitAndStir(hardware, WB1Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

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
        dispenseWashes(hardware, BBVolume2, 'Buff2', endedWells,is384)
        dispensePumps(hardware, [enz_vol,0,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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
    waitAndStir(hardware, WB1Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_TwoWB2(hardware,is384):
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

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_384_WB2Screen(hardware,is384):
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
        dispensePumps(hardware, [0, 0, 0,0,0,0 , BBVolume2, BBVolume2],
                      [], [], [], [], [], [],
                      [well for well in wellListFromHalfColumns([3,7,11,15,19,23]) if well%2==1],[well for well in wellListFromHalfColumns([3,7,11,15,19,23]) if well%2==0],
                      is384,max_vol=12.5)

        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromHalfColumns([1,5,9,13,17,21]),is384)
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromHalfColumns([2,6,10,14,18,22]),is384)
        dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, BBVolume2],
                      [], [], [], [], [], [],
                      [well for well in wellListFromHalfColumns([4,8,12,16,20,24]) if well % 2 == 1],
                      [well for well in wellListFromHalfColumns([4,8,12,16,20,24]) if well % 2 == 0],
                      is384,max_vol=12.5)
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


def ElongationCycle_TwoEnz_W1_Buff2atTheEnd(hardware,is384):
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

    multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000])
    for i in range(2):
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        waitAndStir(hardware, 20)
        removeSupernatant(hardware, VacuumTime)

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_Buff2atTheEnd_DiffVol(hardware,is384):
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
        activeWellsButX=getActiveWellsButX(sequences,cycle)
        X_wells=nucleo_arrays[9]

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

        dispensePumpsDiffCols(hardware, [25,25,25,25,12.5,12.5,15,15,25,25,25,25], [well for well in activeWellsButX if well%2==1], [well for well in activeWellsButX if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
        dispenseWashes(hardware,50,"Buff2",X_wells,is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [50,50,50,50,25,25,30,30,50,50,50,50], 'Buff1', activeWellsButX, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50,50,50,50,25,25,30,30,50,50,50,50], 'DB', activeWellsButX, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [50,50,50,50,25,25,30,30,50,50,50,50], 'DB', activeWellsButX, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [50,50,50,50,25,25,30,30,50,50,50,50], 'BB', activeWellsButX,is384)
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

    multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000])
    for i in range(2):
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        waitAndStir(hardware, 20)
        removeSupernatant(hardware, VacuumTime)

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)



def ElongationCycle_TwoEnz_W1_TR102030(hardware,is384):
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

        dispensePumps(hardware, [enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWells, [], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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
        O_wells=[well for well in wellListFromColumns([1,3,5,7,9,11]) if well % 2 ==1]
        P_wells=[well for well in wellListFromColumns([1,3,5,7,9,11]) if well % 2 ==0]
        dispensePumps(hardware, [0, 50, 0, 0, 0, 0, 50, 50],
                      [],wellListFromHalfColumns([3,7,11,15,19,23]),
                      [], [], [], [], O_wells,P_wells, is384)
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromHalfColumns([4,8,12,16,20,24]),is384)
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

    multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000])
    for i in range(2):
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([3,4,7,8,11,12]),is384)
        dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0],
                      [], [],
                      [], [], [], [], wellListFromColumns([1,2,5,6,9,10]), [], is384)
        waitAndStir(hardware, 20)
        removeSupernatant(hardware, VacuumTime)

    dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([3, 4, 7, 8, 11, 12]), is384)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0],
                  [], [],
                  [], [], [], [], wellListFromColumns([1, 2, 5, 6, 9, 10]), [], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_long_diffVolumes(hardware,is384):
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

        dispensePumpsDiffCols(hardware, [0,0,25,25,50,25,25,50,0,25,0,0], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
        dispenseWashes(hardware,50,"Buff2",wellListFromColumns([9,11]),is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume1, 'Buff1', wellListFromColumns([3,4,5,6,7,8]), is384)
        dispensePumps(hardware,[0,0,0,0,0,0,50,0],[],[],[],[],[],[],wellListFromColumns([10]),[],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [0,0,50,100,50,50,50,100,0,50,0,0], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [0,0,30,60,30,30,30,60,0,30,0,0], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([3,4,5,6,8,9,10,11]),is384)
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([7]),is384)
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


def ElongationCycle_TwoEnz_W1_long_mutants_dI(hardware,is384):
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
        ended_wells=nucleo_arrays[0]
        X_wells=nucleo_arrays[9]
        usedWells=getUsedWells(sequences)
        activeWells=getActiveWells(sequences,cycle)
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

        wells_M96=wellListFromColumns([3])
        wells_M147=wellListFromColumns([4,6,7,8,9,10])
        wells_M170=wellListFromColumns([5])

        if cycle in [53,107,161]:
            multiDispensePumps(hardware,[0,0,0,0,0,0,0,200])
        dispenseWashes(hardware, 50, 'Buff2', union([ended_wells,X_wells]), is384)
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,50], inter([activeWellsButX,wells_M147]), inter([activeWellsButX,wells_M96]), nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],inter([activeWellsButX,wells_M170]),nucleo_arrays[8],is384)

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

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_ReprimeNucs_Oended(hardware,is384):
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
        ended_wells=nucleo_arrays[0]

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

        if cycle==158:
            multiDispensePumps(hardware, [0, 0, 0,0,0,0,1000])

        multiDispensePumps(hardware,[0,0,25,25,25,25])
        dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0], [], [], [], [], [], [], ended_wells, [], is384)
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

    dispensePumps(hardware,[0,0,0,0,0,0,50,0],[],[],[],[],[],[],usedWells,[],is384)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0], [], [], [], [], [], [], usedWells, [], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_AceticAcidCapping(hardware,is384):
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

        dispensePumps(hardware, [0,0,enz_vol,enz_vol,nuc_vol,nuc_vol,0,0], [], [], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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
        if cycle==31:
            multiDispensePumps(hardware,[0,0,0,0,0,0,500,500])
            for i in range(3):
                dispensePumps(hardware, [DBVolume1, DBVolume1, 0, 0, 0, 0, DBVolume1, DBVolume1],
                              [17, 21, 25, 29, 33, 37, 41, 43, 45, 47, 49, 51, 53, 55],
                              [18, 22, 26, 30, 34, 38, 42, 44, 46, 48, 50, 52, 54, 56],
                              [], [], [], [], [19, 23, 27, 31, 35, 39], [20, 24, 28, 32, 36, 40], is384)

                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
                waitAndStir(hardware, 3*60)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
                removeSupernatant(hardware, VacuumTime)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        elif cycle in [32,33,34,35,36]:

            dispensePumps(hardware, [DBVolume1, DBVolume1, 0, 0, 0, 0, DBVolume1, DBVolume1],
                          [17, 21, 25, 29, 33, 37, 41, 43, 45, 47, 49, 51, 53, 55],
                          [18, 22, 26, 30, 34, 38, 42, 44, 46, 48, 50, 52, 54, 56],
                          [], [], [], [], [19, 23, 27, 31, 35, 39], [20, 24, 28, 32, 36, 40], is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, 3 * 60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')
        else:
            dispenseWashes(hardware, DBVolume1, 'DB', wellListFromColumns([3,4,5]), is384)
            dispensePumps(hardware, [DBVolume1, DBVolume1, 0, 0, 0, 0, 0, 0], [41, 43, 45, 47, 49, 51, 53, 55], [42, 44, 46, 48, 50, 52, 54, 56],
                          [], [],[], [], [], [], is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
            waitAndStir(hardware, DB1Time)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        if cycle == 31:
            for i in range(3):
                dispensePumps(hardware, [DBVolume2, DBVolume2, 0, 0, 0, 0, DBVolume2, DBVolume2],
                              [17, 21, 25, 29, 33, 37, 41, 43, 45, 47, 49, 51, 53, 55],
                              [18, 22, 26, 30, 34, 38, 42, 44, 46, 48, 50, 52, 54, 56],
                              [], [], [], [], [19, 23, 27, 31, 35, 39], [20, 24, 28, 32, 36, 40], is384)

                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
                waitAndStir(hardware, 3 * 60)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')
                removeSupernatant(hardware, VacuumTime)
                TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        elif cycle in [32, 33, 34, 35, 36]:

            dispensePumps(hardware, [DBVolume2, DBVolume2, 0, 0, 0, 0, DBVolume2, DBVolume2],
                          [17, 21, 25, 29, 33, 37, 41, 43, 45, 47, 49, 51, 53, 55],
                          [18, 22, 26, 30, 34, 38, 42, 44, 46, 48, 50, 52, 54, 56],
                          [], [], [], [], [19, 23, 27, 31, 35, 39], [20, 24, 28, 32, 36, 40], is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
            waitAndStir(hardware, 3 * 60)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')
        else:
            dispenseWashes(hardware, DBVolume2, 'DB', wellListFromColumns([3, 4, 5]), is384)
            dispensePumps(hardware, [DBVolume2, DBVolume2, 0, 0, 0, 0, 0, 0], [41, 43, 45, 47, 49, 51, 53, 55],
                          [42, 44, 46, 48, 50, 52, 54, 56],
                          [], [], [], [], [], [], is384)

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

def DBPump_Test(hardware,is384):
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


    while 1:

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


        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, 60*1)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, 60)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')



        cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

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


def ElongationCycle_TwoEnz_2DiffWB2_2StepsWB2_W1(hardware,is384):
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

            dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1,2,3,4,5,6,7,8,9]), is384)
            dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([10,11,12]), is384)

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
        updateCycleLabel(hardware, cycle, "Wash1")
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1, 2, 3, 4, 5, 6, 7, 8, 9]), is384)
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([10, 11, 12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        updateCycleLabel(hardware, cycle, "Wash2")
        dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1, 2, 3, 4, 5, 6, 7, 8, 9]), is384)
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([10, 11, 12]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp2')
        waitAndStir(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc2')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac2')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    dispenseWashes(hardware, BBVolume2, 'BB', wellListFromColumns([1, 2, 3, 4, 5, 6, 7, 8, 9]), is384)
    dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([10, 11, 12]), is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1_Reprime(hardware,is384):
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

        if (cycle%15)==1 and cycle!=1 :
            print("Reprime")
            multiDispensePumps(hardware,[1000,1000,1000,1000,1000,1000])

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

def ElongationCycle_TwoEnz_W1_Reprime_DiffVol(hardware,is384):
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

        if (cycle%15)==1 and cycle!=1 :
            print("Reprime")
            multiDispensePumps(hardware,[1000,1000,1000,1000,1000,1000])

        dispensePumpsDiffCols(hardware, [10,7.5,12.5,7.5,10,7.5,12.5,7.5,10,7.5,12.5,7.5], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [20,15,25,15,20,15,25,15,20,15,25,15], 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [20,15,25,15,20,15,25,15,20,15,25,15], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [12,9,15,9,12,9,15,9,12,9,15,9], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [20,15,25,15,20,15,25,15,20,15,25,15], 'BB', usedWells,is384)
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


def ElongationCycle_TwoEnz_W1_96in384(hardware,is384):
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

            dispenseWashesColDiffVols(hardware, [50,25,50,25,50,25,50,25,50,25,50,25], 'BB', usedWells, is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsDiffCols(hardware,[25,12.5,25,12.5,25,12.5,25,12.5,25,12.5,25,12.5],[well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [50,25,50,25,50,25,50,25,50,25,50,25], 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50,25,50,25,50,25,50,25,50,25,50,25], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashesColDiffVols(hardware, [30,15,30,15,30,15,30,15,30,15,30,15], 'DB', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashesColDiffVols(hardware, [50,25,50,25,50,25,50,25,50,25,50,25], 'BB', usedWells, is384)
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


def ElongationCycle_TwoEnz_TwoWB2_W1(hardware,is384):
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

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1,3,5,7,9,11]),is384)

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

    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, 0], [], [], [], [], [], [], usedWells, [], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, 0], [], [], [], [], [], [], usedWells, [], is384)

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
        activeWells=getActiveWellsButX(sequences,cycle)
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
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5,6,11,12]), is384)
        if cycle > 200:
            dispensePumps(hardware,[0,0,0,0,0,0,50,50], [],[],[],[],[],[],[well for well in endedWells if well%2==1],[well for well in endedWells if well%2==0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixEnded')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,enz_vol,enz_vol], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],[], [],is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5,6,11,12]), is384)
        if cycle > 200:
            dispensePumps(hardware,[0,0,0,0,0,0,50,50], [],[],[],[],[],[],[well for well in endedWells if well%2==1],[well for well in endedWells if well%2==0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Ended')
        dispenseWashes(hardware, BBVolume1, 'Buff1', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5,6,11,12]), is384)
        if cycle > 200:
            dispensePumps(hardware,[0,0,0,0,0,0,50,50], [],[],[],[],[],[],[well for well in endedWells if well%2==1],[well for well in endedWells if well%2==0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1EndedWells')
        dispenseWashes(hardware, DBVolume1, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5,6,11,12]), is384)
        if cycle > 200:
            dispensePumps(hardware,[0,0,0,0,0,0,30,30], [],[],[],[],[],[],[well for well in endedWells if well%2==1],[well for well in endedWells if well%2==0], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2EndedWells')
        dispenseWashes(hardware, DBVolume2, 'DB', activeWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', wellListFromColumns([5,6,11,12]), is384)
        if cycle > 200:
            dispensePumps(hardware,[0,0,0,0,0,0,50,50], [],[],[],[],[],[],[well for well in endedWells if well%2==1],[well for well in endedWells if well%2==0], is384)

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

    dispensePumps(hardware, [0,0,0,0,0,0,BBVolume2,BBVolume2], [],[],[],[],[],[],[well for well in usedWells if well%2==1],[well for well in usedWells if well%2==0], is384)

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

def ElongationCycle_TwoEnz_W1_DispCheck(hardware,is384):
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

        wellwb1 = wellListFromHalfColumns([1,3,5,7,9,11,13,15,17,19,21,23])
        wellwb1bis = wellListFromHalfColumns([2,4,6,8,10,12,14,16,18,20,22,24])
        welldb = wellListFromHalfColumns([24,22,20,18,16,14,12,10,8,6,4,2])
        welldbbis = wellListFromHalfColumns([23,21,19,17,15,13,11,9,7,5,3,1])
        wellwb2 = wellListFromColumns([10,11,12])
        wellwb2bis = wellListFromColumns([7,8,9])
        wellwb2ter = wellListFromColumns([4,5,6])
        wellwb2quad = wellListFromColumns([1,2,3])

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

        dispenseWashes(hardware, BBVolume1, 'Buff1', wellwb1, is384)
        dispenseWashes(hardware, BBVolume1, 'Buff1', wellwb1bis, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashes(hardware, DBVolume1, 'DB', welldb, is384)
        dispenseWashes(hardware, DBVolume1, 'DB', welldbbis, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseWashes(hardware, DBVolume2, 'DB', welldb, is384)
        dispenseWashes(hardware, DBVolume1, 'DB', welldbbis, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'BB', wellwb2,is384)
        dispenseWashes(hardware, BBVolume2, 'BB', wellwb2bis, is384)
        dispenseWashes(hardware, BBVolume2, 'BB', wellwb2ter, is384)
        dispenseWashes(hardware, BBVolume2, 'BB', wellwb2quad, is384)
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
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftEDTADisp')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftEDTAInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        well1 = wellListFromColumns([1, 5, 9])
        well2 = wellListFromColumns([2, 6, 10])
        well3 = wellListFromColumns([3, 7, 11])
        well4 = wellListFromColumns([4, 8, 12])
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

def ElongationCycle_TwoEnz_4IncEBTime_W1(hardware,is384):
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

        wellU = wellListFromHalfColumns([1,3,5,7,9,11,13,15,17,19,21,23])
        wellD = wellListFromHalfColumns([2,4,6,8,10,12,14,16,18,20,22,24])


        updateCycleLabel(hardware,cycle,"Premix1")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix1')

        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol],
                      [well for well in wellU if well%2==1],
                      [well for well in wellU if well%2==0],
                      inter([wellU,nucleo_arrays[1]]),
                      inter([wellU,nucleo_arrays[2]]),
                      inter([wellU,nucleo_arrays[3]]),
                      inter([wellU,nucleo_arrays[4]]),
                      nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
        waitAndStir(hardware, 17)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc1')

        updateCycleLabel(hardware, cycle, "Premix2")
        dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                      [well for well in wellD if well % 2 == 1],
                      [well for well in wellD if well % 2 == 0],
                      inter([wellD, nucleo_arrays[1]]),
                      inter([wellD, nucleo_arrays[2]]),
                      inter([wellD, nucleo_arrays[3]]),
                      inter([wellD, nucleo_arrays[4]]),
                      nucleo_arrays[7], nucleo_arrays[8], is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc2')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac2')

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
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]) , is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1,3,5,7,9,11]) , is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash2")
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

    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0] ,
                  [],[],[],[],[],[],usedWells,[], is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispensePumps(hardware, [0, 0, 0, 0, 0, 0, 50, 0],
                  [], [], [], [], [], [], usedWells, [], is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_TwoW1(hardware,is384):
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

    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoDB(hardware,is384):
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
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
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


def ElongationCycle_TwoEnz_W1_synthesisIssue(hardware,is384):
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
        dispenseWashes(hardware, BBVolume1, 'Buff2', wellListFromColumns([2,4,5,6,8,10,12]), is384)
        dispenseWashes(hardware, BBVolume1, 'Buff1', wellListFromColumns([1,3,7,9,11]), is384)
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
    DBRinseRoutine(hardware)


def ElongationCycle_TwoEnz_W1_CloggingFJ8504(hardware,is384):
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
        double_wells=wellListFromHalfColumns([2,3,6,7,10,11,14,15,18,19,22])
        dispenseDoubleWashes_Buff1(hardware, BBVolume1, 'Buff1', double_wells, is384)
        dispenseWashes(hardware,BBVolume1,"Buff1",[89,90,91,92],is384)
        dispenseWashes(hardware,BBVolume1,"Buff2",[1,2,3,4],is384)
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



def ElongationCycle_TwoEnz_W1_PSPTblsht(hardware,is384):
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
        wells_25uM=wellListFromColumns([1,2,3,4,5,7,8,9,10,11])
        wells_15uM=wellListFromColumns([6,12])
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWells if well in wells_25uM], [well for well in activeWells if well in wells_15uM], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")

        wells_noPK=wellListFromColumns([1,2,3,4,6,7,8,9,10,12])
        wells_PK=wellListFromColumns([5,11])
        dispenseWashes(hardware, BBVolume1, 'Buff1', wells_noPK, is384)
        dispenseWashes(hardware, BBVolume1, 'Buff2', wells_PK, is384)
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

    cycles_10min=[6,11]
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


def ElongationCycleSeparatedFourEnz_W1(hardware,is384):
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


def ElongationDegenerate(hardware,is384):
    title = easygui.enterbox("Name of the run ?")

    # Save Quartet Control File
    saveQuartet = int(easygui.enterbox("Do you want to save quartet control file ? (1 yes, 0 No)"))
    if saveQuartet:
        saveQuartetControlFile(title,inspect.getsource(inspect.currentframe()))

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


def take_snapshot(hardware,folder_name):


    thermalImages = 1
    if thermalImages:
        TT = hardware.parent.rightFrame.thermalThread
    else:
        TT=FakeThermalImageThread()

    title=easygui.enterbox("Name_of_snap ?")
    # Set up recording file for thermal snapshots
    now = datetime.datetime.now()
    folder_path = "Test" + "\\" + folder_name

    TT.snapshot_in_cycle(thermalImages, folder_path, 1, title)



def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())



if __name__ == "__main__":
    wells=[1,2,4,7,9,16,18,16,10]

def ElongationCycle_TwoEnz_2DiffWB2_2volEB_1DB_W1_EndedWellsCR0(hardware,is384):
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

            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)

            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispensePumpsDiffCols(hardware, [25, 25, 15, 15, 25, 25, 15, 15, 25, 25, 15, 15], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)
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

        #Wash
        updateCycleLabel(hardware, cycle, "Wash1")
        dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, 20)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1


    dispensePumps(hardware, [0,0,0,0,0,0,0,50], [], [], [],[] , [], [],[],usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1X(hardware,is384):
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
        activeWellsButX=getActiveWellsButX(sequences,cycle)
        endedWellsPlusX=getEndedWellsPlusX(sequences,cycle)

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

        dispenseWashes(hardware, BBVolume1, 'Buff2', endedWellsPlusX, is384)
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWellsButX if well%2==1], [well for well in activeWellsButX if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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

    hardware.arduinoControl.stopHeating()
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)


def ElongationCycle_OneEnz_W1X(hardware,is384):
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
        activeWellsButX=getActiveWellsButX(sequences,cycle)
        endedWellsPlusX=getEndedWellsPlusX(sequences,cycle)

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

        dispensePumps(hardware, [enz_vol,BBVolume2,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], activeWellsButX, endedWellsPlusX, nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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

    hardware.arduinoControl.stopHeating()
    dispenseWashes(hardware, BBVolume2, 'BB', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'BB', usedWells, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_W1X_preprimenucs(hardware,is384):
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
        activeWellsButX=getActiveWellsButX(sequences,cycle)
        endedWellsPlusX=getEndedWellsPlusX(sequences,cycle)

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

        dispenseWashes(hardware, BBVolume1, 'Buff2', endedWellsPlusX, is384)
        multiDispensePumps(hardware,[0,0,25,25,25,25])
        dispensePumps(hardware, [enz_vol,enz_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol,nuc_vol], [well for well in activeWellsButX if well%2==1], [well for well in activeWellsButX if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4],nucleo_arrays[7],nucleo_arrays[8],is384)

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

    hardware.arduinoControl.stopHeating()
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)
    waitAndStir(hardware, WB2Time)
    removeSupernatant(hardware, VacuumTime)
    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells, is384)

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
        EndedWells=getEndedWellsPlusX(sequences, cycle)

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

        dispensePumpsDiffCols(hardware, [25,15,15,7.5,10,12.5,25,15,15,7.5,10,12.5], [well for well in activeWells if well%2==1], [well for well in activeWells if well%2==0], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3], nucleo_arrays[4], [], [],is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        dispenseWashesColDiffVols(hardware, [50,30,30,15,20,25,50,30,30,15,20,25], 'Buff1', usedWells, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        dispenseWashesColDiffVols(hardware, [50,30,30,15,20,25,50,30,30,15,20,25], 'DB', usedWells, is384)
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
        dispenseWashesColDiffVols(hardware, [50,30,30,15,20,25,50,30,30,15,20,25], 'BB', usedWells,is384)
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

def ElongationCycleOneEnz_EightNucs_W1_X(hardware,is384):
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
        updateCycleLabel(hardware, cycle, "Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        dispenseWashes(hardware,BBVolume2,'Buff2',endedWells,is384)
        dispensePumps(hardware, [enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol],
                        activeWells, nucleo_arrays[6], nucleo_arrays[1], nucleo_arrays[2], nucleo_arrays[3],
                        nucleo_arrays[4], nucleo_arrays[7], nucleo_arrays[8], is384)

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

def TwoElongTime_Col_TwoWB2(hardware, is384):
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

            unevenCol = wellListFromColumns([1, 2, 5, 6, 9, 10])
            evenCol = wellListFromColumns([3, 4, 7, 8, 11, 12])

            # Premix
            updateCycleLabel(hardware, cycle, "Premix")
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

            dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, 0, 0],
                          inter([unevenCol, [well for well in activeWells if well % 2 == 1]]),
                          inter([unevenCol, [well for well in activeWells if well % 2 == 0]]),
                          inter([unevenCol, nucleo_arrays[1]]),
                          inter([unevenCol, nucleo_arrays[2]]),
                          inter([unevenCol, nucleo_arrays[3]]),
                          inter([unevenCol, nucleo_arrays[4]]),
                          [], [], is384)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
            waitAndStir(hardware, 0)

            dispensePumps(hardware, [enz_vol, enz_vol, nuc_vol, nuc_vol, nuc_vol, nuc_vol, 0, 0],
                          inter([evenCol, [well for well in activeWells if well % 2 == 1]]),
                          inter([evenCol, [well for well in activeWells if well % 2 == 0]]),
                          inter([evenCol, nucleo_arrays[1]]),
                          inter([evenCol, nucleo_arrays[2]]),
                          inter([evenCol, nucleo_arrays[3]]),
                          inter([evenCol, nucleo_arrays[4]]),
                          [], [], is384)

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
            dispenseDoubleWashes_Buff1(hardware, BBVolume2, 'Buff1', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
            waitAndStir(hardware, WB2Time)
            removeSupernatant(hardware, VacuumTime)
            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

            # We carry on with next cycle or we end the loop
            nucleo_arrays_nextcycle = splitSequences(sequences, cycle + 1)
            if len(nucleo_arrays_nextcycle[0]) == len(sequences):
                cycle = 0
            else:
                cycle += 1

        dispensePumps(hardware, [0, 0, 0, 0, 0, 0, BBVolume2, 0], [], [], [], [], [], [], usedWells, [], is384)

        goToWell(hardware, 'thermalCamera', 1, 0)
        updateCycleLabel(hardware, cycle, "Synthesis End")
        hardware.arduinoControl.stopHeating()
        DBRinseRoutine(hardware)

def ElongationCycle_TwoEnz_TwoStepsWB2_2DB_W1(hardware,is384):
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
        dispenseDoubleWashes_DB(hardware, DBVolume1, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        # DB2
        updateCycleLabel(hardware, cycle, "DB2")
        dispenseDoubleWashes_DB(hardware, DBVolume2, 'DB', wellListFromColumns([1, 3, 5, 7, 9, 11]), is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "Wash")
        dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp1')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc1')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac1')

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

    dispenseWashes(hardware, BBVolume2, 'Buff2', usedWells,is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)
