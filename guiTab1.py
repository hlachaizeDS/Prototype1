# On importe Tkinter
import threading
from tkinter import *
from hardware import *
from action import actionButton_Callback
import TMCL
from  Optris import *
from Thermal import ThermalImageThread,ThermalImage,ThermalImageParams
from PIL import Image, ImageTk
from matplotlib import pyplot as plt


class MainFrameTab1(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        '''Hardware(motors,Leds,...)'''
        self.hardware = HardWare(self)

        #Title
        self.titleLabel = Label(self, text="OligoPrint Soft",justify="center")
        self.titleLabel.grid(row=1, columnspan=2)

        '''Frame on the Right'''
        if self.hardware.thermalCam:
            self.rightFrame = RightFrame(self,bd=2,relief=GROOVE,padx=5,pady=5)
            self.rightFrame.grid(row=3, column=3)

        '''Frame on the Left'''
        self.leftFrame = LeftFrame(self,bd=2,relief=GROOVE,padx=5,pady=5)
        self.leftFrame.grid(row=3, column=1)

        '''DirectCommand Frame'''
        self.directCommand=DirectCommand(self,bd=2,relief=GROOVE,padx=5,pady=5)
        self.directCommand.grid(row=3, column=2)


class RightFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


        initimg=np.zeros([100,100,3],dtype=np.uint8)
        raw_img=Image.fromarray(initimg)
        img=ImageTk.PhotoImage(raw_img,master=parent)


        self.ImageLabel=Label(self,height=120*3,width=160*3,image=img)
        self.ImageLabel.pack()
        self.ImageLabel.Image=img

        self.thermalThread = ThermalImageThread(self)

        self.tempLabel=Label(self,text="",width=40)
        self.tempLabel.pack(side="bottom",fill="x")
        self.tempmeanLabel=Label(self,text="",width=40)
        self.tempmeanLabel.pack(side="bottom",fill="x")

        #Binding to get temperatures live
        self.ImageLabel.bind("<Enter>",self.on_enter)
        self.ImageLabel.bind("<Leave>",self.on_leave)

    def on_enter(self, event):
            self.tempLabel.configure(text="Connecting")

    def on_leave(self, event):
            self.tempLabel.configure(text="")

class LeftFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.cycleLabelString = StringVar()
        self.cycleLabelString.set('Waiting')
        self.cycleLabel = Label(self, textvariable=self.cycleLabelString, width=20,padx=5,pady=5)
        self.cycleLabel.grid(row=1, column=1)

        self.statusLabelString = StringVar()
        self.statusLabelString.set('StatusBar')
        self.statusLabel = Label(self, textvariable=self.statusLabelString,width=20)
        self.statusLabel.grid(row=2,column=1)

        self.skipButton_value = IntVar()
        self.skipButton = Checkbutton(self, text="Skip",indicatoron=0,variable=self.skipButton_value)
        self.skipButton.grid(row=2, column=1, padx=5, pady=5,sticky='ne')



class DirectCommand(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


        #Initialisation
        self.initialisationButton = Button(self, text="Initialisation", command=lambda: initialisationButton_CallBack(self))
        self.initialisationButton.grid(row=1,columnspan=2,padx=5, pady=5)

        self.initialisationLed=Frame(self,width=10,height=10,relief=GROOVE,bd=2,bg='red')
        self.initialisationLed.grid_propagate(0)
        self.initialisationLed.grid(row=1,columnspan=2,sticky='e')
        #POSITION
        self.PositionsButton = Button(self, text="Positions",
                                           command=lambda: positionsButton_CallBack(self))
        self.PositionsButton.grid(row=1,column=2, columnspan=2, padx=5, pady=5)
        #UP
        self.needlesLabel = Label(self, text="Positive Pressure")
        self.needlesLabel.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.goUpButton_value = IntVar()
        self.goUpButton = Checkbutton(self, text="UP", command=lambda: goButton_CallBack(self,"goUp"),indicatoron=0, variable=self.goUpButton_value)
        self.goUpButton.grid(row=3, column=0,columnspan=2, padx=5, pady=5,sticky='e')
        #DOWN
        self.goDownButton_value = IntVar()
        self.goDownButton = Checkbutton(self, text="DOWN", command=lambda: goButton_CallBack(self,"goDown"), indicatoron=0,variable=self.goDownButton_value)
        self.goDownButton.grid(row=4, column=0,columnspan=2,padx=5,pady=5,sticky='e')

        # BOTTOM Pressure
        self.goBottomPressure = Button(self, text="BOT", font=('Helvetica', '7'),
                                        command=lambda: pressureGoDown(self.parent.hardware))
        self.goBottomPressure.grid(row=4, column=0, columnspan=1, padx=5, pady=5, sticky="w")

        # TOP Pressure
        self.goTopPressureButton = Button(self, text="TOP", font=('Helvetica', '7'),
                                        command=lambda: pressureGoUp(self.parent.hardware))
        self.goTopPressureButton.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky="e")

        # # UP MAGNET
        # self.magnetLabel=Label(self,text="Magnet")
        # self.magnetLabel.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        # self.goUpMagnetButton_value = IntVar()
        # self.goUpMagnetButton = Checkbutton(self, text="UP", command=lambda: goButton_CallBack(self, "goUpMagnet"), indicatoron=0,
        #                               variable=self.goUpMagnetButton_value)
        # self.goUpMagnetButton.grid(row=3, column=3, columnspan=1, padx=5, pady=5,sticky="w")
        # # TOP MAGNET
        # self.goTopMagnetButton = Button(self, text="TOP",font=('Helvetica', '7'), command=lambda: magnetGoUp(self.parent.hardware))
        # self.goTopMagnetButton.grid(row=3, column=3, columnspan=1, padx=5, pady=5,sticky="e")
        # # DOWN MAGNET
        # self.goDownMagnetButton_value = IntVar()
        # self.goDownMagnetButton = Checkbutton(self, text="DOWN", command=lambda: goButton_CallBack(self, "goDownMagnet"),
        #                                 indicatoron=0, variable=self.goDownMagnetButton_value)
        # self.goDownMagnetButton.grid(row=4, column=2, columnspan=2, padx=5, pady=5)
        #RIGHT
        self.goRightButton_value=IntVar()
        self.goRightButton = Checkbutton(self, text="RIGHT", command=lambda: goButton_CallBack(self,"goRight"), indicatoron=0,variable=self.goRightButton_value)
        self.goRightButton.grid(row=6,column=1,rowspan=2,padx=5,pady=5)
        #LEFT
        self.goLeftButton_value = IntVar()
        self.goLeftButton = Checkbutton(self, text="LEFT", command=lambda: goButton_CallBack(self,"goLeft"), indicatoron=0,variable=self.goLeftButton_value)
        self.goLeftButton.grid(row=6,column=0,rowspan=2,padx=5,pady=5)
        #IN
        self.goInButton_value = IntVar()
        self.goInButton = Checkbutton(self, text="IN", command=lambda: goButton_CallBack(self,"goIn"), indicatoron=0,variable=self.goInButton_value)
        self.goInButton.grid(row=6,column=3,padx=5,pady=5)
        #OUT
        self.goOutButton_value = IntVar()
        self.goOutButton = Checkbutton(self, text="OUT", command=lambda: goButton_CallBack(self,"goOut"), indicatoron=0,variable=self.goOutButton_value)
        self.goOutButton.grid(row=7, column=3, padx=5, pady=5)
        #VELOCITY
        self.velocityScale = Scale(self,orient='vertical',from_=5,to=50,resolution=5,relief='solid')
        self.velocityScale.grid(row=6 ,column=4,rowspan=2)
        self.velocityScale.set(30)

        #SAFE
        self.safeButton = Button(self, text="SAFE POS", command=lambda: goToWell(self.parent.hardware,"safe",1,0))
        self.safeButton.grid(row=9,column=1, padx=5, pady=5)

        #STIRRING
        self.stirringButton_value = IntVar()
        self.oppositeStirringButton_value = IntVar() #Just to have an "opposite value" to put at 0
        self.stirringButton = Checkbutton(self, text="STIRRING", command=lambda: stirring_Callback(self),
                                       indicatoron=0, variable=self.stirringButton_value)
        self.stirringButton.grid(row=9, column=3, padx=5, pady=5)

        #STOP
        self.stopButton_value = IntVar()
        self.stopButton = Checkbutton(self, text="STOP",fg='red', command=lambda: stopButton_Callback(self),indicatoron=0,variable=self.stopButton_value)
        self.stopButton.grid(row=0, column=5, padx=30, pady=5)

        # ACTION
        self.actionButton = Button(self, text="ACTION", command=lambda: actionButton_Callback(self))
        self.actionButton.grid(row=1, column=5, padx=30, pady=5)

        #Digital Ouputs 1
        digitalOutputsNb=8
        self.digitalOutputButton_value = [None] * digitalOutputsNb
        self.digitalOutputButton = [None] * digitalOutputsNb

        for i in range(digitalOutputsNb):
            self.digitalOutputButton_value[i]=IntVar()
            self.digitalOutputButton[i]=Checkbutton(self, text="Dig Out " + str(i) , command=lambda i=i: digitalOutput_Callback(self, i), indicatoron=0, variable=self.digitalOutputButton_value[i])
            self.digitalOutputButton[i].grid(row=i+2,column=5,padx=30 ,pady=5)

        # Digital Ouputs 2
        digitalOutputsNb2 = 8
        self.digitalOutputButton2_value = [None] * digitalOutputsNb2
        self.digitalOutputButton2 = [None] * digitalOutputsNb2

        for i in range(digitalOutputsNb2):
            self.digitalOutputButton2_value[i] = IntVar()
            self.digitalOutputButton2[i] = Checkbutton(self, text="Dig Out " + str(i),
                                                      command=lambda i=i: digitalOutput2_Callback(self, i),
                                                      indicatoron=0, variable=self.digitalOutputButton2_value[i])
            self.digitalOutputButton2[i].grid(row=i + 2, column=6, padx=30, pady=5)

        #Arduino Heating
        self.arduinoHeating_value = IntVar()
        self.arduinoHeating = Checkbutton(self, text="Heating",
                                                   command=lambda : arduinoHeating_Callback(self),
                                                   indicatoron=0, variable=self.arduinoHeating_value)
        self.arduinoHeating.grid(row=0,column=6,padx=5,pady=5)

'''CALLBACK FUNCTIONS'''

def goButton_CallBack(directCommand,button):
    #Button is a string determining which button we press

    VELOCITY=directCommand.velocityScale.get() * 1000

    if button=="goRight":
        value = directCommand.goRightButton_value.get()
        motor = directCommand.parent.hardware.xMotor
        velocity = VELOCITY
        sens="left"
        oppositeButtonValue=directCommand.goLeftButton_value

    elif button=="goLeft":
        value = directCommand.goLeftButton_value.get()
        motor = directCommand.parent.hardware.xMotor
        velocity=VELOCITY
        sens = "right"
        oppositeButtonValue = directCommand.goRightButton_value

    elif button == "goIn":
        value = directCommand.goInButton_value.get()
        motor = directCommand.parent.hardware.yMotor
        velocity = VELOCITY
        sens = "right"
        oppositeButtonValue = directCommand.goOutButton_value

    elif button == "goOut":
        value = directCommand.goOutButton_value.get()
        motor = directCommand.parent.hardware.yMotor
        velocity = VELOCITY
        sens = "left"
        oppositeButtonValue = directCommand.goInButton_value

    elif button == "goUp":
        value = directCommand.goUpButton_value.get()
        motor = directCommand.parent.hardware.zMotor
        velocity = VELOCITY*6
        sens = "right"
        oppositeButtonValue = directCommand.goDownButton_value

    elif button == "goDown":
        value = directCommand.goDownButton_value.get()
        motor = directCommand.parent.hardware.zMotor
        velocity = VELOCITY*6
        sens = "left"
        oppositeButtonValue = directCommand.goUpButton_value

    elif button == "goUpMagnet":
        value = directCommand.goUpMagnetButton_value.get()
        motor = directCommand.parent.hardware.magnetMotor
        velocity = VELOCITY*10
        sens = "right"
        oppositeButtonValue = directCommand.goDownMagnetButton_value

    elif button == "goDownMagnet":
        value = directCommand.goDownMagnetButton_value.get()
        motor = directCommand.parent.hardware.magnetMotor
        velocity = VELOCITY*10
        sens = "left"
        oppositeButtonValue = directCommand.goUpMagnetButton_value

    elif button == "stirring":
        value = directCommand.stirringButton_value.get()
        motor = directCommand.parent.hardware.stirrerMotor
        velocity = STIRRING_VELOCITY
        sens = "right"
        oppositeButtonValue = directCommand.oppositeStirringButton_value

    #We unselect the Opposite Button
    oppositeButtonValue.set(0)

    if value == 1:
        if sens == "right":
            motor.rotate_left(velocity)
        elif sens == "left":
            motor.rotate_right(velocity)
    elif value == 0:
        motor.stop()

def stirring_Callback(directCommand):
    #Turns on and off digital Ouputs
    value = directCommand.stirringButton_value.get()
    if value:
        directCommand.parent.hardware.arduinoControl.startShaking(280)
    else:
        directCommand.parent.hardware.arduinoControl.stopShaking()

def digitalOutput_Callback(directCommand,i):
    #Turns on and off digital Ouputs
    value = directCommand.digitalOutputButton_value[i].get()
    directCommand.parent.hardware.set_output(i, value)

def digitalOutput2_Callback(directCommand,i):
    #Turns on and off digital Ouputs
    value = directCommand.digitalOutputButton2_value[i].get()
    directCommand.parent.hardware.set_output2(i, value)


def initialisationButton_CallBack(directCommand):

    directCommand.parent.hardware.initialisation()

def positionsButton_CallBack(directCommand):

    directCommand.parent.hardware.give_positions()

def positionsButton_CallBack(directCommand):

    directCommand.parent.hardware.give_positions()

def stopButton_Callback(directCommand):
    h=directCommand.parent.hardware
    for motor in [h.xMotor,h.yMotor,h.zMotor,h.stirrerMotor,h.magnetMotor]:
        motor.stop

def arduinoHeating_Callback(directCommand):
    hardware=directCommand.parent.hardware
    value=directCommand.arduinoHeating_value.get()
    if value:
        hardware.arduinoControl.startHeating()
    else:
        hardware.arduinoControl.stopHeating()

'''CALLBACKS FOR LEFT FRAME'''

if __name__ == "__main__":
    # On crée la racine de notre interface
    root = Tk()
    MainFrame(root).pack()
    root.mainloop()
