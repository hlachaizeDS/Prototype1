from hardware import *
import sys


thermal_is384 = 0

def actionButton_Callback(directCommand):

    #check commit

    hardware=directCommand.parent.hardware

    #ElongationCycleSeparatedTwoEnz(hardware,0)
    #ElongationCycleSeparatedOneEnz(hardware,0)

    #ElongationCycleOneEnz_W1(hardware, 0)
    #ElongationCycleTwoEnz_W1(hardware, 0)

    #ElongationCycleSeparatedOneEnz_ProtK(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_ProtK(hardware, 0)


    #ElongationCycle_SpecialLong(hardware, 0)
    #ElongationCycle_SUPOR_Long(hardware, 0)

    #RNAProcess(hardware,0)
    #RNAProcess_diffWashVols(hardware,0)

    #PSPWashes_screen(hardware,0)
    #dispenseWashesColDiffVols(hardware,[30,40,25,50,50,50,30,40,25,50,50,50],'DB',wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12]),0)

    ElongationCycleTwoEnz_W1_NoHeatduringDB(hardware, 0)
    #ElongationCycleTwoEnz_W1_384_DB2Vols(hardware, 1)
    #ElongationCycle_TwoEnz_W1_DBforActiveWells(hardware, 0)
    #ElongationCycleSeparatedOneEnz_WLE_q47(hardware, 0)
    #ElongationCycleOneEnz_W1_TblrshootSub(hardware, 0)
    #ElongationCycleTwoEnz_W1_50W1_30DB2(hardware, 0)
    #ElongationCycleTwoEnz_W1_volW1(hardware, 0)
    #ElongationCycleTwoEnz_W1_DB2VolScreen(hardware, 0)
    #ElongationCycleTwoEnz_W1_2resins(hardware, 0)
    #ElongationCycleTwoEnz_Degenerate(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_M119_M121(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_reverseOrder(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_SeveralWashes(hardware, 1)
    #ElongationCycle_HS_25ulWashes(hardware, 0)
    #ElongationCycleSeparatedOneEnz_HS_10min(hardware, 0)

    #ElongationCycleTwoEnz_W1_50uL(hardware, 0)
    #ElongationCycleTwoEnz_W1_5s(hardware, 0)
    #ElongationCycleSeparated_M119vM96(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_PuroliteQtty(hardware, 0)
    #ElongationCycleSeparatedOneEnz_ProtK_10min(hardware, 0)
    #ElongationCycle_W1_Vol_Time_ROP(hardware, 0)
    #ElongationCycle_LS_Citrate(hardware, 0)
    #ElongationCycle_LS_shake_flush(hardware, 0)
    #ElongationCycle_LS_ReduceInsertions(hardware, 0)
    #ElongationCycle_LS_Print_dI(hardware, 0)
    #ElongationCycle_LS_PrintdI_NewResin(hardware, 0)
    #ElongationCycle_HS_96in384(hardware, 1)
    #ElongationCycle_LS_Capping(hardware, 0)
    #ElongationCycle_LS_twoWashes(hardware, 0)
    #ElongationCycle_HS_dispUnderVac(hardware, 0)
    #ElongationCycle_HS_EDTAinW1(hardware, 0)
    #ElongationCycle_HS_StirDuringEvac(hardware, 0)
    #ElongationCycle_HS_2diffWashes(hardware, 0)
    #ElongationCycle_HS_IncCoCl2(hardware, 0)
    #ElongationCycle_HS_two_washes(hardware, 0)
    #ElongationCycle_HS_EDTAinDB_FullPS(hardware, 0)
    #ElongationCycle_HS_ShortDB(hardware, 0)
    #ElongationCycle_HS_EDTA(hardware, 0)
    #ElongationCycle_HS_EBDBDiffVols(hardware,0)
    #ElongationCycleSeparatedTwoEnz_forDifferentSizes(hardware, 0)
    #ElongationCycle_HS_diffWashes(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_forDifferentSizes_PK(hardware, 0)
    #ElongationCycle_DiffElDB1_vols(hardware, 0)
    #ElongationCycle_TwoElongations(hardware, 0)
    #ElongationCycle_ProtK_everyCycle(hardware, 0)
    #ElongationCycleSeparated_M119vM96_ProtK(hardware, 0)
    #ElongationCycleSeparatedTwoEnZ_HS_EDTACo(hardware, 0)

    #ElongationCycle_HS_384_TwoWash2(hardware, 1)
    #ElongationCycle_HS_384_2DBs_revWashDB(hardware, 1)