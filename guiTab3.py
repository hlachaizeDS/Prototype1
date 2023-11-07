# On importe Tkinter
import threading
from tkinter import *
from hardware import *
from action import actionButton_Callback
import TMCL
from cycles_steps import *
from PSPs import *
from guiTab1 import arduinoHeating_Callback



class MainFrameTab3(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        '''Hardware(motors,Leds,...)'''
        #self.hardware = HardWare(self)

        #Title
        self.titleLabel = Label(self, text="OligoPrint Soft",justify="center")
        self.titleLabel.grid(row=1, columnspan=2)

        '''Only one frame so far'''
        self.middleFrame=MiddleFrame(self)
        self.middleFrame.grid(row=2,column=2)

class MiddleFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #print(self.parent.parent.tab(1))
        hardware = self.parent.parent.children['!mainframetab1'].hardware

        # Priming Premix
        self.initAllFirstButton = Button(self, text="Init All Pumps", command=lambda: hardware.init_all_du())
        self.initAllFirstButton.grid(row=1, column=1, padx=30, pady=5)

        # Priming premix
        self.PrimingPremixButton = Button(self, text="Prime PSP (MN 2.5mL Buffers 5mL)",
                                             command=lambda: multiDispensePumps(hardware,[2500,2500,0,0,0,0,5000,5000,5000]))
        self.PrimingPremixButton.grid(row=2, column=1, padx=30, pady=5)

        # Priming premix
        self.PrimingPremixButton = Button(self, text="Prime PSP (MN 2.5mL)",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [2500, 2500, 0, 0, 0, 0, 0,
                                                                              0, 0]))
        self.PrimingPremixButton.grid(row=3, column=1, padx=30, pady=5)

        # Priming premix
        self.PrimingPremixButton = Button(self, text="Prime PSP (Buffers 5mL)",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [0, 0, 0, 0, 0, 0, 5000,
                                                                              5000, 5000]))
        self.PrimingPremixButton.grid(row=4, column=1, padx=30, pady=5)

        # Rinse all buffs
        self.primingAllWashesButton = Button(self, text="Rinse All Buffers 40mL",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [0, 0, 0, 0, 0, 0, 40000, 40000, 40000]))
        self.primingAllWashesButton.grid(row=5, column=1, padx=30, pady=5)

        # Rinse PSP buffs
        self.primingAllWashesButton = Button(self, text="Rinse PSP buffers 10mL",
                                             command=lambda: multiDispensePumps(hardware,
                                                                                [10000, 10000, 0, 0, 0, 0, 10000, 10000,
                                                                                 10000]))
        self.primingAllWashesButton.grid(row=6, column=1, padx=30, pady=5)

        # Rinse PSP buffs
        self.primingAllWashesButton = Button(self, text="Rinse MN 10mL",
                                             command=lambda: multiDispensePumps(hardware,
                                                                                [10000, 10000, 0, 0, 0, 0, 0, 0,
                                                                                 0]))
        self.primingAllWashesButton.grid(row=7, column=1, padx=30, pady=5)

        # Rinse PSP buffs
        self.primingAllWashesButton = Button(self, text="Rinse Buffers 10mL",
                                             command=lambda: multiDispensePumps(hardware,
                                                                                [0, 0, 0, 0, 0, 0, 10000, 10000,
                                                                                 10000]))
        self.primingAllWashesButton.grid(row=8, column=1, padx=30, pady=5)

        #Arduino Heating
        self.arduinoHeating_value = IntVar()
        self.arduinoHeating = Checkbutton(self, text="Heating (put manually manifold at 60°C)",
                                                   command=lambda : arduinoHeating_Callback(self),
                                                   indicatoron=0, variable=self.arduinoHeating_value)
        self.arduinoHeating.grid(row=0,column=6,padx=5,pady=5)

        '''Vent And Vacuum'''
        self.ventOffVacOnButton = Button(self, text="Start Vac",
                                 command=lambda: ventOffVacOn_Callback(hardware))
        self.ventOffVacOnButton.grid(row=3, column=3, padx=30, pady=5)

        self.ventOnVacOffButton = Button(self, text="Stop Vac",
                                         command=lambda: ventOnVacOff_Callback(hardware))
        self.ventOnVacOffButton.grid(row=4, column=3, padx=30, pady=5)

        '''stirring'''
        self.stirButton = Button(self, text="High Stir 5s",
                                 command=lambda: waitAndStir(hardware, 5, 360))
        self.stirButton.grid(row=5, column=3, padx=30, pady=5)

        '''Go To Positions'''
        ##Go To Safe position
        self.safeButton = Button(self, text="Safe Pos",
                                        command=lambda: goToWell(hardware, 'safe', 1, 0))
        self.safeButton.grid(row=9, column=1, padx=30, pady=5)

        '''Variable volume Block'''

        ##Entry
        self.volumeToDisp_value = StringVar()
        self.volumeToDisp=Entry(self,textvariable=self.volumeToDisp_value)
        self.volumeToDisp.grid(row=1,column=5)
        self.volumeToDisp_value.set('25')


        self.multidispMNButton = Button(self, text="MN",
                                            command=lambda: multiDispensePumps(hardware, [float(self.volumeToDisp_value.get()) for i in range(2)]+[0,0,0,0,0,0,0]))
        self.multidispMNButton.grid(row=4, column=5, padx=5, pady=5)

        channelList=['M', 'N', 'DB','BB','Buff1']
        dividerList=[1,1,1,1,1,1,4,4,4]
        self.bufferButton = [None] * len(channelList)
        for buffer in channelList:
            self.bufferButton[channelList.index(buffer)] = Button(self, text=buffer, command=lambda buffer=buffer: multiDispensePumps(hardware,disp_pattern(channelList.index(buffer),float(self.volumeToDisp_value.get())*dividerList[channelList.index(buffer)]) ))
            self.bufferButton[channelList.index(buffer)].grid(row=5 + channelList.index(buffer),column=5,padx=5, pady=5)

        self.initButton= Button(self, text='Init', command=lambda : hardware.init_du(int(self.volumeToDisp_value.get())))
        self.initButton.grid(row=5 + channelList.index(buffer) + 1,column=5,padx=5, pady=5)

        self.initAllButton = Button(self, text='Init All',
                                 command=lambda: hardware.init_all_du())
        self.initAllButton.grid(row=5 + channelList.index(buffer) + 2, column=5, padx=5, pady=5)

        self.PSPWashesButton = Button(self, text="PSP_standard", command=lambda: PSPWashes_96OP_standard(hardware, 0))
        self.PSPWashesButton.grid(row=13, column=8, padx=5, pady=5)
        self.PSPWashesButton2 = Button(self, text="PSP_AV", command=lambda: PSPWashes_96OP_AV(hardware, 0))
        self.PSPWashesButton2.grid(row=14, column=8, padx=5, pady=5)
        ##Entry
        # self.timeToDisp_value = StringVar()
        # self.timeToDisp = Entry(self, textvariable=self.timeToDisp_value)
        # self.timeToDisp.grid(row=1, column=6)
        # self.timeToDisp_value.set('0.1')

        # buffersList = ['DB', 'BB', 'Buff1', 'Buff2']
        # self.bufferButton = [None] * len(buffersList)
        # for buffer in buffersList:
        #     self.bufferButton[buffersList.index(buffer)] = Button(self, text=buffer,
        #                                                           command=lambda buffer=buffer: dispense(hardware,
        #                                                                                                  buffer, float(
        #                                                                   self.timeToDisp_value.get())))
        #     self.bufferButton[buffersList.index(buffer)].grid(row=2 + buffersList.index(buffer), column=6, padx=5,
        #                                                       pady=5)


