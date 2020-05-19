from tkinter import *
from tkinter import ttk
from guiTab1 import MainFrameTab1
from guiTab2 import MainFrameTab2
from TkinterRefresher import TkinterRefresher
from guiThermalCamera import guiThermalCamera
import threading
from elementaryFunctions import *


#Create GUI
root = Tk()
root.title("Quartet Controler")
tabControl = ttk.Notebook(root)
tab1=MainFrameTab1(tabControl)
#print(tab1._name) #To know the name of the tab
tabControl.add(tab1, text='Main')
tab2=MainFrameTab2(tabControl)
tabControl.add(tab2, text='Priming')
tabControl.pack(expand=1, fill="both")
#mainFrame=MainFrame(root)
#mainFrame.grid()

tkinterRefresher=TkinterRefresher(tab1)
#We launch the pressure control
#guiTC=guiThermalCamera(tab1)
#t = threading.Thread(target=guiTC.startGui(), args={}, kwargs={})
#t.start()

root.mainloop()