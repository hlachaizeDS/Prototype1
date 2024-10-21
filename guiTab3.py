# On importe Tkinter
import threading
from tkinter import *
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
        self.titleLabel = Label(self, text="Post Synthesis Process Tab", justify="center", bg='#E8E8E8',
                                font=self.label_font_0)
        self.titleLabel.grid(row=0, column=0, columnspan=4, pady=10, sticky='EW')

        '''Only one frame so far'''
        self.middleFrame = MiddleFrame(self)
        self.middleFrame.grid(row=2, column=0)


class MiddleFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # print(self.parent.parent.tab(1))
        hardware = self.parent.parent.children['!mainframetab1'].hardware

        self.label_font_1 = font.Font(size=10, weight='bold')
        self.LabelPriming = Label(self, text="PRIME", justify="center", fg='#524CF9', bg='#B8B6FC',
                                  font=self.label_font_1)
        self.LabelPriming.grid(row=0, column=2, padx=30, pady=10, sticky='EW')

        # Priming all PSP lines
        self.PrimingAllPSPLines = Button(self, text="Prime All PSP Lines (MN 3mL Buffers 7mL)",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [3000, 3000, 0, 0, 0, 0, 0, 0, 7000, 7000,
                                                                              7000, 0]), bg='#E1E1E1')
        self.PrimingAllPSPLines.grid(row=2, column=2, padx=30, pady=5)

        # Priming M&N lines
        self.PrimingMNLines = Button(self, text="Prime MN (3mL)",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [3000, 3000, 0, 0, 0, 0, 0, 0, 0,
                                                                              0, 0, 0]))
        self.PrimingMNLines.grid(row=4, column=2, padx=30, pady=5)

        # Priming buffers lines
        self.PrimingBuffersLines = Button(self, text="Prime Buffers (7mL)",
                                          command=lambda: multiDispensePumps(hardware,
                                                                             [0, 0, 0, 0, 0, 0, 0, 0, 7000,
                                                                              7000, 7000, 0]))
        self.PrimingBuffersLines.grid(row=5, column=2, padx=30, pady=5)

        self.LabelRinse = Label(self, text="RINSE", justify="center", fg='#169902', bg='#91F582',
                                  font=self.label_font_1)
        self.LabelRinse.grid(row=0, column=1, pady=10, sticky='EW')

        # Rinse all lines after synthesis miliQ
        self.RinseAllLines = Button(self, text="Rinse All Lines After Synthesis (15mL)",
                                             command=lambda: multiDispensePumps(hardware, [15000, 15000, 15000, 15000,
                                                                                           15000, 15000, 15000, 15000,
                                                                                           15000, 15000, 15000, 15000, 15000]),
                                    bg='#E1E1E1')
        # à ajouter pour init les pompes hardware.init_all_du() en même temps que le rince all lines
        self.RinseAllLines.grid(row=2, column=1, padx=30, pady=5)

        # Rinse all buffs BM
        self.RinseAllPSPLines10 = Button(self, text="Rinse PSP Lines (15mL) -> BM water",
                                         command=lambda: multiDispensePumps(hardware, [15000, 15000, 0, 0, 0, 0, 0, 0,
                                                                                       15000, 15000, 15000, 0]),
                                         bg='#E1E1E1')
        self.RinseAllPSPLines10.grid(row=3, column=1, padx=30, pady=5)

        # Rinse MN 10mL
        self.RinseMN = Button(self, text="Rinse M&N (10mL)", command=lambda: multiDispensePumps(hardware, [10000, 10000,
                                                                                                           0, 0, 0, 0,
                                                                                                           0, 0, 0, 0,
                                                                                                           0, 0]))
        self.RinseMN.grid(row=5, column=1, padx=30, pady=5)
        # Rinse buffs 10mL
        self.RinseBuffers = Button(self, text="Rinse Buffers (10mL)", command=lambda: multiDispensePumps(hardware,
                                                                                [0, 0, 0, 0, 0, 0, 0, 0, 10000, 10000,
                                                                                 10000, 0]))
        self.RinseBuffers.grid(row=6, column=1, padx=30, pady=5)

        # Arduino Heating
        # " self.arduinoHeating_value = IntVar()
        # self.arduinoHeating = Checkbutton(self, text="Heating",
        # command=lambda : arduinoHeating_Callback(self),
        # indicatoron=0, variable=self.arduinoHeating_value)
        # self.arduinoHeating.grid(row=0,column=6,padx=5,pady=5)


        '''stirring'''
        self.stirButton = Button(self, text="High Stir 5s",
                                 command=lambda: waitAndStir(hardware, 5, 1100))
        self.stirButton.grid(row=3, column=0, padx=30, pady=5)
        self.stirButton2 = Button(self, text="Stir 20s",
                                  command=lambda: waitAndStir(hardware, 20))
        self.stirButton2.grid(row=4, column=0, padx=30, pady=5)

        '''Go To Positions'''
        ##Go To Safe position
        self.safeButton = Button(self, text="Safe Pos",
                                 command=lambda: goToWell(hardware, 'safe', 1, 0))
        self.safeButton.grid(row=5, column=0, padx=30, pady=5)

        '''Process buttons'''
        self.LabelProcess = Label(self, text="PROCESS", justify="center", fg='#B4290B', bg='#FA9084',
                                  font=self.label_font_1)
        self.LabelProcess.grid(row=0, column=3, pady=10, sticky='EW')

        self.PSPWashesButton = Button(self, text="PSP_One-Pot_96 (extra wash version)",
                                      command=lambda: PSPWashes_96OP_extraH20andEtOH(hardware, 0), bg='#E1E1E1')
        self.PSPWashesButton.grid(row=2, column=3, padx=5, pady=5)
        self.PSPWashesButton2 = Button(self, text="PSP_AV", command=lambda: PSPWashes_96OP_AV(hardware, 0))
        self.PSPWashesButton2.grid(row=4, column=3, padx=5, pady=5)


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
