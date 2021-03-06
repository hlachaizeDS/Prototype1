from time import sleep
import time
from hardware import STIRRING_VELOCITY
import math

def initialiseMotorList(hardware,motor_list):

    '''Gets a list of motors and initialise them in parallel'''
    for motor in motor_list:
        motor.reference_search(0)

    sleep(0.6)

    nb_motors_initialised=0
    nb_motors_to_initialise=len(motor_list)

    while nb_motors_initialised != nb_motors_to_initialise:
        nb_motors_initialised=0
        for motor in motor_list:
            if motor.axis.get(8) == 1:
                nb_motors_initialised += 1

        hardware.parent.update()
        sleep(0.2)

    for motor in motor_list:
        motor.axis.set(1, 0) #We set the actual position to 0 for each motor


def goToWell(hardware,element,well,quadrant):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    '''Put Lee vann or needles 'element' at the well 'well' '''

    'We make sure the needles are up'
    #needlesGoUp(hardware)

    'Positions of A1 with the up left Lee vann'
    #X_1 = 88822
    #Y_1 = 10518
    X_1 = 89719
    Y_1 = 6023

    if quadrant==1:
        X_1=X_1-2287
        Y_1=Y_1-2300
    if quadrant==2:
        X_1 = X_1 + 2287
        Y_1 = Y_1 - 2300
    if quadrant==3:
        X_1 = X_1 - 2287
        Y_1 = Y_1 + 2300
    if quadrant==4:
        X_1 = X_1 + 2287
        Y_1 = Y_1 + 2300

    if element=='A':
        X_1=X_1
        Y_1=Y_1

    if element=='M':
        X_1=X_1+2*9150
        Y_1=Y_1

    if element=='N':
        X_1=X_1+9150
        Y_1=Y_1

    if element=='DB':
        'Positions of A1 for DB'
        X_1= X_1 - 46051
        Y_1= Y_1 - 9350

    if element=='BB':
        'Positions of A1 for wash'
        X_1 = X_1 - 45901
        Y_1 = Y_1 + 68

    if element=='Buff1':
        'Positions of A1 for Buff1'
        X_1= X_1 - 46207
        Y_1= Y_1 + 9805

    if element=='Buff2':
        'Positions of A1 for Buff2'
        X_1 = X_1 - 46207
        Y_1 = Y_1 + 19350

    if element=='safe':
        X_1 = 0
        Y_1 = 118059

    if element=='thermo':
        X_1=-1047
        Y_1=6115

    if element == "thermalCamera":
        X_1 = 0
        Y_1 = 118059

    if element == "washPrime":
        #X_1 = 167686
        X_1=182478
        Y_1 = -23027

    if element == "premixPrime":
        X_1 = 0
        Y_1 = 0

    'premixPrime'
    plateWell=realWellToPlateWell(well)

    # if element=="A":
    #     equivalent_well=plateWell
    # if element=="DB":
    #     equivalent_well=plateWell
    # if element=="BB":
    #     equivalent_well=plateWell
    # if element=="needles":
    #     equivalent_well=plateWell
    # if element=="thermo":
    #     equivalent_well=plateWell
    # if element=="thermalCamera":
    #     equivalent_well=plateWell
    # if element=='safe':
    #     equivalent_well=realWellToPlateWell(1)
    equivalent_well=plateWell

    plateX1=X_1-(3*9200)
    plateY1=Y_1

    X = plateX1 + ((equivalent_well - 1) % 14) * 9150
    Y = plateY1 + ((equivalent_well - 1) // 14) * 9200
    hardware.xMotor.move_absolute(X)
    hardware.yMotor.move_absolute(Y)
    sleep(0.4)

    while hardware.xMotorParametersInterface.get(8) == 0 or hardware.yMotorParametersInterface.get(8) == 0:
        hardware.parent.update()
        sleep(0.2)

def goToRealWell(hardware,realWell,quadrant):
    #Works only for the upper left corner vann

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    'We make sure the needles are up'
    #'needlesGoUp(hardware)

    'Positions of A1 with the up left Lee vann'
    X_1 = 89719 -(3*9200)
    Y_1 = 6023


    if quadrant==1:
        X_1=X_1-2287
        Y_1=Y_1-2300
    if quadrant==2:
        X_1 = X_1 + 2287
        Y_1 = Y_1 - 2300
    if quadrant==3:
        X_1 = X_1 - 2287
        Y_1 = Y_1 + 2300
    if quadrant==4:
        X_1 = X_1 + 2287
        Y_1 = Y_1 + 2300

    X = X_1 + ((realWell - 1) % 14) * 9200
    Y = Y_1 + ((realWell - 1) // 14) * 9150
    hardware.xMotor.move_absolute(X)
    hardware.yMotor.move_absolute(Y)
    sleep(0.2)

    while hardware.xMotorParametersInterface.get(8) == 0 or hardware.yMotorParametersInterface.get(8) == 0:
        hardware.parent.update()
        sleep(0.2)

def goToRealWell6Nozzles(hardware,realWell,quadrant):
    #Works only for the upper left corner vann

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    'We make sure the needles are up'
    #'needlesGoUp(hardware)

    'Positions of A1 with the up left Lee vann'
    X_1 = 89719 -(3*9200)
    Y_1 = 6023


    if quadrant==1:
        X_1=X_1-2287
        Y_1=Y_1-2300
    if quadrant==2:
        X_1 = X_1 + 2287
        Y_1 = Y_1 - 2300
    if quadrant==3:
        X_1 = X_1 - 2287
        Y_1 = Y_1 + 2300
    if quadrant==4:
        X_1 = X_1 + 2287
        Y_1 = Y_1 + 2300

    X = X_1 + ((realWell - 1) % 18) * 9200
    Y = Y_1 + ((realWell - 1) // 18) * 9150
    hardware.xMotor.move_absolute(X)
    hardware.yMotor.move_absolute(Y)
    sleep(0.2)

    while hardware.xMotorParametersInterface.get(8) == 0 or hardware.yMotorParametersInterface.get(8) == 0:
        hardware.parent.update()
        sleep(0.2)


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

def waitAndStir(hardware,timeToWait):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    goToWell(hardware, 'thermalCamera', 1,0)

    hardware.arduinoControl.startShaking(900)
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

'''
Old Manifold
def waitAndStir(hardware,timeToWait):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    goToWell(hardware, 'safe', 1)

    hardware.stirrerMotor.rotate_left(STIRRING_VELOCITY)
    wait(hardware,timeToWait)
    hardware.stirrerMotor.stop_wait(hardware)
    initialiseMotorList(hardware,[hardware.stirrerMotor])
'''

def magnetGoUp(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    hardware.magnetMotor.move_absolute_wait(hardware, -1706249)

def magnetGoDown(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    hardware.magnetMotor.move_absolute_wait(hardware, -642511)

def needlesGoDown(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    hardware.zMotor.move_absolute_wait(hardware,-250877)

def needlesGoUp(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    hardware.zMotor.move_absolute_wait(hardware, 9149)

def aspirate(hardware,time):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    output=7 #output for vacuum
    hardware.set_output(output, 1)
    sleep(time)
    hardware.set_output(output, 0)


def dispense(hardware,solution, time):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    # dispense for a given amount of time the right solution
    if solution=="A":
        card=1
        output=2
    if solution=="C":
        card = 1
        output=3
    if solution=="G":
        card = 1
        output=4
    if solution=="T":
        card = 1
        output=5
    if solution=="M":
        card = 1
        output=0
    if solution=="N":
        card = 1
        output=1
    if solution=="DB":
        card = 2
        output=0
    if solution=="BB":
        card=2
        output=1
    if solution=="Buff1":
        card=2
        output=2
    if solution=="Buff2":
        card=1
        output=6

    if card==1 :
        hardware.set_output(output, 1)
        sleep(time)
        hardware.set_output(output, 0)

    if card==2:
        hardware.set_output2(output, 1)
        sleep(time)
        hardware.set_output2(output, 0)


def multiDispense(hardware,nucleoArray,time):

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    for i in range(4):
        if nucleoArray[i] == 1:
            hardware.set_output(i+2, 1)
    sleep(time)
    for i in range(4):
        hardware.set_output(i+2,0)

def multiDispenseWithEnzyme(hardware,nucleoArray,time_nuc,time_enz):

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    for i in range(4):
        if nucleoArray[i+2] == 1:
            hardware.set_output(i+2, 1)
    if 1 in nucleoArray[2:6]:
        sleep(time_nuc)
    for i in range(4):
        hardware.set_output(i+2,0)

    for i in range(2):
        if nucleoArray[i] == 1:
            hardware.set_output(i, 1)
    if 1 in nucleoArray[0:2]:
        sleep(time_enz)
    for i in range(2):
        hardware.set_output(i,0)

def multiDispenseWithEnzymeSep(hardware,nucleoArray,time_nuc,time_enz_M,time_enz_N):

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    for i in range(4):
        if nucleoArray[i+2] == 1:
            hardware.set_output(i+2, 1)
    if 1 in nucleoArray[2:6]:
        sleep(time_nuc)
    for i in range(4):
        hardware.set_output(i+2,0)

    if nucleoArray[1]==1:
        hardware.set_output(1, 1)
        sleep(time_enz_N)
        hardware.set_output(1, 0)

    if nucleoArray[0]==1:
        hardware.set_output(0, 1)
        sleep(time_enz_M)
        hardware.set_output(0, 0)

def multiDispenseAether(hardware,nucleoArray,time_enz,time_A,time_C,time_G,time_T):

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    times=[time_enz,time_enz,time_A,time_C,time_G,time_T]
    for i in range(4):
        j=5-i
        if nucleoArray[j] !=0:
            hardware.set_output(j, 1)
            sleep(times[j])
            hardware.set_output(j, 0)

    for i in range(2):
        if nucleoArray[i] != 0:
            hardware.set_output(i, 1)
    if 1 in nucleoArray[0:2]:
        sleep(time_enz)
    for i in range(2):
        hardware.set_output(i,0)

def multiDispenseNACGTWithEnzyme(hardware,nucleoArray,time_nuc,time_enz):

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    for i in range(5):
        if nucleoArray[i+1] == 1:
            hardware.set_output(i+1, 1)
    if 1 in nucleoArray[1:6]:
        sleep(time_nuc)
    for i in range(5):
        hardware.set_output(i+1,0)

    for i in range(1):
        if nucleoArray[i] == 1:
            hardware.set_output(i, 1)
    if 1 in nucleoArray[0:1]:
        sleep(time_enz)
    for i in range(1):
        hardware.set_output(i,0)

def multiDispenseMNACGT(hardware,nucleoArray,time):

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    for i in range(6):
        if nucleoArray[i] == 1:
            hardware.set_output(i, 1)
    sleep(time)
    for i in range(6):
        hardware.set_output(i,0)

def dispenseInPlate(hardware):

    final=96

    for well in range(1,final+1,1):
        goToWell(hardware,'A',well)
        dispense(hardware,'A',0.02*((well%8) +1))

