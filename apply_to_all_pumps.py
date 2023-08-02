from DispenseBlock_RS485 import *

disp_block=DispenseBlock('FP')

for du in disp_block.dus:
    if du.address in [1,2,3,4,5,6,7,8,9,10,11,12]:
        print(du.address)
        du.bus.send(du.address,9,65,0,7) #send 0 for 9600, 7 fpr 115200
