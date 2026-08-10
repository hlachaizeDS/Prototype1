from cycles_steps import *
import datetime
import easygui
from Thermal import FakeThermalImageThread
from quartetControlSave import saveQuartetControlFile,force2digits
from tkinter_windows import *


def HeatedElution_96(hardware, is384):

    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet(path)
    getParameters(synthesis_sheet)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    easygui.msgbox(msg="Pump switched off and manifold at 80°C ? \n\nDon't forget to come back in 50min", title="Elution", ok_button="Yes", image=None, root=None)

    title = easygui.enterbox("Name of the PSP ?")

    TT = hardware.parent.rightFrame.thermalThread
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_Elution_" + title

    updateCycleLabel(hardware, 0, "PreHeat")
    TT.snapshot_in_cycle(1, folder_path, 1, 'Bef_PreHeat')
    hardware.arduinoControl.startHeating()
    wait(hardware, 20 * 60)
    TT.snapshot_in_cycle(1, folder_path, 1, 'Bef_H20_Disp')
    multi_dispense(hardware, {"DB": 1000})
    multi_dispense_in_wells(hardware, {"DB": [60, usedWells]}, is384, max_vol=30*4)
    TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_H20_Disp')
    waitAndStir(hardware, 30*60, 300)
    #wait(hardware, 30 * 60)
    TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_H20_Inc')
    hardware.arduinoControl.stopHeating()

def PSP_OnePot_96(hardware, is384):


    # We read the excel and get the parameters back
    synthesis_sheet = getExcelSheet(path)
    getParameters(synthesis_sheet)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)
    usedWells = getUsedWells(sequences)
    activeWells = getActiveWells(sequences, 1)

    Plate_plan_window(usedWells, is384)

    easygui.msgbox(msg="Pump at -40kPa switched on ?", title="96", ok_button="Yes", image=None, root=None)

    title = easygui.enterbox("Name of the PSP ?")

    TT = hardware.parent.rightFrame.thermalThread
    now = datetime.datetime.now()
    folder_path = str(now.year) + force2digits(now.month) + '\\' + str(now.year) + force2digits(
        now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
        now.second) + "_PSP_" + title

    TT.snapshot_in_cycle(1, folder_path, 1, 'BeforeAnything')

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
        removeSupernatant(hardware, 30)
        for nb in range(1):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 1")
            multi_dispense(hardware, {"DB": 1000})
            multi_dispense_in_wells(hardware, {"DB": [100, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH201_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 30)

    if PREWASH_TSTPK:
        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "Prewash TSTPK")
            multi_dispense(hardware, {"Buff2": 1000})
            multi_dispense_in_wells(hardware, {"Buff2": [100, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Disp_' + str(nb + 1))
            waitAndStir(hardware, 300)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PK_Inc_' + str(nb + 1))
            removeSupernatant(hardware, 30)

    if PREWASH_H2O_2:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 2")
            multi_dispense(hardware, {"DB": 1000})
            multi_dispense_in_wells(hardware, {"DB": [150, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH202_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, 30)

        for nb in range(2):
            updateCycleLabel(hardware, nb + 1, "EtOH Wash")
            multi_dispense(hardware, {"Buff1": 1000})
            multi_dispense_in_wells(hardware, {"Buff1": [200, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETHWash_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)

        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Prewash H20 3")
            multi_dispense(hardware, {"DB": 1000})
            multi_dispense_in_wells(hardware, {"DB": [150, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashH203_Disp_' + str(nb + 1))
            waitAndStir(hardware, 2*60)
            removeSupernatant(hardware, 30)

    if PREWASH_IPA:
        for nb in range(1):
            updateCycleLabel(hardware, nb + 1, "Prewash ipa")
            multi_dispense(hardware, {"BB": 1000})
            multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_PrewashIPA_Disp_' + str(nb + 1))
            waitAndStir(hardware, 20)
            removeSupernatant(hardware, 30)

    if PREDRYING:
        updateCycleLabel(hardware, 1, "Pre Drying")
        removeSupernatant(hardware, 7 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Predrying')

    if LIBERATION:
        updateCycleLabel(hardware, 1, "Liberation")
        multi_dispense(hardware, {"N": 1000})
        multi_dispense_in_wells(hardware, {"N": [50, usedWells]}, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Disp')
        waitAndStir(hardware, 1800)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Liberation_Inc')

    if PRECIPITATION:
        updateCycleLabel(hardware, 1, "Precipitation")
        multi_dispense(hardware, {"BB": 1000})
        multi_dispense_in_wells(hardware, {"BB": [200, usedWells]}, is384)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Disp_200')
        wait(hardware, 10 * 60)
        TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_Isop_Inc')
        removeSupernatant(hardware, 40)
        waitAndStir(hardware, 5, 1100)

    if DESALTING:
        for nb in range(3):
            updateCycleLabel(hardware, nb + 1, "Desalting")
            multi_dispense(hardware, {"Buff1": 1000})
            multi_dispense_in_wells(hardware, {"Buff1": [200, usedWells]}, is384)
            TT.snapshot_in_cycle(1, folder_path, 1, 'Aft_ETH_Disp_' + str(nb + 1))
            wait(hardware, 10)
            removeSupernatant(hardware, 60)
        waitAndStir(hardware, 5, 1100)
        for nb in range(1):
            updateCycleLabel(hardware, nb + 1, "Desalting_IPA")
            multi_dispense(hardware, {"BB": 1000})
            multi_dispense_in_wells(hardware, {"BB": [50, usedWells]}, is384)
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
