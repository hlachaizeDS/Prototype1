from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits
import inspect

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

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        multi_dispense_in_wells(hardware, {"Buff2": [50, X_wells],
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

    hardware.arduinoControl.stopHeating()

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_FourElongTime_Xbuff2(hardware,is384):

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
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 20)

        startsynth = time.time()

        #Premix
        updateCycleLabel(hardware,cycle,"Premix")
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'BefPremix')

        if cycle % 100 == 0:
            multi_dispense(hardware, {line: 200 for line in ["A","C","G","T","M","N","O","P","Q"]},max_vol=12.5)

        multi_dispense_in_wells(hardware, {"Buff2": [50, X_wells]}, is384)

        if cycle < 241:
            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([8, 11]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([8, 11]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([8, 11]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([8, 11]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([8, 11]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([8, 11]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([8, 11]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([8, 11]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([8, 11]), Q_wells])]
            }, is384)

            start = time.time()

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
            waitAndStir(hardware, 13)

            end120 = time.time()
            print('120i', end120 - start)

            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([7,10]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([7,10]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([7,10]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([7,10]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([7,10]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([7,10]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([7,10]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([7,10]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([7,10]), Q_wells])]
            }, is384)

            end90d = time.time()
            print('90d', end90d - start)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
            waitAndStir(hardware, 13)

            end90 = time.time()
            print('90i', end90 - start)

            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([9,12]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([9,12]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([9,12]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([9,12]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([9,12]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([9,12]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([9,12]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([9,12]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([9,12]), Q_wells])]
            }, is384)

            end60d = time.time()
            print('60d', end60d - start)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
            waitAndStir(hardware, 53)

            end60 = time.time()
            print('60i', end60 - start)

        if cycle > 240:
            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([8, 11]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([8, 11]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([8, 11]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([8, 11]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([8, 11]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([8, 11]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([8, 11]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([8, 11]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([8, 11]), Q_wells])]
            }, is384)

            start = time.time()

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp1')
            waitAndStir(hardware, 6)

            end120 = time.time()
            print('120i', end120 - start)

            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([1,4,7,10]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([1,4,7,10]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([1,4,7,10]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([1,4,7,10]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([1,4,7,10]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([1,4,7,10]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([1,4,7,10]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([1,4,7,10]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([1,4,7,10]), Q_wells])]
            }, is384)

            end90d = time.time()
            print('90d', end90d - start)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp2')
            waitAndStir(hardware, 6)

            end90 = time.time()
            print('90i', end90 - start)

            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([3,6,9,12]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([3,6,9,12]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([3,6,9,12]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([3,6,9,12]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([3,6,9,12]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([3,6,9,12]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([3,6,9,12]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([3,6,9,12]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([3,6,9,12]), Q_wells])]
            }, is384)

            end60d = time.time()
            print('60d', end60d - start)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp3')
            waitAndStir(hardware, 1)

            end60 = time.time()
            print('60i', end60 - start)

            multi_dispense_in_wells(hardware, {
                "M": [EBVolume, inter([ColToWell([2,5]), [well for well in activeWellsButX if well % 2 == 1]])],
                "N": [EBVolume, inter([ColToWell([2,5]), [well for well in activeWellsButX if well % 2 == 0]])],
                "A": [NucsVolume, inter([ColToWell([2,5]), A_wells])],
                "C": [NucsVolume, inter([ColToWell([2,5]), C_wells])],
                "G": [NucsVolume, inter([ColToWell([2,5]), G_wells])],
                "T": [NucsVolume, inter([ColToWell([2,5]), T_wells])],
                "O": [NucsVolume, inter([ColToWell([2,5]), O_wells])],
                "P": [NucsVolume, inter([ColToWell([2,5]), P_wells])],
                "Q": [NucsVolume, inter([ColToWell([2,5]), Q_wells])]
            }, is384)

            end45d = time.time()
            print('45d', end45d - start)

            TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftPremixDisp4')
            waitAndStir(hardware, 37)

            end45 = time.time()
            print('45i', end45 - start)

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
                                           "Buff2": [25, X_wells]}, is384)
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

    hardware.arduinoControl.stopHeating()

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    end=time.time() - startsynth
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
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

        multi_dispense_in_wells(hardware, {"Buff2": [50, X_wells],
                                           "M": [EBVolume, [well for well in activeWellsButX if well % 4 == 1]],
                                           "N": [EBVolume, [well for well in activeWellsButX if well % 4 == 2]],
                                           "A": [NucsVolume, A_wells],
                                           "C": [NucsVolume, C_wells],
                                           "G": [NucsVolume, G_wells],
                                           "T": [NucsVolume, T_wells],
                                           "O": [EBVolume, [well for well in activeWellsButX if well % 4 == 3]],
                                           "P": [EBVolume, [well for well in activeWellsButX if well % 4 == 0]],
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

    hardware.arduinoControl.stopHeating()

    multi_dispense(hardware, {"Buff2": 200})
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_Xop(hardware,is384):

    easygui.msgbox(msg="Pump at -40kPa switched on ?", title="96", ok_button="Yes", image=None, root=None)

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

        start = time.time()

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

    multi_dispense(hardware, {"O": 500, "P": 500})
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                        "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                        "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)

def Synthesis_OneEnz_FourDB_Xbuff2(hardware,is384):

    easygui.msgbox(msg="Pump at -40kPa switched on ?", title="96", ok_button="Yes", image=None, root=None)

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

        start = time.time()

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

        multi_dispense_in_wells(hardware, {"Buff2": [25, X_wells]}, is384)

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
        multi_dispense_in_wells(hardware, {"N": [DBVolume1, inter([activeWellsButX,[well for well in ColToWell([1,3,5,7,9,11]) if well % 4 in [1,2]]])],
                                           "O": [DBVolume1, inter([activeWellsButX,[well for well in ColToWell([1,3,5,7,9,11]) if well % 4 in [3,0]]])],
                                           "P": [DBVolume1, inter([activeWellsButX,[well for well in ColToWell([2,4,6,8,10,12]) if well % 4 in [1,2]]])],
                                           "Q": [DBVolume1, inter([activeWellsButX,[well for well in ColToWell([2,4,6,8,10,12]) if well % 4 in [3,0]]])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"N": [DBVolume2, inter([activeWellsButX,[well for well in ColToWell([1,3,5,7,9,11]) if well % 4 in [1,2]]])],
                                           "O": [DBVolume2, inter([activeWellsButX,[well for well in ColToWell([1,3,5,7,9,11]) if well % 4 in [3,0]]])],
                                           "P": [DBVolume2, inter([activeWellsButX,[well for well in ColToWell([2,4,6,8,10,12]) if well % 4 in [1,2]]])],
                                           "Q": [DBVolume2, inter([activeWellsButX,[well for well in ColToWell([2,4,6,8,10,12]) if well % 4 in [3,0]]])]}, is384)
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

    multi_dispense(hardware, {"Buff2": 500})
    multi_dispense_in_wells(hardware, {"Buff2" : [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"Buff2" : [50, usedWells]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
    DBRinseRoutine(hardware)

def Synthesis_TwoEnz_TwoDB_Xop(hardware,is384):

    easygui.msgbox(msg="Pump at -40kPa switched on ?", title="96", ok_button="Yes", image=None, root=None)

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


        start = time.time()

        if (cycle==1):
            removeSupernatant(hardware, 20)

            multi_dispense_in_wells(hardware,{"Buff2":[50,usedWells]},is384)

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
        multi_dispense_in_wells(hardware, {"Buff1": [BBVolume1, activeWellsButX]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Disp')
        waitAndStir(hardware, WB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftW1Vac')

        #DB1
        updateCycleLabel(hardware, cycle, "DB1")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([1,3,4,5,7,9,11])])],
                                           "BB": [DBVolume1, inter([activeWellsButX,wellListFromColumns([2,6,8,10,12])])]}, is384)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Disp')
        waitAndStir(hardware, DB1Time)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Inc')

        removeSupernatant(hardware, VacuumTime)
        TT.snapshot_in_cycle(thermalImages, folder_path, cycle, 'AftDB1Vac')

        #DB2
        updateCycleLabel(hardware, cycle, "DB2")
        multi_dispense_in_wells(hardware, {"DB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([1,3,4,5,7,9,11])])],
                                           "BB": [DBVolume2, inter([activeWellsButX,wellListFromColumns([2,6,8,10,12])])]}, is384)
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

    multi_dispense(hardware, {"O": 500, "P": 500})
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                        "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"O": [50, [well for well in usedWells if well % 2 == 1]],
                                        "P": [50, [well for well in usedWells if well % 2 == 0]]}, is384)

    goToWell(hardware, 'thermalCamera', 1,0)
    updateCycleLabel(hardware, cycle, "Synthesis End")
    hardware.arduinoControl.stopHeating()
    end=time.time() - start
    print('End ', end)
    print('End', time.strftime("%H:%M:%S", time.gmtime(end)))
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

            multi_dispense_in_wells(hardware,{"BB":[50,usedWells]},is384)

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
                                           "P": [50, X_wells],
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

    multi_dispense(hardware, {"P": 500})
    multi_dispense_in_wells(hardware, {"P": [50, usedWells]}, is384)
    waitAndStir(hardware, 20)
    removeSupernatant(hardware, 20)
    multi_dispense_in_wells(hardware, {"P": [50, usedWells]}, is384)

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
