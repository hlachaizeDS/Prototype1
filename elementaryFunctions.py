from time import sleep
import time
import math

def realWellToPlateWell(realWell):
    column=(realWell-1)//8
    row=(realWell-1)%8

    plateWell=column*14 + 3 + row + 1

    return plateWell

def plateWellToRealWell(plateWell):
    column=(plateWell-1)//14
    row=(plateWell-1)%14

    if row in [0,1,2,11,12,13]: #When the plate well is outside the range of realwells
        return 0

    realWell=column*8 - 3 + row + 1

    return realWell

def realWellToPlateWell6Nozzles(realWell):
    column=(realWell-1)//8
    row=(realWell-1)%8

    plateWell=column*18 + 5 + row + 1

    return plateWell

def plateWellToRealWell6Nozzles(plateWell):
    column=(plateWell-1)//18
    row=(plateWell-1)%18

    if row in [0,1,2,3,4,13,14,15,16,17]: #When the plate well is outside the range of realwells
        return 0

    realWell=column*8 - 5 + row + 1

    return realWell

def fake_plate_well_to_real_well(fake_plate_well, real_plate_dims, fake_plate_dims, dispHead_dims):

    column=(fake_plate_well-1)//fake_plate_dims[0] + 1
    row=(fake_plate_well-1)%fake_plate_dims[0] + 1

    real_rows=list(range(dispHead_dims[0],dispHead_dims[0]+real_plate_dims[0]))

    real_cols =list(range(dispHead_dims[1], dispHead_dims[1] + real_plate_dims[1]))

    if row not in real_rows or column not in real_cols: #When the plate well is outside the range of realwells
        return 0

    realWell=(column - (dispHead_dims[1]-1) - 1 )*real_plate_dims[0] + row - (dispHead_dims[0]-1)

    return realWell

def wait(hardware,timeToWait):

    timeToGoTo=time.time()+timeToWait

    while (time.time()<timeToGoTo):
        if hardware.parent.leftFrame.skipButton_value.get()==1:
            break
        hardware.parent.leftFrame.statusLabelString.set('Waiting ' + '%.1f' %(timeToGoTo-time.time()) + ' s')
        hardware.parent.update()
        sleep(0.02)

    hardware.parent.leftFrame.statusLabelString.set('StatusBar')
    hardware.parent.leftFrame.skipButton_value.set(0)

def waitAndStir(hardware,timeToWait, velocity=900):

    hardware.goToWell('thermalCamera', 1,0)

    hardware.arduinoControl.startShaking(velocity)
    #hardware.arduinoControl.startShaking(330) #RNA
    wait(hardware,timeToWait)
    hardware.arduinoControl.stopShaking()

def stirrerOnFast(hardware):
    hardware.set_output2(5,1)
    hardware.set_output2(4,1)


def stirrerOnSlow(hardware):
    hardware.set_output2(5, 1)
    hardware.set_output2(4, 0)

def stirrerStop(hardware):

    stirrerOnSlow(hardware)
    sleep(1)
    while hardware.stirrerMotorParametersInterface.get(10) == 0:
        sleep(0.05)
        hardware.parent.update()
    while hardware.stirrerMotorParametersInterface.get(10) != 0:
        sleep(0.05)
        hardware.parent.update()
    hardware.set_output2(5, 0)

def magnetGoUp(hardware):

    hardware.magnetMotor.move_absolute_wait(hardware, -1706249)

def magnetGoDown(hardware):
    hardware.magnetMotor.move_absolute_wait(hardware, -642511)

def pressureGoDown(hardware):
    hardware.posPressure.goDown('dessalt')

def pressureGoUp(hardware):
    hardware.posPressure.goUp()

def aspirate(hardware,time):

    output=7 #output for vacuum
    hardware.set_output(output, 1)
    sleep(time)
    hardware.set_output(output, 0)





if __name__ == "__main__":
    for well in range(1,50):
        print('well='+str(well))
        print(fake_plate_well_to_real_well(well,[18,14],[6,2]))