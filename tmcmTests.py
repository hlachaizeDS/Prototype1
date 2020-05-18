
from serial import Serial
from time import sleep
import TMCL

## serial-address as set on the TMCM module.
MODULE_ADDRESS = 1

## Open the serial port presented by your rs485 adapter
serial_port = Serial("COM3")

## Create a Bus instance using the open serial port
bus = TMCL.connect(serial_port)

## Get the module
motor = bus.get_motor(MODULE_ADDRESS,4)

## From this point you can start issuing TMCL commands
## to the motor as per the TMCL docs. This example will
## rotate the motor left at a speed of 1234 for 2 seconds

##LED
##Allume la led puis l'éteint
bus.send(1,14,2,2,1)
sleep(2)
bus.send(1,14,2,2,0)

##Motor
res=motor.rotate_right(1234)
print(res)
sleep(2)
motor.stop()