'''CALLBACK FUNCTIONS'''

def primerBuffer_Callback(hardware,solution):
    #Primer for 10s selected buffer, then dispense 0.1s

    dispense(hardware,solution,10)
    sleep(1)
    dispense(hardware,solution,0.05)


def vent_Callback(middleFrame,hardware):
    #Vents for 10s

    hardware.vacValveOpen()
    wait(hardware, 7)
    hardware.vacValveClose()

    #hardware.set_output(7, 1)
    #wait(hardware, 10)
    #hardware.set_output(7, 0)

def ventOffVacOn_Callback(hardware):
    if hardware.extraVentilation:
        hardware.set_output(1, 1)
    hardware.vacValveOpen()

def ventOnVacOff_Callback(hardware):
    if hardware.extraVentilation:
        hardware.set_output(1, 0)
    hardware.vacValveClose()

def hitPrimingPremix_Callback(hardware):

    secondsToPrime=15
    stroke=0.15 #seconds
    for i in range(int(secondsToPrime/(stroke*2))):
        multiDispense(hardware,[1,1,1,1],stroke)
        sleep(stroke)

def bufferButton_Callback(directCommand,i):
    #Turns on and off digital Ouputs
    value = directCommand.digitalOutputButton_value[i].get()
    directCommand.parent.hardware.set_output(i, value)

def goToColumn_Callback(MiddleFrame,hardware,buffer):
    colToGo=int(MiddleFrame.colToGo_value.get())
    goToWell(hardware,buffer,(colToGo-1)*4+1,0)
    MiddleFrame.colToGo_value.set(colToGo+1)



def disp_pattern(id,vol):
    pattern=[0,0,0,0,0,0,0,0,0]
    pattern[id]=vol

    return pattern
'''CALLBACKS FOR LEFT FRAME'''

if __name__ == "__main__":
    # On crée la racine de notre interface
    root = Tk()
    MainFrame(root).pack()
    root.mainloop()
