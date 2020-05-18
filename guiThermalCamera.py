from tkinter import *
from tkinter import ttk
from guiTab1 import MainFrameTab1,RightFrame,DirectCommand
from guiTab2 import MainFrameTab2
import threading

class guiThermalCamera():
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent


        self.rootThermalCamera = Tk()
        self.rootThermalCamera.title("ThermalCamera")

        self.rightFrame=RightFrame(self.rootThermalCamera)
        self.rightFrame.pack()

    def startGui(self):
        self.rootThermalCamera.mainloop()

