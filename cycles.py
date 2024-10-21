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

def getParameters(synthesis_sheet):

    param_indexes=findIndexes('Parameter',synthesis_sheet)


    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())