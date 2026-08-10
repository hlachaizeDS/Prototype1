import datetime

from hardware import *
from PSPs import *
import sys


thermal_is384 = 0

def actionButton_Callback(directCommand):
    hardware = directCommand.parent.hardware


    #template
    #Synthesis384_TwoEnz_Xbuff2(hardware, 1)
    #Synthesis384_TwoEnz_4X12buff2(hardware, 1)
    #Synthesis_TwoEnz_Xbuff2(hardware, 0) #à vérifier
    #Synthesis_TwoEnz_Xop(hardware, 0)

    #384------------------
    #Synthesis384_TwoEnz_Xbuff2(hardware, 1)



    #PSPOnePot_384(hardware, 1)

    #96-------------------
    #EB

    #WB1

    #DB
    #Synthesis_TwoEnz_TwoDB_Xop(hardware, 0)
    #WB2



    #Synthesis_TwoEnz_Xp(hardware, 0) #a relire
    #Synthesis_FourEnz_Xbuff2(hardware, 0)
    #Humidification_Test(hardware,1)
    #Synthesis_TwoEnz_FourElongTime_Xbuff2(hardware, 0)
    #multi_dispense(hardware,{"N":40000,"O":40000,"P":40000,"Q":40000}, max_vol=12.5)
    #Synthesis384_TwoEnz_Xbuff2_1sur4(hardware, 1)
    #Synthesis384_OneEnz_SixDB_4X12S3(hardware, 1)
    #Synthesis384_OneEnz_Xbuff2(hardware, 1)
    #Synthesis384_TwoEnz_ThreeWB2_4X12q(hardware, 1)
    #Synthesis384_OneEnz_FourDB_4X12buff2(hardware, 1)
    #Synthesis384_OneEnz_FourWB2_4X12buff2(hardware, 1)
    Synthesis_OneEnz_FourDB_Xbuff2(hardware, 0)
    #for i in range(1000):
    #    print(i)
    #    multi_dispense(hardware,{"N":12.5})
    #    multi_dispense(hardware,{"N":12.5})
    #    multi_dispense(hardware,{"N":15})

    #PSPs
    #PSPWashes_96OP_extraH20andEtOH(hardware,0)
    #PSPWashes_96OP_extraH20andEtOH_Soft(hardware,0)
    #PSPWashes_96OP_extraH20andEtOH_half(hardware,0)
    #PSPWashes_96OP_extraH20andEtOH_IsoTime_EthConc(hardware, 0)
    #PSPOnePot_384_4LBs(hardware, 1)
    #PSPOnePot_384(hardware, 1)
    #usedWells=wellListFromColumns_384(list(range(1,25)))
    #multi_dispense_in_wells(hardware, {"N": [25, [well for well in usedWells if well % 8 in [1, 2]]],
     #                                  "O": [25, [well for well in usedWells if well % 8 in [3, 4]]],
     #                                  "P": [25, [well for well in usedWells if well % 8 in [5, 6]]],
     #                                  "Q": [25, [well for well in usedWells if well % 8 in [7, 0]]]
      #                                 }, 1, max_vol=12.5)


