from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits


def PSPOnePot_384(hardware, is384):

    title = easygui.enterbox("Name of the PSP ?")
    TT = hardware.parent.rightFrame.thermalThread
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_PSP_" + title

    TT.snapshot_in_cycle(1, folder_path, 1, 'BeforeAnything')

    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet_384(path)
    getParameters(synthesis_sheet)
    sequences = getSequences_384(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    vacuum_time=30 #s

    #LINES
    TSTPK="Buff2"
    LB="M"
    H20="DB"
    ETH="Buff1"
    ISOP="BB"

    #STEPS
    PREWASH_H2O_1=1
    PREWASH_TSTPK=1
    PREWASH_H2O_2=1
    PREWASH_ETH=1
    PREDRYING=1
    LIBERATION=1
    PRECIPITATION=1
    DESALTING=1
    DRYING=1


    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            multi_dispense(hardware,{"DB":1000})
            multi_dispense_in_wells(hardware,{"DB": [25, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_'+str(nb+1))
            waitAndStir(hardware,30)
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multi_dispense(hardware, {"Buff2":1000})
            multi_dispense_in_wells(hardware, {"Buff2": [50, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware,300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            multi_dispense(hardware, {"DB": 1000})
            multi_dispense_in_wells(hardware, {"DB": [25, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 30)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_ETH:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Prewash ETH")
            multi_dispense(hardware, {"Buff1": 1000})
            multi_dispense_in_wells(hardware, {"Buff1": [25, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashETH_Disp_' + str(nb + 1))
            waitAndStir(hardware, 10)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 20*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        multi_dispense(hardware, {"M": 1000})
        multi_dispense_in_wells(hardware, {"M": [20, usedWells]}, is384, max_vol=10)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware,1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')
        hardware.arduinoControl.stopHeating()

    if PRECIPITATION:
        hardware.arduinoControl.stopHeating()
        updateCycleLabel(hardware, 1, "Precipitation")
        multi_dispense(hardware, {"BB": 1000})
        multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp')
        wait(hardware,20*60)
        removeSupernatant(hardware, 40)

    if DESALTING:
        hardware.arduinoControl.stopHeating()
        for nb in range(5):
            updateCycleLabel(hardware, nb + 1, "Desalting" + str(nb + 1))
            multi_dispense(hardware, {"Buff1": 1000})
            multi_dispense_in_wells(hardware, {"Buff1": [70, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

    if DRYING:
        hardware.arduinoControl.startHeating()
        updateCycleLabel(hardware, 1, "Drying")
        removeSupernatant(hardware, 20*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Drying')
        hardware.arduinoControl.stopHeating()


    updateCycleLabel(hardware, 0, "PSP Done")


def PSPOnePot_384_4quadrantsversion(hardware, is384):

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

    vacuum_time=30 #s

    #LINES
    TSTPK="Buff2"
    LB="M"
    H20="DB"
    ETH="Buff1"
    ISOP="BB"

    #STEPS
    PREWASH_H2O_1=1
    PREWASH_TSTPK=1
    PREWASH_H2O_2=1
    PREWASH_ETH=1
    PREDRYING=1
    LIBERATION=1
    PRECIPITATION=1
    DESALTING=1
    DRYING=1


    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0])
            dispenseWashes(hardware, 25, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_'+str(nb+1))
            waitAndStir(hardware,30)
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            dispenseWashes(hardware, 50, TSTPK, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware,300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0])
            dispenseWashes(hardware, 25, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 30)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_ETH:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Prewash ETH")
            multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,0,0,1000,0])
            dispenseWashes(hardware, 25, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashETH_Disp_' + str(nb + 1))
            waitAndStir(hardware, 10)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 20*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        multiDispensePumps(hardware, [0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        dispensePumps(hardware, [0, 20, 0, 0, 0, 0, 0, 0], [], usedWells, [], [], [], [], [], [], is384, max_vol=10)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware,1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')
        hardware.arduinoControl.stopHeating()

    if PRECIPITATION:
        hardware.arduinoControl.stopHeating()
        updateCycleLabel(hardware, 1, "Precipitation")
        multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
        dispenseWashes(hardware, 50, ISOP, usedWells, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp')
        wait(hardware,20*60)
        removeSupernatant(hardware, 40)

    if DESALTING:
        hardware.arduinoControl.stopHeating()
        for nb in range(5):
            updateCycleLabel(hardware, nb + 1, "Desalting" + str(nb + 1))
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            dispenseWashes(hardware, 70, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

    if DRYING:
        #hardware.arduinoControl.startHeating()
        updateCycleLabel(hardware, 1, "Drying")
        removeSupernatant(hardware, 20*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Drying')


    updateCycleLabel(hardware, 0, "PSP Done")


def PSPWashes_96OP(hardware, is384):

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

    vacuum_time=30 #s

    #LINES
    TSTPK="M"
    LB="N"
    H20="DB"
    ETH="Buff1"
    ISOP="BB"

    #STEPS
    PREWASH_H2O_1=1
    PREWASH_TSTPK=1
    PREWASH_H2O_2=1
    PREWASH_ETH=1
    PREDRYING=1
    LIBERATION=1
    PRECIPITATION=1
    DESALTING=1
    DRYING=1


    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_'+str(nb+1))
            waitAndStir(hardware,5)
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            dispensePumps(hardware,[100,0,0,0,0,0],usedWells,[],[],[],[],[],is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware,300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(5):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 50, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 5)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_ETH:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Prewash ETH")
            dispenseWashes(hardware, 50, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashETH_Disp_' + str(nb + 1))
            waitAndStir(hardware, 30)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 15*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        dispensePumps(hardware,[0,50,0,0,0,0],[],usedWells,[],[],[],[],is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware,1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')
        hardware.arduinoControl.stopHeating()

    if PRECIPITATION:
        hardware.arduinoControl.stopHeating()
        updateCycleLabel(hardware, 1, "Precipitation")
        dispenseWashes(hardware, 200, ISOP, usedWells, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp')
        wait(hardware,15*60)
        removeSupernatant(hardware, 40)

    if DESALTING:
        hardware.arduinoControl.stopHeating()
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Desalting")
            dispenseWashes(hardware, 200, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

    if DRYING:
        #hardware.arduinoControl.startHeating()
        updateCycleLabel(hardware, 1, "Drying")
        removeSupernatant(hardware, 15*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Drying')


    updateCycleLabel(hardware, 0, "PSP Done")

def PSPWashes_96OP_extraH20andEtOH_IsoTime_EthConc(hardware, is384):
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
    PREWASH_H2O_1 = 0
    PREWASH_TSTPK = 0
    PREWASH_H2O_2 = 0
    PREWASH_IPA = 0
    PREDRYING = 0
    LIBERATION = 0
    PRECIPITATION = 0
    DESALTING = 1
    DRYING = 1

    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 150, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, vacuum_time)

        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, wellListFromColumns([1,2,3,4]), is384)
            dispenseWashes(hardware, 200, "Buff2", wellListFromColumns([5,6]), is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            dispenseWashes(hardware, 150, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

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
        dispenseWashes(hardware, 200, ISOP, wellListFromColumns([1,2,5,6]), is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp_200')
        wait(hardware, 7 * 60)
        multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
        dispenseWashes(hardware, 200, ISOP, wellListFromColumns([3,4]), is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp_200')
        wait(hardware, 3 * 60)
        removeSupernatant(hardware, 40)
        waitAndStir(hardware, 5, 1100)

    if DESALTING:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Desalting")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, wellListFromColumns([1,2,3,4]), is384)
            dispenseWashes(hardware, 200, "Buff2", wellListFromColumns([5,6]), is384)
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

def PSPWashes_96OP_onlynucs(hardware, is384):

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

    vacuum_time=5 #s

    #LINES
    TSTPK="M"
    LB="N"
    H20="G" and "T"
    ETH="A"
    ISOP="C"

    #STEPS
    PREWASH_H2O_1=1
    PREWASH_TSTPK=1
    PREWASH_H2O_2=1
    PREWASH_ETH=1
    PREDRYING=1
    LIBERATION=1
    PRECIPITATION=1
    DESALTING=1
    DRYING=1


    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            volume=100
            dispensePumps(hardware, [0,0,0,0,volume,volume], [], [], [], [], [well for well in usedWells if well%2==1],[well for well in usedWells if well%2==0], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_'+str(nb+1))
            waitAndStir(hardware,5)
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_TSTPK:
        times=[5*60,5*60]
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            dispensePumps(hardware,[100,0,0,0,0,0],usedWells,[],[],[],[],[],is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware,times[nb])
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware,vacuum_time)

    if PREWASH_H2O_2:
        if PREWASH_H2O_1==0 and PREWASH_TSTPK==0:
            removeSupernatant(hardware,vacuum_time)
        for nb in range(5):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            volume=100
            dispensePumps(hardware, [0, 0, 0, 0, volume, volume], [], [], [], [],
                          [well for well in usedWells if well % 2 == 1], [well for well in usedWells if well % 2 == 0],
                          is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 10)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_ETH:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Prewash ETH")
            volume=50
            dispensePumps(hardware, [0, 0, volume, 0, 0, 0], [], [], usedWells, [],[], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashETH_Disp_' + str(nb + 1))
            waitAndStir(hardware, 30)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 15*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        dispensePumps(hardware,[0,50,0,0,0,0],[],usedWells,[],[],[],[],is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware,1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')
        hardware.arduinoControl.stopHeating()

    if PRECIPITATION:
        hardware.arduinoControl.stopHeating()
        updateCycleLabel(hardware, 1, "Precipitation")
        volume = 200
        dispensePumps(hardware, [0, 0, 0, volume, 0, 0], [], [], [], usedWells, [], [], is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp')
        wait(hardware,15*60)
        input("Press a key to continue")
        removeSupernatant(hardware, 2*vacuum_time)

    if DESALTING:
        hardware.arduinoControl.stopHeating()
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Desalting")
            volume = 200
            dispensePumps(hardware, [0, 0, volume, 0, 0, 0], [], [], usedWells, [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 2*vacuum_time)

    if DRYING:
        #hardware.arduinoControl.startHeating()
        updateCycleLabel(hardware, 1, "Drying")
        removeSupernatant(hardware, 15*60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Drying')


    updateCycleLabel(hardware, 0, "PSP Done")

def PSPWashes_96OP_AV(hardware, is384):
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

    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            #multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            #dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            input("dispense tst")
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 200, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2 * 60)
            removeSupernatant(hardware, vacuum_time)

        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            dispenseWashes(hardware, 200, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2 * 60)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        #multiDispensePumps(hardware, [0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        #dispensePumps(hardware, [0, 50, 0, 0, 0, 0, 0, 0], [], usedWells, [], [], [], [], [], [], is384)
        input("dispense LB")
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware, 1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')

    if PRECIPITATION:
        updateCycleLabel(hardware, 1, "Precipitation")
        multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
        dispenseWashes(hardware, 200, ISOP, usedWells, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp_200')
        wait(hardware, 10 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Inc')
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

def PSP_OnePot_96(hardware, is384):
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

    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 200, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

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

def PSPWashes_96OP_extraH20andEtOH(hardware, is384):
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

    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 150, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, vacuum_time)

        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            dispenseWashes(hardware, 150, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

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
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Inc')
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

def PSPWashes_96OP_extraH20andEtOH_Soft(hardware, is384):
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

    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 175, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60,700)
            removeSupernatant(hardware, vacuum_time)

        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            dispenseWashes(hardware, 175, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60,700)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

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
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Inc')
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

def PSPWashes_96OP_extraH20andEtOH_half(hardware, is384):
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

    if PREWASH_H2O_1:
        removeSupernatant(hardware, vacuum_time)
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            dispenseWashes(hardware, 100, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multiDispensePumps(hardware, [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dispensePumps(hardware, [100, 0, 0, 0, 0, 0, 0, 0], usedWells, [], [], [], [], [], [], [], is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_H2O_2:
        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            dispenseWashes(hardware, 200, H20, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, vacuum_time)

        wells_extra_wash = wellListFromHalfColumns([1, 3, 5, 8, 10, 12, 13, 15, 17, 20, 22, 24])
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000])
            dispenseWashes(hardware, 200, ETH, wells_extra_wash, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

        for nb in range(3):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            dispenseWashes(hardware, 200, H20, wells_extra_wash, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, vacuum_time)

    if PREWASH_IPA:
        for nb in range(1):
            multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0])
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            dispenseWashes(hardware, 50, ISOP, usedWells, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, vacuum_time)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

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