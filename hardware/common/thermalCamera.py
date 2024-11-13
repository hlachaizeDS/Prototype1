from pywinauto.application import Application
import os
import time
import datetime
from elementaryFunctions import *

import warnings
warnings.simplefilter('ignore', category=UserWarning)

class ThermalCamera():
    def __init__(self, parent,*args, **kwargs):
        self.parent = parent


    def snapshot(self,folder_path,file_path):

        goToWell(self.parent,"thermalCamera",1,0)

        app = Application().connect(title_re="Optris PI Connect")
        window = app.window(title_re="Optris PI Connect")
        window.type_keys("{F1}")
        window = app.window(title_re="Enregistrer sous")

        window = window.DirectUIHWND
        typebar = window.ComboBox2
        typebar.select("TIFF (*.tiff)")

        window = app.window(title_re="Enregistrer sous")
        root_path="C:\\Users\\Prototype\\Desktop\\Proto7\\Thermal_Camera"
        final_path=root_path + "\\" + folder_path + "\\" + file_path
        os.makedirs(root_path + "\\" + folder_path, exist_ok=True)


        window.type_keys(final_path)
        window.type_keys("{ENTER}")

    def snapshot_in_cycle(self,folder_path,cycle,step):
        try:

            #If it's just a test we dont take pictures
            if (folder_path[len(folder_path)-4:]=="test"):
                return

            goToWell(self.parent, "thermalCamera", 1, 0)

            app = Application().connect(title_re="Optris PI Connect")
            window = app.window(title_re="Optris PI Connect")
            window.type_keys("{F1}")
            window = app.window(title_re="Enregistrer sous")

            window = window.DirectUIHWND
            typebar = window.ComboBox2
            typebar.select("TIFF (*.tiff)")
            window = app.window(title_re="Enregistrer sous")

            root_path = "C:\\Users\\Prototype\\Desktop\\Proto7\\Thermal_Camera"

            now = datetime.datetime.now()

            final_path=root_path + "\\" + folder_path + "\\" + str(cycle) + "\\" + str(now.year) + force2digits(now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(now.second) + '_C' + str(cycle) + '_' + step
            os.makedirs(root_path + "\\" + folder_path + "\\" + str(cycle), exist_ok=True)


            window.type_keys(final_path)
            window.type_keys("{ENTER}")
        except:
            print('Couldnt take snapshot')

def force2digits(number):
    if number<10:
        return '0'+str(number)
    else:
        return str(number)

if __name__ == "__main__":
    # On crée la racine de notre interface
    root='ok'
    thermalCamera=ThermalCamera(root)
    thermalCamera.snapshot_in_cycle("test2",4,"DB2")
