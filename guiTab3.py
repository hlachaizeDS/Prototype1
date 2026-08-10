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


class MainFrameTab3(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        '''Hardware(motors,Leds,...)'''
        # self.hardware = HardWare(self)

        # Title
        self.label_font_0 = font.Font(size=15, weight='bold')
        self.titleLabel = Label(self, text="Post Synthesis Process Tab", justify="center", bg='#E8E8E8', width=80,
                                font=self.label_font_0)
        self.titleLabel.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='EW')

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

        # Priming all PSP lines
        self.PrimingAllPSPLinesButton = Button(self, text="Prime PSP Lines",
                                         command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {**{line : 3000 for line in ["N"]},
                                                                         **{lines : 7000 for lines in ["DB","BB","Buff1","Buff2"]}})], bg='#E1E1E1', width=20)
        self.PrimingAllPSPLinesButton.grid(row=2, column=2, padx=30, pady=5)
        self.tool_tip.bind_widget(self.PrimingAllPSPLinesButton, balloonmsg="N 3mL \n Quad 7mL")

        #self.parent.directCommand.PrimingAllPSPLinesLed.configure(bg='green')

        # Priming Idex

        #self.LabelIdex = Label(self, text="Idex : primer entre chaque étape", justify="center", bg='#DFFF00', width=20)
        #self.LabelIdex.grid(row=8, column=1, padx=40, pady=10, sticky='EW')

        #self.PrimingIdexButton = Button(self, text="Prime Idex",
        #                                  command=lambda: prime_IdexPumps(hardware,7500), bg='#E1E1E1', width=20)
        #self.PrimingIdexButton.grid(row=9, column=1, padx=5, pady=5)
        #self.tool_tip.bind_widget(self.PrimingIdexButton, balloonmsg="5mL")


        # Priming M&N lines
        self.PrimingMNLinesButton = Button(self, text="Prime N",
                                     command=lambda: multi_dispense(hardware, {line : 3000 for line in ["N"]}), bg='#E1E1E1', width=20)
        self.PrimingMNLinesButton.grid(row=4, column=2, padx=30, pady=5)
        self.tool_tip.bind_widget(self.PrimingMNLinesButton, balloonmsg="3mL")

        # Priming buffers lines
        self.PrimingBuffersLinesButton = Button(self, text="Prime PSP Quad",
                                          command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {line : 7000 for line in ["DB","BB","Buff1","Buff2"]})], bg='#E1E1E1', width=20)
        self.PrimingBuffersLinesButton.grid(row=5, column=2, padx=30, pady=5)
        self.tool_tip.bind_widget(self.PrimingBuffersLinesButton, balloonmsg="7mL")

        self.LabelRinse = Label(self, text="RINSE", justify="center", fg='#169902', bg='#91F582', width=40,
                                font=self.label_font_1)
        self.LabelRinse.grid(row=0, column=1, padx=10, pady=10, sticky='EW')

        # Rinse all lines after synthesis miliQ
        self.RinseAllLinesButton = Button(self, text="Rinse All Lines",
                                    command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {line : 15000 for line in ["M","N","A","C","G","T","O","P","Q","DB","BB","Buff1","Buff2"]})], bg='#E1E1E1', width=20)
        self.RinseAllLinesButton.grid(row=2, column=1, padx=30, pady=5)
        self.tool_tip.bind_widget(self.RinseAllLinesButton, balloonmsg="H2O MQ \n15mL")


        #self.parent.directCommand.RinseAllLinesLed.configure(bg='green')

        # Rinse all buffs BM
        self.RinseAllPSPLines15Button = Button(self, text="Rinse PSP Lines",
                                         command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {line : 45000 for line in ["N","DB","BB","Buff1","Buff2"]})], bg='#E1E1E1', width=20)
        self.RinseAllPSPLines15Button.grid(row=3, column=1, padx=30, pady=5)
        self.tool_tip.bind_widget(self.RinseAllPSPLines15Button, balloonmsg="H2O BM \n45mL")

        #self.parent.directCommand.RinseAllPSPLines10Led.configure(bg='green')


        # Rinse MN 10mL
        self.RinseMNButton = Button(self, text="Rinse M&N",
                              command=lambda: multi_dispense(hardware, {line : 15000 for line in ["M","N"]}), bg='#E1E1E1', width=20)
        self.RinseMNButton.grid(row=5, column=1, padx=30, pady=5)
        self.tool_tip.bind_widget(self.RinseMNButton, balloonmsg="15mL")

        # Rinse buffs 10mL
        self.RinseBuffersButton = Button(self, text="Rinse Buffers",
                                   command=lambda: [prime_IdexPumps(hardware,7500),multi_dispense(hardware, {line : 15000 for line in ["DB","BB","Buff1","Buff2"]})], bg='#E1E1E1', width=20)
        self.RinseBuffersButton.grid(row=6, column=1, padx=30, pady=5)
        self.tool_tip.bind_widget(self.RinseBuffersButton, balloonmsg="15mL")

        # Arduino Heating
        # " self.arduinoHeating_value = IntVar()
        # self.arduinoHeating = Checkbutton(self, text="Heating",
        # command=lambda : arduinoHeating_Callback(self),
        # indicatoron=0, variable=self.arduinoHeating_value)
        # self.arduinoHeating.grid(row=0,column=6,padx=5,pady=5)


        '''Process buttons'''
        self.LabelProcess = Label(self, text="PROCESS", justify="center", fg='#B4290B', bg='#FA9084', width=40,
                                  font=self.label_font_1)
        self.LabelProcess.grid(row=0, column=3, pady=10, padx=10, sticky='EW')

        self.PSP96Button = Button(self, text="PSP One-Pot 96",
                                      command=lambda: PSP_OnePot_96(hardware, 0), bg='#E1E1E1')
        self.PSP96Button.grid(row=2, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.PSP96Button, balloonmsg="Manifold 64°C \n\nDB = H2O \nBB = IPA \nBuff1 = ETH \nBuff2 = P1 + P1E \nN = P2 + P2E")


        self.Elu96Button = Button(self, text="Heated Elution 96",
                                      command=lambda: HeatedElution_96(hardware, 0), bg='#E1E1E1')
        self.Elu96Button.grid(row=3, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.Elu96Button, balloonmsg="Manifold 80°C \nPreHeat 20min \n60ul H2O \nHeat 30min")


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
