# On importe Tkinter
import threading
from tkinter import *
from hardware import *
from action import actionButton_Callback
import TMCL



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

        # Priming Premix
        self.initAllFirstButton = Button(self, text="Init All Pumps", command=lambda: hardware.init_all_du())
        self.initAllFirstButton.grid(row=1, column=1, padx=30, pady=5)

        # Priming premix
        self.PrimingPremixButton = Button(self, text="Prime 2mL",
                                             command=lambda: multiDispensePumps(hardware,[2000,2000,2000,2000,2000,2000]))
        self.PrimingPremixButton.grid(row=2, column=1, padx=30, pady=5)

        # Priming DB
        self.primingDBButton = Button(self, text="DB 10s",
                                          command=lambda: primerBuffer_Callback(hardware,"DB"))
        self.primingDBButton.grid(row=3, column=1, padx=30, pady=5)

        ## Priming BB
        self.primingBBButton = Button(self, text="BB 10s",
                                          command=lambda: primerBuffer_Callback(hardware,"BB"))
        self.primingBBButton.grid(row=4, column=1, padx=30, pady=5)

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
        self.safeButton.grid(row=9, column=1, padx=30, pady=5)

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
                                            command=lambda: multiDispensePumps(hardware, [float(self.volumeToDisp_value.get()) for i in range(6)]))
        self.multidispMNACGTButton.grid(row=2, column=5, padx=5, pady=5)

        self.multidispButton = Button(self, text="ACGT", command=lambda : multiDispensePumps(hardware, [0,0]+[float(self.volumeToDisp_value.get()) for i in range(4)]))
        self.multidispButton.grid(row=3, column=5, padx=5, pady=5)

        self.multidispMNButton = Button(self, text="MN",
                                            command=lambda: multiDispensePumps(hardware, [float(self.volumeToDisp_value.get()) for i in range(2)]+[0,0,0,0]))
        self.multidispMNButton.grid(row=4, column=5, padx=5, pady=5)

        channelList=['M', 'N', 'A', 'C','G','T']
        self.bufferButton = [None] * len(channelList)
        for buffer in channelList:
            self.bufferButton[channelList.index(buffer)] = Button(self, text=buffer, command=lambda buffer=buffer: multiDispensePumps(hardware,disp_pattern(channelList.index(buffer),float(self.volumeToDisp_value.get()) )))
            self.bufferButton[channelList.index(buffer)].grid(row=5 + channelList.index(buffer),column=5,padx=5, pady=5)

        self.initButton= Button(self, text='Init', command=lambda : hardware.init_du(int(self.volumeToDisp_value.get())))
        self.initButton.grid(row=5 + channelList.index(buffer) + 1,column=5,padx=5, pady=5)

        self.initAllButton = Button(self, text='Init All',
                                 command=lambda: hardware.init_all_du())
        self.initAllButton.grid(row=5 + channelList.index(buffer) + 2, column=5, padx=5, pady=5)
        ##Entry
        self.timeToDisp_value = StringVar()
        self.timeToDisp = Entry(self, textvariable=self.timeToDisp_value)
        self.timeToDisp.grid(row=1, column=6)
        self.timeToDisp_value.set('0.1')

        buffersList = ['DB', 'BB', 'Buff1', 'Buff2']
        self.bufferButton = [None] * len(buffersList)
        for buffer in buffersList:
            self.bufferButton[buffersList.index(buffer)] = Button(self, text=buffer,
                                                                  command=lambda buffer=buffer: dispense(hardware,
                                                                                                         buffer, float(
                                                                          self.timeToDisp_value.get())))
            self.bufferButton[buffersList.index(buffer)].grid(row=2 + buffersList.index(buffer), column=6, padx=5,
                                                              pady=5)

        '''GoToWell Block'''
        self.colToGo_value = StringVar()
        self.colToGo = Entry(self, textvariable=self.colToGo_value)
        self.colToGo.grid(row=1, column=7)
        self.colToGo_value.set('1')

        buffersList = ['A', 'C', 'G', 'T', 'M', 'N', 'DB', 'BB', 'Buff1', 'Buff2']
        self.bufferButton2 = [None] * len(buffersList)
        for buffer in buffersList:
            self.bufferButton2[buffersList.index(buffer)] = Button(self, text=buffer,
                                                                  command=lambda buffer=buffer: goToColumn_Callback(self,hardware,buffer))
            self.bufferButton2[buffersList.index(buffer)].grid(row=3 + buffersList.index(buffer), column=7, padx=5,
                                                              pady=5)

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
    pattern=[0,0,0,0,0,0]
    pattern[id]=vol

    return pattern
'''CALLBACKS FOR LEFT FRAME'''

if __name__ == "__main__":
    # On crée la racine de notre interface
    root = Tk()
    MainFrame(root).pack()
    root.mainloop()
