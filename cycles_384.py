from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits
import inspect
from tkinter_windows import *

def Synthesis384_TwoEnz_Xbuff2(hardware, is384):

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        oddWells = RowToWell_384([1, 3, 5, 7, 9, 11, 13, 15])
        evenWells = RowToWell_384([2, 4, 6, 8, 10, 12, 14, 16])
        oddActiveWells = inter([activeWellsButX, oddWells])
        evenActiveWells = inter([activeWellsButX, evenWells])
        A_active_wells = inter([activeWellsButX, A_wells])
        C_active_wells = inter([activeWellsButX, C_wells])
        G_active_wells = inter([activeWellsButX, G_wells])
        T_active_wells = inter([activeWellsButX, T_wells])

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[25,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [NucsVolume, O_wells],
                                           "P": [NucsVolume, P_wells],
                                           "Q": [NucsVolume, Q_wells],
                                           "Buff2": [12, X_wells]
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

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis384_TwoEnz_4X12buff2(hardware, is384):

    easygui.msgbox(msg="Pump at -20kPa switched on ?", title="384", ok_button="Yes", image=None, root=None)

    synthesis_sheet = getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences = getSequences_384(synthesis_sheet)
    usedWells = getUsedWells(sequences)
    Plate_plan_window(usedWells, is384)

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        oddWells = RowToWell_384([1,3,5,7,9,11,13,15])
        evenWells = RowToWell_384([2,4,6,8,10,12,14,16])
        oddActiveWells = inter([activeWellsButX, oddWells])
        evenActiveWells = inter([activeWellsButX, evenWells])
        A_active_wells = inter([activeWellsButX,A_wells])
        C_active_wells = inter([activeWellsButX, C_wells])
        G_active_wells = inter([activeWellsButX, G_wells])
        T_active_wells = inter([activeWellsButX, T_wells])

        start=time.time()

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[25,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        if cycle % 4 == 1:
            multi_dispense_in_wells(hardware, {"Buff2": [12, X_wells]}, is384)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           }, is384)

        elongTime=time.time()
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        print('Elong ', time.time() - elongTime)
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

        goToWell(hardware, 'thermalCamera', 1, 0)
        hardware.vacValveOpen()
        wait(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'DuringVac')
        hardware.vacValveClose()
        wait(hardware, 3)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')
        print('Cycle ', cycle, time.time() - start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)

