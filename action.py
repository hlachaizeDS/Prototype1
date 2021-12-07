from hardware import *
import sys


thermal_is384 = 0

def actionButton_Callback(directCommand):


    hardware=directCommand.parent.hardware

    #ElongationCycleSeparatedTwoEnz(hardware,0)
    #ElongationCycleSeparatedOneEnz(hardware,0)


    #ElongationCycleSeparatedOneEnz_ProtK(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_ProtK(hardware, 0)

    #ElongationCycle_SpecialLong(hardware, 0)

    RNAProcess(hardware,0)

    #ElongationCycleSeparatedTwoEnz_SeveralWashes(hardware, 1)
    #ElongationCycle_HS_25ulWashes(hardware, 0)
    #ElongationCycleSeparatedOneEnz_HS_10min(hardware, 0)

    #ElongationCycle_HS_EBDBDiffVols(hardware,0)
    #ElongationCycleSeparatedTwoEnz_forDifferentSizes(hardware, 0)
    #ElongationCycle_HS_diffWashes(hardware, 0)
    #ElongationCycleSeparatedTwoEnz_forDifferentSizes_PK(hardware, 0)