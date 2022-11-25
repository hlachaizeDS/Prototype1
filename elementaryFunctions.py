from time import sleep
import time
import math

X_A1=149601
Y_A1=37733

X_step=9200
Y_step=9150

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

    'Positions of A1 with the M nozzle'
    #X_1 = 88822
    #Y_1 = 10518
    X_1 = X_A1
    Y_1 = Y_A1

    if quadrant==1:
        X_1=X_1-int(X_step/4)
        Y_1=Y_1-int(Y_step/4)
    if quadrant==2:
        X_1 = X_1 + int(X_step/4)
        Y_1 = Y_1 - int(Y_step/4)
    if quadrant==3:
        X_1 = X_1 - int(X_step/4)
        Y_1 = Y_1 + int(Y_step/4)
    if quadrant==4:
        X_1 = X_1 + int(X_step/4)
        Y_1 = Y_1 + int(Y_step/4)

    positions_dict= {
        "M": [0, 0],
        "N": [1, 0],
        "O": [2, 0],
        "P": [3, 0],
        "Q": [4, 0],
        "A": [2, 1],
        "C": [3, 1],
        "G": [4, 1],
        "T": [5, 1],
        "DB": [6, -1],
        "BB": [6, 0],
        "Buff1": [6, 1],
        "Buff2": [6, 2],
    }

    if element in positions_dict.keys():
        X_1=X_1 - positions_dict[element][0]*X_step
        Y_1=Y_1 - positions_dict[element][1]*Y_step


    if element=='safe':
        X_1 = 0
        Y_1 = 131379

    if element=='thermo':
        X_1=0
        Y_1=131379

    if element == "thermalCamera":
        X_1 = 0
        Y_1 = 131379

    if element == "washPrime":
        #X_1 = 167686
        X_1=224963
        Y_1 = 0

    if element == "premixPrime":
        X_1 = 0
        Y_1 = 0

    X = X_1 + ((well - 1) % 8) * X_step
    Y = Y_1 + ((well - 1) // 8) * Y_step
    hardware.xMotor.move_absolute(X)
    hardware.yMotor.move_absolute(Y)
    sleep(0.4)

    while hardware.xMotorParametersInterface.get(8) == 0 or hardware.yMotorParametersInterface.get(8) == 0:
        hardware.parent.update()
        sleep(0.2)

def goToFakeWell(hardware,fake_well,fake_plate_dims,dispHead_dims,quadrant):

    #Works only for the upper left nozzle

    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    'We make sure the needles are up'
    #'needlesGoUp(hardware)

    'Positions of A1 with the up left Lee vann'
    X_1 = X_A1 - ((dispHead_dims[0] - 1)*X_step)
    Y_1 = Y_A1 - ((dispHead_dims[1] - 1)*Y_step)

    if quadrant == 1:
        X_1 = X_1 - int(X_step / 4)
        Y_1 = Y_1 - int(Y_step / 4)
    if quadrant == 2:
        X_1 = X_1 + int(X_step / 4)
        Y_1 = Y_1 - int(Y_step / 4)
    if quadrant == 3:
        X_1 = X_1 - int(X_step / 4)
        Y_1 = Y_1 + int(Y_step / 4)
    if quadrant == 4:
        X_1 = X_1 + int(X_step / 4)
        Y_1 = Y_1 + int(Y_step / 4)

    X = X_1 + ((fake_well - 1) % fake_plate_dims[0]) * X_step
    Y = Y_1 + ((fake_well - 1) // fake_plate_dims[0]) * Y_step
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

def fake_plate_well_to_real_well(fake_plate_well, fake_plate_dims, dispHead_dims):

    column=(fake_plate_well-1)//fake_plate_dims[0] + 1
    row=(fake_plate_well-1)%fake_plate_dims[0] + 1

    middle_row=fake_plate_dims[0]/2
    real_rows=[middle_row-3,middle_row-2,middle_row-1,middle_row,middle_row+1,middle_row+2,middle_row+3,middle_row+4]

    middle_col=fake_plate_dims[1]/2
    real_cols= [middle_col-5,middle_col-4,middle_col-3,middle_col-2,middle_col-1,middle_col,
                middle_col+1,middle_col+2,middle_col+3,middle_col+4,middle_col+5,middle_col+6]

    if row not in real_rows or column not in real_cols: #When the plate well is outside the range of realwells
        return 0

    realWell=(column - (dispHead_dims[1]-1) - 1 )*8 + row - (dispHead_dims[0]-1)

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
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    hardware.magnetMotor.move_absolute_wait(hardware, -1706249)

def magnetGoDown(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    hardware.magnetMotor.move_absolute_wait(hardware, -642511)

def pressureGoDown(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    hardware.posPressure.goDown('dessalt')

def pressureGoUp(hardware):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return
    hardware.posPressure.goUp()

def aspirate(hardware,time):
    if hardware.parent.directCommand.stopButton_value.get()==1:
        return

    output=7 #output for vacuum
    hardware.set_output(output, 1)
    sleep(time)
    hardware.set_output(output, 0)



def multiDispensePumps(hardware,volumes):


    volumes=volumes.copy()
    if len(volumes)!=12:
        volumes.extend([0]*(12-len(volumes)))

    for pump_id in range(12):
        hardware.dus[pump_id].dispense(volumes[pump_id])

    #wait for being able to move
    for pump_id in range(12):
        hardware.dus[pump_id].wait_for_canMove()


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

if __name__ == "__main__":
    for well in range(1,50):
        print('well='+str(well))
        print(fake_plate_well_to_real_well(well,[18,14],[6,2]))