def Synthesis384_TwoEnz_ThreeWB2_4X12q(hardware, is384):

    easygui.msgbox(msg="Pump at -20kPa switched on ?", title="384", ok_button="Yes", image=None, root=None)

    synthesis_sheet = getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences = getSequences_384(synthesis_sheet)
    usedWells = getUsedWells(sequences)
    Plate_plan_window(usedWells, is384)

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        oddWells = RowToWell_384([1,3,5,7,9,11,13,15])
        evenWells = RowToWell_384([2,4,6,8,10,12,14,16])
        oddActiveWells = inter([activeWellsButX, oddWells])
        evenActiveWells = inter([activeWellsButX, evenWells])
        A_active_wells = inter([activeWellsButX,A_wells])
        C_active_wells = inter([activeWellsButX, C_wells])
        G_active_wells = inter([activeWellsButX, G_wells])
        T_active_wells = inter([activeWellsButX, T_wells])

        start=time.time()

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB": [25, ColToWell_384([20,23])],
                                           "Buff2": [25, ColToWell_384([21,24])],
                                           "O": [25, [well for well in ColToWell_384([19,22]) if well % 4 in [1,2]]],
                                           "P": [25, [well for well in ColToWell_384([19,22]) if well % 4 in [3,0]]]}, is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        if cycle % 4 == 1:
            multi_dispense_in_wells(hardware, {"Q": [12, X_wells]}, is384)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           }, is384)

        elongTime=time.time()
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        print('Elong ', time.time() - elongTime)
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
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, inter([activeWellsButX, ColToWell_384([20,23])])],
                                           "Buff2": [BBVolume2, inter([activeWellsButX, ColToWell_384([21,24])])],
                                           "O": [BBVolume2, inter([activeWellsButX, [well for well in ColToWell_384([19,22]) if well % 4 in [1,2]]])],
                                           "P": [BBVolume2, inter([activeWellsButX, [well for well in ColToWell_384([19,22]) if well % 4 in [3,0]]])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        goToWell(hardware, 'thermalCamera', 1, 0)
        hardware.vacValveOpen()
        wait(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'DuringVac')
        hardware.vacValveClose()
        wait(hardware, 3)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')
        print('Cycle ', cycle, time.time() - start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Q": 200})
    multi_dispense_in_wells(hardware, {"Q": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Q": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)

def Synthesis384_OneEnz_FourDB_4X12buff2(hardware, is384):

    easygui.msgbox(msg="Pump at -20kPa switched on ?", title="384", ok_button="Yes", image=None, root=None)

    synthesis_sheet = getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences = getSequences_384(synthesis_sheet)
    usedWells = getUsedWells(sequences)
    Plate_plan_window(usedWells, is384)

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        oddWells = RowToWell_384([1,3,5,7,9,11,13,15])
        evenWells = RowToWell_384([2,4,6,8,10,12,14,16])
        oddActiveWells = inter([activeWellsButX, oddWells])
        evenActiveWells = inter([activeWellsButX, evenWells])
        A_active_wells = inter([activeWellsButX,A_wells])
        C_active_wells = inter([activeWellsButX, C_wells])
        G_active_wells = inter([activeWellsButX, G_wells])
        T_active_wells = inter([activeWellsButX, T_wells])

        start=time.time()

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB": [50, usedWells]}, is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        if cycle % 4 == 1:
            multi_dispense_in_wells(hardware, {"Buff2": [12, X_wells]}, is384)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, activeWellsButX],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           }, is384)

        elongTime=time.time()
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        print('Elong ', time.time() - elongTime)
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
        multi_dispense_in_wells(hardware, {"N": [DBVolume1, [well for well in activeWellsButX if well % 8 in [1, 2]]],
                                           "O": [DBVolume1, [well for well in activeWellsButX if well % 8 in [3, 4]]],
                                           "P": [DBVolume1, [well for well in activeWellsButX if well % 8 in [5, 6]]],
                                           "Q": [DBVolume1, [well for well in activeWellsButX if well % 8 in [7, 0]]]
                                           }, is384, max_vol=12.5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"N": [DBVolume2, [well for well in activeWellsButX if well % 8 in [1, 2]]],
                                           "O": [DBVolume2, [well for well in activeWellsButX if well % 8 in [3, 4]]],
                                           "P": [DBVolume2, [well for well in activeWellsButX if well % 8 in [5, 6]]],
                                           "Q": [DBVolume2, [well for well in activeWellsButX if well % 8 in [7, 0]]]
                                           }, is384)
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

        goToWell(hardware, 'thermalCamera', 1, 0)
        hardware.vacValveOpen()
        wait(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'DuringVac')
        hardware.vacValveClose()
        wait(hardware, 3)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')
        print('Cycle ', cycle, time.time() - start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)

