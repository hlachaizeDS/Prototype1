from hardware import *
import sys



def actionButton_Callback(directCommand):


    hardware=directCommand.parent.hardware

    #ElongationCycleSeparatedTwoEnz(hardware,0)
    #ElongationCycleSeparatedOneEnz(hardware,0)

    #ElongationCycleSeparatedTwoEnz_EvacuationTimings(hardware,1)

    #goToWell(hardware,"BB",93,1)
    #hardware.posPressure.goDown("synthesis")
    #fillPlate(hardware,"DB",50,1)
    #removeSupernatantPosPressure(hardware,"excel",0.5,"dessalt",0)
    #removeSupernatantPosPressure(hardware,list(range(1,97)),0.3,"synthesis",1)
    #goToWell(hardware,"BB",95,4)

    ElongationCycleSeparatedTwoEnz_DiffDB1Vols(hardware, 1)