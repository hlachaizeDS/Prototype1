from tkinter import *

class TkinterRefresher:
    def __init__(self, parent):
        self.parent=parent
        self.counter=0
        if self.parent.hardware.thermalCam:
            self.refreshGUI()


    def refreshGUI(self):
        self.parent.rightFrame.update()
        self.parent.after(50,self.refreshGUI)