import datetime

from hardware import *
from PSPs import *
import sys


thermal_is384 = 0

def actionButton_Callback(directCommand):
    hardware = directCommand.parent.hardware

    #PDR
    #PDR_Synthesis_TwoEnz_TwoDB_X(hardware,0)

    #384------------------
    #ElongationCycle_TwoEnz_W1_384(hardware)
    #ElongationCycle_TwoEnz_W1_384_2and3minElong(hardware)
    #ElongationCycle_TwoEnz_W1_384_Buff2attheEnd(hardware)
    #ElongationCycle_TwoEnz_W1_384_WB2forSubs(hardware)
    #ElongationCycle_TwoEnz_W1_384_LowDensityLowScale(hardware)

    #96-------------------
    #EB

    #WB1

    #DB

    #WB2

    #Misc
    #take_snapshot(hardware,"Newheater")

    #ElongationTwoEnz_HighScale_10minSomeCycles(hardware, 0)
    #ElongationCycleSeparatedFourEnz_B4(hardware, 0)
    #ElongationCycle_TwoEnz_W1(hardware, 0)
    #ElongationCycle_OneEnz_W1(hardware, 0)
    #ElongationCycle_TwoEnz_W1X(hardware, 0)
    #ElongationCycle_OneEnz_W1X(hardware, 0)
    #ElongationCycle_TwoEnz_W1X_preprimenucs(hardware, 0)
    #ElongationCycle_TwoEnz_W1_TwoWB2(hardware,0)
    #ElongationCycle_TwoEnz_W1_384_WB2Screen(hardware, 1)
    #ElongationCycle_TwoEnz_W1_Buff2atTheEnd_DiffVol(hardware, 0)
    #ElongationCycle_TwoEnz_W1_TR102030(hardware, 0)
    #ElongationCycle_TwoEnz_TwoW1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_synthesisIssue(hardware, 0)
    #ElongationCycle_TwoEnz_W1_CloggingFJ8504(hardware, 0)
    #ElongationCycle_TwoEnz_W1_PSPTblsht(hardware, 0)
    #ElongationCycle_TwoEnz_W1_10minsomeCycles(hardware, 0)
    #ElongationCycle_OneEnz_W1_X(hardware, 0)
    #ElongationCycle_OneEnz_W1_10minsomeCycles(hardware, 0)
    #ElongationCycleSeparatedFourEnz_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoStepsWB2_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoWB2_W1(hardware, 0)
    # start=time.time()

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
    #ElongationCycle_TwoEnz_W1_ReprimeNucs_Oended(hardware,0)
    #ElongationCycle_TwoEnz_W1_long_mutants_dI(hardware,0)
    #ElongationCycle_TwoEnz_W1_long_diffVolumes(hardware, 0)
    #ElongationCycle_TwoEnz_2DiffWB2_2volEB_1DB_W1_EndedWellsCR0(hardware, 0)
    #ElongationCycleTwoEnz_W1_DiffVols_X(hardware, 0)
    #ElongationCycleOneEnz_EightNucs_W1_X(hardware, 0)
    #TwoElongTime_Col_TwoWB2(hardware, 0)
    #ElongationCycle_TwoEnz_TwoStepsWB2_2DB_W1(hardware, 0)

    #ElongationCycle_TwoEnz_W1_10minsomeCycles(hardware, 0)


    #Synthesis_TwoEnz(hardware, 0)
    #Synthesis_TwoEnz_X(hardware, 0)
    #Synthesis_TwoEnz_Xp(hardware, 0)
    #Synthesis_TwoEnz_Xp_AVPrimingO(hardware, 0)
    #Synthesis_TwoEnz_TwoDB_X(hardware, 0)
    #Synthesis_TwoEnz_FourIncWB1_X(hardware, 0)
    #Synthesis_FourEnz_TwoDB_X(hardware, 0)
    #Synthesis_TwoEnz_TwoDB_TwoWB2x2_LastWB2_X(hardware, 0)
    #Synthesis_TwoEnz_TwoWB1_ExtraWB1_X(hardware, 0)
    #Synthesis_OneEnz_FourWB1_ExtraPkWash_X(hardware, 0)
    #multi_dispense_in_wells(hardware,{"Q": [50, [well for well in wellListFromColumns([1,2,3,4,5,6,7,8,9,10,11,12])]]})


    #PSPs
    #PSPWashes_96OP_extraH20andEtOH(hardware,0)
    #PSPWashes_96OP_extraH20andEtOH_Soft(hardware,0)
    #PSPWashes_96OP_extraH20andEtOH_half(hardware,0)
    #PSPOnePot_384_4LBs(hardware, 1)



