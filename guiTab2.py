# On importe Tkinter
import threading
from tkinter import *
from hardware import *
from action import actionButton_Callback
from cycles_steps import *



class MainFrameTab2(Frame):
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

        # Init Pumps
        self.initAllFirstButton = Button(self, text="Init All Pumps", command=lambda: hardware.init_all_du())
        self.initAllFirstButton.grid(row=1, column=1, padx=5, pady=5)

        # Priming MNACGT
        self.PrimingPremixButton = Button(self, text="Prime MNACGT 3mL",
                                             command=lambda: multiDispensePumps(hardware,[3000]*6))
        self.PrimingPremixButton.grid(row=2, column=1, padx=5, pady=5)

        # Priming All single lines
        self.PrimingPremixButton = Button(self, text="Prime MNACGTOP 3mL",
                                          command=lambda: multiDispensePumps(hardware, [3000] * 8))
        self.PrimingPremixButton.grid(row=3, column=1, padx=5, pady=5)

        # Priming BB DB
        self.primingWashesButton = Button(self, text="Prime DB BB 5mL",
                                          command=lambda: multiDispensePumps(hardware,[0,0,0,0,0,0,0,0,5000,5000]))
        self.primingWashesButton.grid(row=4, column=1, padx=5, pady=5)

        # Priming all multi lines
        self.primingWashesButton = Button(self, text="Prime DB BB Buff1 Buff2 5mL",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [0,0,0,0,0,0,0,0,5000,5000,5000,5000]))
        self.primingWashesButton.grid(row=5, column=1, padx=5, pady=5)


        ##Vent 7s
        self.ventButton = Button(self, text="Vent 7s",
                                 command=lambda: vent_Callback(self,hardware))
        self.ventButton.grid(row=6, column=2, padx=30, pady=5)

        ## Stir 3min
        self.stirButton = Button(self, text="Stir 3min",
                                 command=lambda: waitAndStir(hardware, 3*60))
        self.stirButton.grid(row=3, column=2, padx=30, pady=5)

        ## Stir 30s
        self.stirButton = Button(self, text="Stir 30s",
                                          command=lambda: waitAndStir(hardware,30))
        self.stirButton.grid(row=4, column=2, padx=30, pady=5)

        ## Stir 10s
        self.stirButton = Button(self, text="Stir 10s",
                                 command=lambda: waitAndStir(hardware, 10))
        self.stirButton.grid(row=5, column=2, padx=30, pady=5)

        '''Vent And Vacuum'''
        self.ventOffVacOnButton = Button(self, text="Start Vac",
                                 command=lambda: ventOffVacOn_Callback(hardware))
        self.ventOffVacOnButton.grid(row=3, column=3, padx=30, pady=5)

        self.ventOnVacOffButton = Button(self, text="Stop Vac",
                                         command=lambda: ventOnVacOff_Callback(hardware))
        self.ventOnVacOffButton.grid(row=4, column=3, padx=30, pady=5)

        '''Go To Positions'''
        ##Go To Safe position
        self.safeButton = Button(self, text="Safe Pos",
                                        command=lambda: goToWell(hardware, 'safe', 1, 0))
        self.safeButton.grid(row=9, column=1, padx=5, pady=5)

        ##Go To Priming position
        self.primeWashesButton = Button(self, text="Wash Prime Pos",
                                 command=lambda: goToWell(hardware,'washPrime',1,0))
        self.primeWashesButton.grid(row=9, column=3, padx=30, pady=5)

        ##Go To Priming position
        self.primePremixButton = Button(self, text="Premix Prime Pos",
                                        command=lambda: goToWell(hardware, 'premixPrime', 1, 0))
        self.primePremixButton.grid(row=9, column=2, padx=30, pady=5)

        '''Variable volume Block'''

        ##Entry
        self.volumeToDisp_value = StringVar()
        self.volumeToDisp=Entry(self,textvariable=self.volumeToDisp_value)
        self.volumeToDisp.grid(row=1,column=5)
        self.volumeToDisp_value.set('25')

        self.multidispMNACGTButton = Button(self, text="MNACGT",
                                            command=lambda: multiDispensePumps(hardware, [float(self.volumeToDisp_value.get()) for i in range(6)]+[0,0,0,0,0,0]))
        self.multidispMNACGTButton.grid(row=2, column=5, padx=5, pady=5)

        self.multidispMNACGTButton = Button(self, text="MNACGTOP",
                                            command=lambda: multiDispensePumps(hardware,
                                                                               [float(self.volumeToDisp_value.get()) for
                                                                                i in range(8)] + [ 0, 0, 0, 0]))
        self.multidispMNACGTButton.grid(row=3, column=5, padx=5, pady=5)

        self.multidispButton = Button(self, text="ACGT", command=lambda : multiDispensePumps(hardware, [0,0]+[float(self.volumeToDisp_value.get()) for i in range(4)]+[0,0,0,0,0,0]))
        self.multidispButton.grid(row=4, column=5, padx=5, pady=5)

        self.multidispMNButton = Button(self, text="MN",
                                            command=lambda: multiDispensePumps(hardware, [float(self.volumeToDisp_value.get()) for i in range(2)]+[0,0,0,0,0,0,0,0,0,0]))
        self.multidispMNButton.grid(row=5, column=5, padx=5, pady=5)

        simpleChannelList=['M', 'N', 'A', 'C','G','T', 'O', 'P', ]
        self.bufferButton = [None] * len(simpleChannelList)
        for buffer in simpleChannelList:
            self.bufferButton[simpleChannelList.index(buffer)] = Button(self, text=buffer, command=lambda buffer=buffer: multiDispensePumps(hardware,disp_pattern(simpleChannelList.index(buffer),float(self.volumeToDisp_value.get())*1) ))
            self.bufferButton[simpleChannelList.index(buffer)].grid(row=6 + simpleChannelList.index(buffer),column=5,padx=5, pady=5)

        quadChannelList = ['DB', 'BB', 'Buff1', 'Buff2']
        self.quadBufferButton = [None] * len(quadChannelList)
        for buffer in quadChannelList:
            self.quadBufferButton[quadChannelList.index(buffer)] = Button(self, text=buffer, command=lambda
                buffer=buffer: multiDispensePumps(hardware, disp_pattern(len(simpleChannelList)+quadChannelList.index(buffer),
                                                                         float(self.volumeToDisp_value.get()) * 4)))
            self.quadBufferButton[quadChannelList.index(buffer)].grid(row=5 + quadChannelList.index(buffer), column=6,
                                                                    padx=5, pady=5)

        self.initButton= Button(self, text='Init', command=lambda : hardware.init_du(int(self.volumeToDisp_value.get())))
        self.initButton.grid(row=5 + quadChannelList.index(buffer) + 3,column=6,padx=5, pady=5)

        self.initAllButton = Button(self, text='Init All',
                                 command=lambda: hardware.init_all_du())
        self.initAllButton.grid(row=5 + quadChannelList.index(buffer) + 4, column=6, padx=5, pady=5)
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

        '''GoToWell Block'''
        self.colToGo_value = StringVar()
        self.colToGo = Entry(self, textvariable=self.colToGo_value)
        self.colToGo.grid(row=1, column=7)
        self.colToGo_value.set('1')

        buffersList = ['A', 'C', 'G', 'T', 'M', 'N', 'DB', 'BB', 'Buff1', 'Buff2','PosPressure']
        self.bufferButton2 = [None] * len(buffersList)
        for buffer in buffersList:
            self.bufferButton2[buffersList.index(buffer)] = Button(self, text=buffer,
                                                                  command=lambda buffer=buffer: goToColumn_Callback(self,hardware,buffer))
            self.bufferButton2[buffersList.index(buffer)].grid(row=3 + buffersList.index(buffer), column=7, padx=5,
                                                              pady=5)

        '''PositivePressure'''
        self.posPressTime_value = StringVar()
        self.posPressTime = Entry(self, textvariable=self.posPressTime_value)
        self.posPressTime.grid(row=1, column=8)
        self.posPressTime_value.set('0.3')

        self.posPressDessButton = Button(self, text="P+ Dessalt + Quant",command=lambda: removeSupernatantPosPressure(hardware,"excel",float(self.posPressTime_value.get()),"dessalt",0))
        self.posPressDessButton .grid(row=2, column=8, padx=5,pady=5)

        self.posPressSynDessButton = Button(self, text="P+ Syn+Dessalt",
                                         command=lambda: removeSupernatantPosPressure(hardware, "excel", float(
                                             self.posPressTime_value.get()), "synDessaltStack", 0))
        self.posPressSynDessButton.grid(row=3, column=8, padx=5, pady=5)

        self.posPressSynButton = Button(self, text="P+ Synthesis",
                                        command=lambda: removeSupernatantPosPressure(hardware, "excel", float(
                                            self.posPressTime_value.get()), "synthesis", 0))
        self.posPressSynButton.grid(row=4, column=8, padx=5, pady=5)

        '''Fill'''
        self.fillVol_value = StringVar()
        self.fillVol = Entry(self, textvariable=self.fillVol_value)
        self.fillVol.grid(row=6, column=8)
        self.fillVol_value.set('25')

        self.fillVolLabel = Label(self, text="ul to fill", justify="center")
        self.fillVolLabel.grid(row=6, column=9)

        self.is384_value = StringVar()
        self.is384 = Entry(self, textvariable=self.is384_value)
        self.is384.grid(row=7, column=8)
        self.is384_value.set('0')
        self.is384flag = Label(self, text="1=384 0=96", justify="center")
        self.is384flag.grid(row=7, column=9)

        fillList = ['nucs', 'DB', 'BB', 'Buff1']
        self.fillButtons = [None] * len(fillList)
        for fill in fillList:
            self.fillButtons[fillList.index(fill)] = Button(self, text=fill,
                                                                   command=lambda buffer=fill: fillPlate(hardware,buffer,float(self.fillVol_value.get()),float(self.is384_value.get())))
            self.fillButtons[fillList.index(fill)].grid(row=8 + fillList.index(fill), column=8, padx=5,
                                                               pady=5)
        self.PSPWashesButton = Button(self, text="PSP Washes",command=lambda : PSPWashes_96OP_onlynucs(hardware, float(self.is384_value.get())))
        self.PSPWashesButton.grid(row=13,column=8,padx=5,pady=5)

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

    hardware.vacValveOpen()

def ventOnVacOff_Callback(hardware):

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
    pattern=[0,0,0,0,0,0,0,0,0,0,0,0]
    pattern[id]=vol

    return pattern
'''CALLBACKS FOR LEFT FRAME'''

if __name__ == "__main__":
    # On crée la racine de notre interface
    root = Tk()
    MainFrame(root).pack()
    root.mainloop()
