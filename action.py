from hardware import *
from PSPs import *
import sys


thermal_is384 = 0

def actionButton_Callback(directCommand):


    #hardware.arduinoControl.startShaking(1300)
    hardware=directCommand.parent.hardware
    #take_snapshot(hardware,"Newheater")
    #ElongationTwoEnz_HighScale_10minSomeCycles(hardware, 0)
    #ElongationCycleSeparatedFourEnz_B4(hardware, 0)
    #ElongationCycle_TwoEnz_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoW1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_synthesisIssue(hardware, 0)
    #ElongationCycle_TwoEnz_W1_CloggingFJ8504(hardware, 0)
    #ElongationCycle_TwoEnz_W1_PSPTblsht(hardware, 0)
    #ElongationCycle_TwoEnz_W1_10minsomeCycles(hardware, 0)
    #ElongationCycle_OneEnz_W1(hardware, 0)
    #ElongationCycle_OneEnz_W1_10minsomeCycles(hardware, 0)
    #ElongationCycleSeparatedFourEnz_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoStepsWB2_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoWB2_W1(hardware, 0)
    # start=time.time()
    # for i in range(int(2000/12.5)):
    #     print(i*12.5)
    #     multiDispensePumps(hardware,[12.5,12.5])
    # print(time.time()-start)

    #ElongationCycle_TwoEnz_TwoDB(hardware, 0)
    #ElongationCycle_TwoEnz_4IncEBTime_W1(hardware, 0)
    #ElongationCycle_TwoEnz_EDTAspike_FourIncW1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_DispCheck(hardware, 0)
    #ElongationCycle_TwoEnz_TwoW1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_Reprime_DiffVol(hardware, 1)
    #ElongationCycle_TwoEnz_W1_96in384(hardware, 1)
    #ElongationCycle_TwoEnz_2DiffWB2_2StepsWB2_W1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_AceticAcidCapping(hardware, 0)
    #ElongationCycle_TwoEnz_EndedWellsCR0_hardocded_W1(hardware, 0)
    #Testing_384(hardware,0)
    ElongationCycle_TwoEnz_W1_DBactiveWells_ReprimeNucs_Oended(hardware,0)