def Synthesis384_OneEnz_FourWB2_4X12buff2(hardware, is384):

    easygui.msgbox(msg="Pump at -20kPa switched on ?", title="384", ok_button="Yes", image=None, root=None)

    synthesis_sheet = getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences = getSequences_384(synthesis_sheet)
    usedWells = getUsedWells(sequences)
    Plate_plan_window(usedWells, is384)

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        oddWells = RowToWell_384([1,3,5,7,9,11,13,15])
        evenWells = RowToWell_384([2,4,6,8,10,12,14,16])
        oddActiveWells = inter([activeWellsButX, oddWells])
        evenActiveWells = inter([activeWellsButX, evenWells])
        A_active_wells = inter([activeWellsButX,A_wells])
        C_active_wells = inter([activeWellsButX, C_wells])
        G_active_wells = inter([activeWellsButX, G_wells])
        T_active_wells = inter([activeWellsButX, T_wells])

        start=time.time()

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"N": [25, [well for well in usedWells if well % 8 in [1, 2]]],
                                           "O": [25, [well for well in usedWells if well % 8 in [3, 4]]],
                                           "P": [25, [well for well in usedWells if well % 8 in [5, 6]]],
                                           "Q": [25, [well for well in usedWells if well % 8 in [7, 0]]]
                                           }, is384, max_vol=12.5)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        if cycle % 4 == 1:
            multi_dispense_in_wells(hardware, {"Buff2": [12, X_wells]}, is384)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, activeWellsButX],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           }, is384)

        elongTime=time.time()
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        print('Elong ', time.time() - elongTime)
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
        multi_dispense_in_wells(hardware, {"DB": [ DBVolume1, activeWellsButX]}, is384)
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
        multi_dispense_in_wells(hardware, {"N": [BBVolume2, [well for well in activeWellsButX if well % 8 in [1, 2]]],
                                           "O": [BBVolume2, [well for well in activeWellsButX if well % 8 in [3, 4]]],
                                           "P": [BBVolume2, [well for well in activeWellsButX if well % 8 in [5, 6]]],
                                           "Q": [BBVolume2, [well for well in activeWellsButX if well % 8 in [7, 0]]]
                                           }, is384, max_vol=12.5)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBDisp')
        waitAndStir(hardware, WB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBInc')

        goToWell(hardware, 'thermalCamera', 1, 0)
        hardware.vacValveOpen()
        wait(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'DuringVac')
        hardware.vacValveClose()
        wait(hardware, 3)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')
        print('Cycle ', cycle, time.time() - start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)


def Synthesis384_OneEnz_Xbuff2(hardware, is384):

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
        [ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,X_wells,Q_wells] \
            = splitSequences(sequences,cycle)

        usedWells = getUsedWells(sequences)
        activeWells = getActiveWells(sequences,cycle)
        activeWellsButX = [well for well in activeWells if well not in X_wells]
        oddWells = RowToWell_384([1, 3, 5, 7, 9, 11, 13, 15])
        evenWells = RowToWell_384([2, 4, 6, 8, 10, 12, 14, 16])
        oddActiveWells = inter([activeWellsButX, oddWells])
        evenActiveWells = inter([activeWellsButX, evenWells])
        A_active_wells = inter([activeWellsButX, A_wells])
        C_active_wells = inter([activeWellsButX, C_wells])
        G_active_wells = inter([activeWellsButX, G_wells])
        T_active_wells = inter([activeWellsButX, T_wells])

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[25,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, activeWellsButX],
                                           "N": [NucsVolume, N_wells],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [NucsVolume, O_wells],
                                           "P": [NucsVolume, P_wells],
                                           "Q": [NucsVolume, Q_wells],
                                           "Buff2": [12, X_wells]
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

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis384_OneEnz_SixDB_4X12S3(hardware, is384):

    easygui.msgbox(msg="Pump at -20kPa switched on ?", title="384", ok_button="Yes", image=None, root=None)

    synthesis_sheet = getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences = getSequences_384(synthesis_sheet)
    usedWells = getUsedWells(sequences)
    Plate_plan_window(usedWells, is384)

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
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

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)


        multi_dispense_in_wells(hardware, {"BB": [12, X_wells]}, is384)

        multi_dispense_in_wells(hardware, {"M": [EBVolume, activeWellsButX],
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
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([[well for well in activeWellsButX if well % 2 == 1], ColToWell_384([15, 18, 21, 24]), ])],
                                           "Buff2": [DBVolume1, inter([[well for well in activeWellsButX if well % 2 == 0], ColToWell_384([15, 18, 21, 24]),])],
                                           "N": [DBVolume1, inter([[well for well in activeWellsButX if well % 8 in [1,2]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])],
                                           "O": [DBVolume1, inter([[well for well in activeWellsButX if well % 8 in [3,4]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])],
                                           "P": [DBVolume1, inter([[well for well in activeWellsButX if well % 8 in [5,6]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])],
                                           "Q": [DBVolume1, inter([[well for well in activeWellsButX if well % 8 in [7,0]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([[well for well in activeWellsButX if well % 2 == 1], ColToWell_384([15, 18, 21, 24]), ])],
                                           "Buff2": [DBVolume2, inter([[well for well in activeWellsButX if well % 2 == 0], ColToWell_384([15, 18, 21, 24]),])],
                                           "N": [DBVolume2, inter([[well for well in activeWellsButX if well % 8 in [1,2]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])],
                                           "O": [DBVolume2, inter([[well for well in activeWellsButX if well % 8 in [3,4]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])],
                                           "P": [DBVolume2, inter([[well for well in activeWellsButX if well % 8 in [5,6]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])],
                                           "Q": [DBVolume2, inter([[well for well in activeWellsButX if well % 8 in [7,0]], ColToWell_384([13, 14, 16, 17, 19, 20, 22, 23]),])]}, is384)
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
        print('Cycle ',cycle, time.time() - start)

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense_in_wells(hardware, {"BB": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"BB": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)

def Synthesis384_TwoEnz_Xbuff2_1sur4(hardware, is384):

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
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

            multi_dispense_in_wells(hardware,{"BB":[25,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "BB": [12, inter([wellListFromColumns_384([15,22,23,24]), X_wells])]
                                           }, is384)

        if cycle % 4 == 1:
                multi_dispense_in_wells(hardware, {"BB": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,6.5,25,12,6.5,25,0,0,0],inter([wellListFromColumns_384([16,17,18,19,20,21]), X_wells])]
                                           },is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')

        goToWell(hardware, 'thermalCamera', 1, 0)
        hardware.vacValveOpen()
        wait(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'DuringVacElong')
        hardware.vacValveClose()
        wait(hardware, 3)

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

        goToWell(hardware, 'thermalCamera', 1, 0)
        hardware.vacValveOpen()
        wait(hardware, 10)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'DuringVac')
        hardware.vacValveClose()
        wait(hardware, 3)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftBBVac')

        #We carry on with next cycle or we end the loop
        nucleo_arrays_nextcycle=splitSequences(sequences,cycle+1)
        if len(nucleo_arrays_nextcycle[0])==len(sequences):
            cycle=0
        else:
            cycle+=1

    multi_dispense(hardware,{"Buff2":200})
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis384_TwoEnz_Xall(hardware, is384):

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
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

            multi_dispense_in_wells(hardware,{"BB":[25,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "Buff2": [25, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX],
                                           "Buff2": [25, X_wells]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, activeWellsButX],
                                           "Buff2": [25, X_wells]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, activeWellsButX],
                                           "Buff2": [15, X_wells]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [BBVolume2, activeWellsButX],
                                           "Buff2": [25, X_wells]}, is384)
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

    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Synthesis384_TwoEnz_halfvol_X(hardware, is384):

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
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

        multi_dispense_in_wells(hardware, {"M": [[EBVolume,EBVolume,EBVolume,EBVolume/2,EBVolume/2,EBVolume,EBVolume/2,EBVolume/2,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume], [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [[EBVolume,EBVolume,EBVolume,EBVolume/2,EBVolume/2,EBVolume,EBVolume/2,EBVolume/2,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume,EBVolume], [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [[NucsVolume,NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume ,NucsVolume,NucsVolume,NucsVolume], A_wells],
                                           "C": [[NucsVolume,NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume ,NucsVolume,NucsVolume,NucsVolume], C_wells],
                                           "G": [[NucsVolume,NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume ,NucsVolume,NucsVolume,NucsVolume], G_wells],
                                           "T": [[NucsVolume,NucsVolume,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume/2,NucsVolume/2,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume,NucsVolume ,NucsVolume,NucsVolume,NucsVolume], T_wells],
                                           "Buff2": [25, X_wells]
                                           }, is384)

        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp')
        waitAndStir(hardware, Elong_time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixInc')
        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixVac')

        # W1
        updateCycleLabel(hardware, cycle, "W1")
        multi_dispense_in_wells(hardware, {"Buff1": [[BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1/2,BBVolume1,BBVolume1,BBVolume1/2,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1,BBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1/2,DBVolume1,DBVolume1,DBVolume1/2,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1,DBVolume1], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [[DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2/2,DBVolume2,DBVolume2,DBVolume2/2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2,DBVolume2], activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Disp')
        waitAndStir(hardware, DB2Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB2Vac')

        #Wash
        updateCycleLabel(hardware, cycle, "W2")
        multi_dispense_in_wells(hardware, {"BB": [[BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2/2,BBVolume2,BBVolume2,BBVolume2/2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2,BBVolume2], activeWellsButX]}, is384)
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

    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    DBRinseRoutine(hardware)

def Humidification_Test(hardware, is384):


    TT = hardware.parent.rightFrame.thermalThread

    # Set up recording file for thermal snapshots
    folder_path = "Tests\\humidification_tests2"

    TT.snapshot_in_cycle(1, folder_path, 1, 'BeforeAnything')
    start=time.time()
    n=0

    while(1):

        print(n)
        end=time.time()
        print(end-start)

        hardware.vacValveOpen()

        wait(hardware, 2)
        TT.snapshot_in_cycle(1, folder_path, 1, 'After ' + str(n*3) + " min")
        wait(hardware, 3)

        hardware.vacValveClose()

        wait(hardware, 3)
        wait(hardware,3*60)

        n=n+1

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
        synthesis_sheet = getExcelSheet_384(path)
        getParameters(synthesis_sheet)
        sequences = getSequences_384(synthesis_sheet)
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

            multi_dispense_in_wells(hardware,{"BB":[25,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)



        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        multi_dispense_in_wells(hardware, {"M": [EBVolume, [well for well in activeWellsButX if well % 4 in [1,2]]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 in [3,0]]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "Buff2": [25, X_wells]
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

    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [25, usedWells]}, is384)

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