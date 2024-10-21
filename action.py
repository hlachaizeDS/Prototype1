import datetime

from hardware import *
from PSPs import *
import sys


thermal_is384 = 0

def actionButton_Callback(directCommand):
    hardware = directCommand.parent.hardware

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



