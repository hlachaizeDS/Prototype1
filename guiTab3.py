# On importe Tkinter
import threading
from tkinter import *
from tkinter.tix import *
from tkinter import font

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
        self.LabelPriming = Label(self, text="PRIME", justify="center", fg='#524CF9', bg='#B8B6FC', width= 40,
                                  font=self.label_font_1)
        self.LabelPriming.grid(row=0, column=2, padx=30, pady=10, sticky='EW')

        # Priming all PSP lines
        self.PrimingAllPSPLines = Button(self, text="Prime All PSP Lines",
                                          command=lambda: multi_dispense(hardware, {line : 4000 for line in ["N", "DB","BB","Buff1","Buff2"]}), bg='#E1E1E1', width=20)
        self.PrimingAllPSPLines.grid(row=2, column=2, padx=10, pady=5)
        self.tool_tip.bind_widget(self.PrimingAllPSPLines, balloonmsg="MN+Quad 4mL")

        # Priming M&N lines
        self.PrimingMNLines = Button(self, text="Prime MN",
                                          command=lambda: multi_dispense(hardware, {line : 4000 for line in ["M","N"]}), bg='#E1E1E1', width=20)
        self.PrimingMNLines.grid(row=4, column=2, padx=10, pady=5)
        self.tool_tip.bind_widget(self.PrimingMNLines, balloonmsg="MN 4mL")

        # Priming buffers lines
        self.PrimingBuffersLines = Button(self, text="Prime Quad",
                                          command=lambda: multi_dispense(hardware, {line : 4000 for line in ["DB","BB","Buff1","Buff2"]}), bg='#E1E1E1', width=20)
        self.PrimingBuffersLines.grid(row=5, column=2, padx=10, pady=5)
        self.tool_tip.bind_widget(self.PrimingBuffersLines, balloonmsg="Quad 4mL")

        self.LabelRinse = Label(self, text="RINSE", justify="center", fg='#169902', bg='#91F582', width= 40,
                                  font=self.label_font_1)
        self.LabelRinse.grid(row=0, column=1, pady=10, padx=10, sticky='EW')

        # Rinse all lines after synthesis miliQ
        self.RinseAllLines = Button(self, text="Rinse All Lines",
                                             command=lambda: multi_dispense(hardware, {line : 15000 for line in ["M","N","A","C","G","T","O","P","Q","DB","BB","Buff1","Buff2"]}), bg='#E1E1E1', width=20)
        # à ajouter pour init les pompes hardware.init_all_du() en même temps que le rince all lines
        self.RinseAllLines.grid(row=2, column=1, padx=10, pady=5)
        self.tool_tip.bind_widget(self.RinseAllLines, balloonmsg="A lancer 2 fois \nBien vider la cuve trash \n\nH2O MQ \n15mL")

        # Rinse all buffs BM
        self.RinseAllPSPLines15 = Button(self, text="Rinse PSP Lines",
                                         command=lambda: multi_dispense(hardware, {line : 45000 for line in ["N","DB","BB","Buff1","Buff2"]}), bg='#E1E1E1', width=20)
        self.RinseAllPSPLines15.grid(row=3, column=1, padx=10, pady=5)
        self.tool_tip.bind_widget(self.RinseAllPSPLines15, balloonmsg="A lancer 1 fois \nBien vider la cuve trash \n\nH2O BM \n45mL")

        # Arduino Heating
        # " self.arduinoHeating_value = IntVar()
        # self.arduinoHeating = Checkbutton(self, text="Heating",
        # command=lambda : arduinoHeating_Callback(self),
        # indicatoron=0, variable=self.arduinoHeating_value)
        # self.arduinoHeating.grid(row=0,column=6,padx=5,pady=5)


        '''Process buttons'''
        self.LabelProcess = Label(self, text="PROCESS 96", justify="center", fg='#B4290B', bg='#FA9084', width=40,
                                  font=self.label_font_1)
        self.LabelProcess.grid(row=0, column=3, pady=10, padx=10, sticky='EW')

        self.PSP96Button = Button(self, text="PSP One-Pot 96",
                                      command=lambda: PSP_OnePot_96(hardware, 0), bg='#E1E1E1', width=20)
        self.PSP96Button.grid(row=1, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.PSP96Button, balloonmsg="Manifold 50°C \n\nDB = H2O \nBB = IPA \nBuff1 = ETH \nBuff2 = P1 + P1E \nN = P2 + P2E")

        self.Elu96Button = Button(self, text="Heated 37°C Elution 96",
                                      command=lambda: HeatedElution30_96(hardware, 0), bg='#E1E1E1', width=20)
        self.Elu96Button.grid(row=2, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.Elu96Button, balloonmsg="Std protocol \n\nManifold 50°C \nPreHeat 20min \n60ul H2O \nIncubation 30min")

        self.Elu96Button = Button(self, text="Heated HT Elution 96",
                                      command=lambda: HeatedElution15_96(hardware, 0), bg='#E1E1E1', width=20)
        self.Elu96Button.grid(row=2, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.Elu96Button, balloonmsg="For 500 mers or evil seqs \n\nManifold 80°C \nPreHeat 20min \n60ul H2O \nIncubation 15min")

        self.LabelProcess = Label(self, text="PROCESS 384", justify="center", fg='#B4290B', bg='#FA9084', width=40,
                                  font=self.label_font_1)
        self.LabelProcess.grid(row=4, column=3, pady=10, padx=10, sticky='EW')

        self.PSP384Button = Button(self, text="PSP One-Pot 384",
                                      command=lambda: PSP_OnePot_384(hardware, 1), bg='#E1E1E1', width=20)
        self.PSP384Button.grid(row=5, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.PSP384Button, balloonmsg="Manifold 60°C \n\nDB = H2O \nBB = IPA \nBuff1 = ETH \nBuff2 = P1 + P1E \nN = P2 + P2E")

        self.Elu384Button = Button(self, text="Heated Elution 384",
                                      command=lambda: HeatedElution_384(hardware, 1), bg='#E1E1E1', width=20)
        self.Elu384Button.grid(row=6, column=3, padx=5, pady=5)
        self.tool_tip.bind_widget(self.Elu384Button, balloonmsg="Manifold 80°C \nPreHeat 20min \n50ul H2O \nHeat 30min")


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
