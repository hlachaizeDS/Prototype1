import os
from DispenseBlock_USB import *

disp_block=DispenseBlock_USB('FP')

pump_list=["M","N","A","C","G","T","O","P","DB","BB","Buff1","Buff2"]

pump_to_update=["M"]

for du in disp_block.dus:
    pump=pump_list[disp_block.dus.index(du)]
    if pump in pump_to_update:
        print(pump)
        os.system('ls C:\Users\SynthesisDNASCRIPT\DNA Script\SO - Synthesis Operations - Bibliothèque\Utilities\Instrumentation\Pumps_Control1161\Firmwares\pilotage pompe _V1A-v3.2 - Test.tmc')
