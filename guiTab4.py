# On importe Tkinter
import threading
from tkinter import *
from tkinter import font
from tkinter.tix import *

from hardware import *
from action import actionButton_Callback
from cycles_steps import *
from PSPs import *
from guiTab1 import arduinoHeating_Callback


class MainFrameTab4(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        '''Hardware(motors,Leds,...)'''
        # self.hardware = HardWare(self)

        # Title
        self.label_font_0 = font.Font(size=15, weight='bold')
        self.titleLabel = Label(self, text="PDR Synthesis Tab", justify="center", bg='#E8E8E8', width=80,
                                font=self.label_font_0)
        self.titleLabel.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky='EW')

        '''Only one frame so far'''
        self.middleFrame = MiddleFrame(self)
        self.middleFrame.grid(row=2, column=0)


class MiddleFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.tool_tip = Balloon(self)

        # print(self.parent.parent.tab(1))
        hardware = self.parent.parent.children['!mainframetab1'].hardware

        self.label_font_1 = font.Font(size=10, weight='bold')
        self.LabelPriming = Label(self, text="PRIME", justify="center", fg='#524CF9', bg='#B8B6FC', width=40,
                                  font=self.label_font_1)
        self.LabelPriming.grid(row=0, column=2, padx=30, pady=10, sticky='EW')

        # Init Pumps
        self.initAllFirstButton = Button(self, text="Init All Pumps", command=lambda: hardware.init_all_du(), width=20, bg='#E1E1E1')
        self.initAllFirstButton.grid(row=2, column=2, padx=5, pady=5)

        # Priming all lines
        self.PrimingAllLines = Button(self, text="Prime All Lines",
                                         command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {**{line : 3000 for line in ["M","N","A","C","G","T","O","P","Q"]},
                                                                         **{lines : 7000 for lines in ["DB","BB","Buff1","Buff2"]}})], bg='#E1E1E1', width=20)
        self.PrimingAllLines.grid(row=4, column=2, padx=30, pady=5)
        self.tool_tip.bind_widget(self.PrimingAllLines, balloonmsg="Mono 3mL \nQuad 7mL")


        # Prime Idex
        #self.PrimingIdex = Button(self, text="Prime Idex",
        #                                  command=lambda: prime_IdexPumps(hardware, 7500), bg='#E1E1E1',width=20)
        #self.PrimingIdex.grid(row=3, column=2, padx=30, pady=5)
        #self.tool_tip.bind_widget(self.PrimingIdex, balloonmsg="5mL")


        self.LabelRinse = Label(self, text="RINSE", justify="center", fg='#169902', bg='#91F582', width=40,
                                font=self.label_font_1)
        self.LabelRinse.grid(row=0, column=1, pady=10, padx=10, sticky='EW')

        # Rinse all lines after synthesis milliQ
        self.RinseAllLines = Button(self, text="Rinse All Lines",
                                    command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {line : 15000 for line in ["M","N","A","C","G","T","O","P","Q","DB","BB","Buff1","Buff2"]})], bg='#E1E1E1', width=20)
        self.RinseAllLines.grid(row=2, column=1, padx=30, pady=5)
        self.tool_tip.bind_widget(self.RinseAllLines, balloonmsg="H2O MQ \n15mL")


        '''Process buttons'''

        self.LabelProcess = Label(self, text="PROCESS", justify="center", fg='#B4290B', bg='#FA9084', width=40,
                                  font=self.label_font_1)
        self.LabelProcess.grid(row=0, column=3, pady=10, padx=10, sticky='EW')

        self.DBcompButton = Button(self, text="DB comparaison",
                                      command=lambda: PDR_Synthesis_TwoEnz_TwoDB_Xop(hardware,0), bg='#DFFF00', width=30)
        self.DBcompButton.grid(row=2, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.DBcompButton, balloonmsg="DB = DB ctrl \nBB = DB test \nBuff1 = S4 \nBuff2 = S3 \nMN = TDT \nOP = CR0")

        self.nucsButton = Button(self, text="DMSO comparaison",
                                      command=lambda: PDR_OneEnz_EightNucs_Xbuff2(hardware, 0), bg='#CD1076', width=30)
        self.nucsButton.grid(row=3, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.nucsButton, balloonmsg="DB = DB \nBB = S3 \nBuff1 = S4 \nBuff2 = CR0 \nM = TDT \nNOPQ = Nucs test")

        self.wb2Button = Button(self, text="WB2 comparaison",
                                      command=lambda: PDR_Synthesis_OneEnz_TwoWB2_Xop(hardware, 0), bg='#00BFFF', width=30)
        self.wb2Button.grid(row=4, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.wb2Button, balloonmsg="DB = DB \nBB = S4 \nBuff1 = S3 ctrl \nBuff2 = S3 test \nMN = TDT \nOP = CR0")

        self.wb1Button = Button(self, text="WB1 comparaison",
                                      command=lambda: PDR_Synthesis_OneEnz_TwoWB1_Xop(hardware, 0), bg='#00C957', width=30)
        self.wb1Button.grid(row=5, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.wb1Button, balloonmsg="DB = DB \nBB = S3 \nBuff1 = S4 ctrl \nBuff2 = S4 test \nMN = TDT \nOP = CR0")


'''CALLBACK FUNCTIONS'''


def primerBuffer_Callback(hardware, solution):
    # Primer for 10s selected buffer, then dispense 0.1s

    dispense(hardware, solution, 10)
    sleep(1)
    dispense(hardware, solution, 0.05)


def vent_Callback(middleFrame, hardware):
    # Vents for 10s

    hardware.vacValveOpen()
    wait(hardware, 7)
    hardware.vacValveClose()

    # hardware.set_output(7, 1)
    # wait(hardware, 10)
    # hardware.set_output(7, 0)


def ventOffVacOn_Callback(hardware):
    if hardware.extraVentilation:
        hardware.set_output(1, 1)
    hardware.vacValveOpen()


def ventOnVacOff_Callback(hardware):
    if hardware.extraVentilation:
        hardware.set_output(1, 0)
    hardware.vacValveClose()


def hitPrimingPremix_Callback(hardware):
    secondsToPrime = 15
    stroke = 0.15  # seconds
    for i in range(int(secondsToPrime / (stroke * 2))):
        multiDispense(hardware, [1, 1, 1, 1], stroke)
        sleep(stroke)


def bufferButton_Callback(directCommand, i):
    # Turns on and off digital Ouputs
    value = directCommand.digitalOutputButton_value[i].get()
    directCommand.parent.hardware.set_output(i, value)


def goToColumn_Callback(MiddleFrame, hardware, buffer):
    colToGo = int(MiddleFrame.colToGo_value.get())
    goToWell(hardware, buffer, (colToGo - 1) * 4 + 1, 0)
    MiddleFrame.colToGo_value.set(colToGo + 1)


def disp_pattern(id, vol):
    pattern = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    pattern[id] = vol

    return pattern


'''CALLBACKS FOR LEFT FRAME'''

if __name__ == "__main__":
    # On crée la racine de notre interface
    root = Tk()
    MainFrame(root).pack()
    root.mainloop()
