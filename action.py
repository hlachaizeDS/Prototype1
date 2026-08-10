from hardware import *
import sys
from PSPs import *


thermal_is384 = 0

def actionButton_Callback(directCommand):


    hardware=directCommand.parent.hardware

    #PDR
    PDR_Synthesis_TwoEnz_TwoDB_Xop(hardware, 0) #comparaison DB
    #PDR_OneEnz_EightNucs_Xbuff2(hardware, 0) #comparaison DMSO
    #PDR_Synthesis_TwoDiffEnzMN_Xbuff2(hardware, 0) #comparaison Tdt
    #PDR_Synthesis_OneEnz_TwoWB2_Xop(hardware, 0) #comparaison WB2

    #THE ONLY ONE
    #Synthesis_TwoEnz_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_Xop(hardware, 0)
    #Synthesis_TwoEnz_Xq(hardware, 0)
    #Synthesis_TwoEnz_Xbb(hardware, 0)
    #Synthesis_TwoEnz_Degenerate_Xop(hardware, 0)

    # ONE ENZYME
    #ElongationCycleSeparatedOneEnz(hardware,0)
    #ElongationOneEnz_10minSomeCycles(hardware, 0)
    #ElongationCycle_OneEnz_W1_10minSomeCycles(hardware, 0)
    #ElongationCycle_OneEnz_W1_10minSomeCycles_NoLastDB(hardware, 0)
    #ElongationCycle_OneEnz_EndedN_W1(hardware, 0)

    # TWO ENZYMES
    #ElongationCycleSeparatedTwoEnz(hardware, 1)
    #ElongationTwoEnz_10minSomeCycles(hardware, 0)
    #ElongationCycle_TwoEnz_W1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_4diffWB_end(hardware, 0)
    #ElongationCycle_TwoEnz_W1_X(hardware, 0)
    #ElongationCycle_TwoEnz_noMN_W1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_10minsomeCycles(hardware, 0)
    #ElongationCycleSeparatedTwoEnzDBactive(hardware, 0)
    #ElongationCycle_TwoEnz_W1_CR0inX(hardware, 0)

    # FOUR ENZYMES
    #ElongationCycleSeparatedFourEnz(hardware, 0)
    #ElongationCycleSeparatedFourEnz_B4(hardware, 0)
    #ElongationCycleSeparatedFourEnz_W1_X(hardware, 0)

    # RNA
    #RNAProcess(hardware,0)

    # MISC HENRI
    #for i in range(5000//25):
    #    print(str(i*25))
    #    multiDispensePumps(hardware,[0,0,0,25,0,0])
    #PoolTest(hardware, 0)
    #multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,0,200])
    #start=time()
    #multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,1000])
    #end=time()
    #print("DB:" + str(end-start))
    #start = time()
    #multiDispensePumps(hardware, [0, 0, 0, 0, 0, 0, 0, 0, 0,1000])
    #end = time()
    #print("BB:" + str(end - start))
    #Synthesis_TwoEnz_Inkjetbaseperbase(hardware, 0)
    #multi_dispense_in_wells_degenerate(hardware,{"A":[[200,25,200,25],[1,9,17,25]]},0,None,0,1)
    #Synthesis_Laura_Dismutase_2D(hardware, 0)

    # ELONG MIX
    #Synthesis_FourEnz_Xbuff2(hardware, 0)
    #OneEnz_Xn_W1(hardware, 0)
    #TwoEnz_IncubEmpty(hardware, 0)
    #FourEnz_TwoElongTime2m4m(hardware, 0)
    #TwoDiffNucs(hardware,0)
    #TwoEnz_TwoElongTime2m4m(hardware, 0)
    #TwoElongTime_TwoWB2(hardware, 0)
    #TwoElongTime_Col_TwoWB2(hardware, 0)
    #TwoEnz_FourElongTime(hardware, 0)
    #ElongationCycle_OneEnz_EndedWellsWash_Long(hardware, 0)
    #ElongationCycle_TwoEnz_TwoDB_EBDBVol_W1(hardware, 0)
    #ElongationCycle_EnzviaQ(hardware, 0)
    #ElongationCycle_TwoEnz_FourDiffVolEnz(hardware, 0)
    #ElongationCycle_TwoDiffEnz_TwoDiffWB1_TwoDiffWB2_W1(hardware, 0)
    #ElongationCycleSeparatedFourEnzQ(hardware, 0)
    #OneEnz_EightNucs_W1_X(hardware, 0)
    #OneEnz_EightNucs_TwoDB_W1(hardware, 0)
    #OneEnz_EightNucs_ElongTime_W1_X(hardware, 0)
    #OneEnz_EightNucs_ElongVol_ElongTime_W1(hardware, 0)
    #OneEnz_TwelveNucs_TwoDiffWB2_W1_X(hardware, 0)
    #OneEnz_EightNucs_W1_2DB(hardware, 0)
    #OneEnz_EightNucs_W1_2WB2_W1X(hardware, 0)
    #ElongationCycleSeparatedFourEnzQ_X(hardware, 0)
    #ElongationCycle_OneEnz_W1_2WB2_ON(hardware, 0)
    #FourEnz_DiffVol_W1_X(hardware, 0)
    #OneEnz_DiffVolCol_W1_X(hardware, 0)
    #TwoEnz_DiffVolCol_W1_X(hardware, 0)
    #Synthesis_TwoEnz_4EBIncTime_X(hardware, 0)
    #Synthesis_TwoEnz_4EBIncTime_ExtraPK_Xq(hardware, 0)
    #FourEnz_TwoDB_W1_X(hardware, 0)
    #Synthesis_OneEnz_EightNucs_4ElongTime_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_EBTime_TwoWB1_Xop(hardware, 0)


    # WB1
    #ElongationCycle_OneEnz_W1_PKDifferentPercent(hardware, 0)
    #ElongationCycle_OneEnz_DiffFourW1_2stepsWB2_X(hardware, 0)
    #ElongationCycle_OneEnz_FourDiffWB1_OneStepDB_TwoStepsWB2_W1(hardware, 0)
    #ElongationCycle_OneEnz_DiffFourW1(hardware, 0)
    #ElongationCycle_OneEnz_DiffFourW1_XtraWash(hardware, 0)
    #ElongationCycle_OneEnz_DiffFourW1_3IncW1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_TwoDiffW1(hardware, 0)
    #ElongationCycle_TwoDB_TwoWB1(hardware,0)
    #ElongationCycle_FourW1(hardware, 0)
    #ElongationCycle_TwoDiffEnz_TwoDiffW1(hardware, 0)
    #ElongationCycle_TwoEnz_EDTAspike_FourIncW1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoWB1_OneStepDB_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoVolFourDiffWB1_W1X(hardware, 0)
    #ElongationCycle_TwoDiffEnz_TwoDiffWB1_TwoDiffDB_W1(hardware, 0)
    #ElongationCycle_TwoDiffEnz_TwoDiffWB1_TwoDiffWB2_W1(hardware, 0)
    #FourEnz_TwoDiffWB1_EndedWellsCR0(hardware, 0)
    #ElongationCycle_TwoEnz_W1_TwoDiffW1_X(hardware, 0)
    #Synthesis_EightDiffWB1_X(hardware, 0)
    #Synthesis_TwoEnz_EBTime_TwoWB1_Xop(hardware, 0)



    # DB
    #ElongationCycle_TwoDB_TwoWB2(hardware,0)
    #ElongationCycle_TwoDB_TwoWB1(hardware,0)
    #ElongationCycle_OneEnz_TwoDB_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoDB_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoDBpart_W1_X(hardware, 0)
    #ElongationCycle_TwoEnz_TwoDB_HalfPlateLessVol_W1(hardware, 0)
    #ElongationCycle_FourDB_W1(hardware,0)
    #ElongationCycle_TwoWB2_FourDB(hardware, 0)
    #ElongationCycle_TwoEnz_4IncubTimeDB1_W1(hardware, 0)
    #ElongationCycle_TwoEnz_4onlyDB1Time_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoWB1_OneStepDB_W1(hardware, 0)
    #ElongationCycle_OneEnz_FourDB_W1(hardware, 0)
    #ElongationCycle_TwoEnz_W1_OnlyOneDB(hardware, 0)
    #ElongationCycle_TwoEnz_TwoDB_EBDBVol_W1(hardware, 0)
    #ElongationCycle_TwoDiffEnz_TwoDiffWB1_TwoDiffDB_W1(hardware, 0)
    #ElongationCycle_OneEnz_FourDiffWB1_OneStepDB_TwoStepsWB2_W1(hardware, 0)
    #OneEnz_EightNucs_W1_2DB(hardware, 0)
    #Synthesis_TwoEnz_OneStepDB_FourTimeDB_X(hardware, 0)
    #Synthesis_OneEnz_TwoWB1_OneStepTwoDB_ThreeTimeDB_Xbuff2(hardware, 0)
    #Synthesis_OneEnz_TwoWB1_TwoDB_ThreeTimeDB1_Xbuff2(hardware, 0)
    #FourEnz_TwoDB_W1_X(hardware, 0)
    #ElongationCycle_TwoEnz_TwoDB_Xop(hardware, 0) #comparaison DB (old code)
    #Synthesis_OneEnz_2DB_Xbuff2_Rev(hardware, 0)


    # WB2
    #ElongationCycle_TwoDB_TwoWB2(hardware,0)
    #ElongationCycle_TwoWB2_FourDB(hardware, 0)
    #ElongationCycle_TwoElongTime_TwoWB2_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoWB2_X(hardware, 0)
    #ElongationCycle_TwoEnz_TwoWB2(hardware, 0)
    #ElongationCycle_TwoEnz_TwoStepsWB2FourVol_W1(hardware, 0)
    #ElongationCycle_TwoEnz_TwoStepsWB2_W1(hardware, 0)
    #ElongationCycle_OneEnz_FourdiffWB2_W1_X(hardware, 0)
    #ElongationCycle_OneEnz_FourdiffWB2_2stepsWB2_W1_X(hardware, 0)
    #ElongationCycle_TwoEnz_2DiffWB2_2WB2Steps_W1(hardware, 0)
    #ElongationCycle_OneEnz_DiffFourW1_2WB2(hardware, 0)
    #ElongationCycle_OneEnz_FourDiffWB1_OneStepDB_TwoStepsWB2_W1(hardware, 0)
    #ElongationCycle_TwoEnz_plus48cyWB2_W1(hardware, 0)
    #ElongationCycle_DiffEnz_TwoWB2_X(hardware, 0)
    #FourEnz_TwoWB2_X(hardware, 0)
    #ElongationCycle_OneEnz_FourdiffWB2_W1_2DB(hardware, 0)

    #PSP
    #PSPWashes_noDBquad_HT_extraWaterTimeAndEth_Buff2(hardware, 0)
    #PSPWashes_96OP_extraH20andEtOH_Input(hardware, 0)
    #PSPWashes_96OP_extraH20andEtOH_extraH2O30min(hardware, 0)
    #PSPWashes_96OP_extraH20andEtOH_IsoTime_EthConc(hardware, 0)
    #PSPWashes_96OP_extraH20andEtOH_pKlonger(hardware, 0)

    #MISC
    #ElongationCycle_TwoEnz_W1_VolScreenPerStep(hardware, 0)
    #ElongationCycle_TwoEnz_24Ended_W1(hardware, 0)
    #ElongationCycle_TwoEnz_EndedWellsCR0_hardocded_W1(hardware, 0)
    #OneEnz_ExtraWash30cycles_W1X(hardware, 0)
    #multi_dispense_in_wells(hardware,{"Q":[25,wellListFromColumns([1])]},0)
    #ElongationCycleTwoEnz_W1_DiffVols_X(hardware, 0)
    #ElongationCycleTwoEnz_W1_DiffVols_pause50cycles_X(hardware, 0)


    #Synthesis_TwoEnz_HalfVol_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_Xbuff2_RevTest(hardware, 0)
    #Synthesis_DiffVolCol_X(hardware, 0)
    #Synthesis_TwoDB_DiffVolCol_X(hardware, 0)
    #Synthesis_TwoEnz_TwoDB_TwoX(hardware, 0)
    #Synthesis_TwoEnz_TwoDB_X(hardware, 0)
    #Synthesis_FourEnz_TwoDB_X(hardware, 0)
    #Synthesis_FourEnz_Xbuff2(hardware, 0)
    #Synthesis_OneEnz_FourWB1_TwoWB2_X(hardware, 0)
    #Synthesis_OneEnz_FourWB1_XtraWash_X(hardware, 0)
    #Synthesis_DiffVolCol_DoubleWB2_XPK_Xbuff2(hardware, 0)
    #Synthesis_FourEnz_TwoWB1_Xq(hardware, 0)
    #Synthesis_FourEnz_TwoWB2_Xq(hardware, 0)
    #Synthesis_ThreeEnzMixed_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_TwoWB1_2xWB2_Xq(hardware, 0)
    #Synthesis_TwoEnz_ROPtest_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_TwoWB1_DB1Time_Xop(hardware, 0)
    #Synthesis_OneEnz_FourWB2_Xbuff2(hardware, 0)
    #Synthesis_OneEnz_TwoWB1_FourWB2_Xbuff2(hardware, 0)
    #Synthesis_FourEnz_TwoWB1_TwoWB2(hardware, 0)
    #Synthesis_ThreeEnz_TwoWB1_TwoWB2_Xq(hardware,0)
    #Synthesis_TwoEnz_TwoWB1_TwoWB2_Xq(hardware, 0)
    #Synthesis_TwoEnz_4ElongTime_Xbuff2(hardware, 0)
    #Synthesis_FourEnz_TwoDB_Xq(hardware, 0)
    #Synthesis_Inkjet_Tblshoot(hardware, 0)
    #Synthesis_TwoEnz_ThreeElongTime_ThreeWB2_Xq(hardware, 0)
    #Synthesis_TwoEnz_ThreeWB2_Xq(hardware, 0)
    #Synthesis_TwoEnz_ThreeWB2_Xop(hardware, 0)
    #Synthesis_OneEnz_FiveDB_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_TwoWB2_2G_Xop(hardware, 0)
    #Synthesis_TwoEnz_ThreeWB1_Xop(hardware, 0)
    #Synthesis_TwoEnz_IncVol_Xbuff2(hardware, 0)
    #Synthesis_TwoEnz_RedVol_Xbuff2(hardware, 0)
    #Synthesis_TwoDiffEnz_LongWB1_Xbuff2(hardware, 0)
    #Synthesis_FourEnz_TwoDB_Xq(hardware, 0)
    #Synthesis_TwoEnz_TwoG_Xbuff2(hardware,0)
    #Synthesis_InkjetB5_TwoG_Xbuff2(hardware, 0)
    #Synthesis_OneEnz_FiveWB2_Xbuff2(hardware, 0)
    #Synthesis_TwoEnzCrossed_Xbuff2(hardware, 0)