"""
This module handles extracting well temperatures from Optris images
"""
from  Optris import *
import numpy as np
#import imageio
from pathlib import Path
from typing import Union
import logging
import time
from matplotlib import pyplot as plt
import threading
from PIL import Image, ImageTk
import datetime
import os
from time import *
from elementaryFunctions import goToWell

__all__ = ['ThermalImage', 'ThermalImageParams', 'default_TheramlImageParams']

class ThermalImageParams:
    def __init__(self):
        self.origin: np.ndarray = None    # [x, y] coordinates of A, 1 origin
        self.gridsize: np.ndarray = None  # [xs, ys] Number of wells in x, y
        self.wellsize: int = None         # [px] Number of pixels around centers to average for a well (square)
        self.p1: np.ndarray = None
        self.p2: np.ndarray = None

# When calibrating, edit these parameters and they will be updated in the matplotlib gui
# Then transfer them to the appropriate BB config.
default_TheramlImageParams = ThermalImageParams()
# default_TheramlImageParams.p1 = np.array([18, 32.5, 1.0])
# default_TheramlImageParams.p2 = np.array([147, 31.5, 1.0])
default_TheramlImageParams.p1 = np.array([13, 8, 1.0])
default_TheramlImageParams.p2 = np.array([139.5, 9, 1.0])

default_TheramlImageParams.gridsize = np.array((12, 8))
default_TheramlImageParams.wellsize = 1

class ThermalImage:
    """
    Represent and translate an optris thermal image
    """
    def __init__(self, img: np.ndarray, params: ThermalImageParams):
        """
        :param img: Input image
        :param params: Interpertation paramters
        """
        self.params = params
        self.img = img
        #self.img=np.rot90(self.img)
        #self.img=np.rot90(self.img)
        # Compute spacing
        hypot = self.params.p2-self.params.p1
        self.spacing = np.hypot(hypot[0], hypot[1])/11.0
        logging.info("Spacing: %.2f", self.spacing)
        self.theta = -np.arctan2(hypot[1], hypot[0])
        logging.info("Theta: %.3f", self.theta)

        # Affine transform of grid array
        self.t = np.array([[np.cos(self.theta),-np.sin(self.theta), params.p1[1]],
                           [np.sin(self.theta),  np.cos(self.theta), params.p1[0]],
                           [0.0,                 0.0,                1.0]])
        # for i in range(self.t.shape[0]):
        #     for j in range(self.t.shape[1]):
        #         self.t[i, j]=round(self.t[i,j])
        self.fig = None
        return

    def center(self, c: int, r: int) -> np.ndarray:
        """
        Given well c, r return image x, y center
        """
        params = self.params
        if not 0 <= c <= params.gridsize[0] or not 0 <= r <= params.gridsize[1]:
            raise ValueError
        p = params.p1.copy()
        p += [c * self.spacing, r * self.spacing, 0.0]
        y, x, _ = np.dot(p, self.t)
        return np.array((x, y))

    def as_array(self) -> np.ndarray:
        """
        Return the means of the whole plate as an np array
        :return:
        """
        data = np.zeros(self.params.gridsize)

        for c in range(self.params.gridsize[0]):
            for r in range(self.params.gridsize[1]):
                data[c, r] = self.well_mean(c, r)
        return data

    def as_list(self) -> np.ndarray:
        data = []

        for c in range(self.params.gridsize[0]):
            for r in range(self.params.gridsize[1]):
                data.append('{0:.2f}'.format(self.well_mean(c, r)))
        return data



    def well_as_array(self, c: int, r: int) -> np.ndarray:
        """
        Given a well c, r return just the well pixels
        """
        s = self.params.wellsize
        x, y = self.center(c, r)
        x = int(x)
        y = int(y)
        ret = self.img[x-s:x+s+1, y-s:y+s+1]
        return ret

    def well_mean(self, c: int, r: int) -> float:
        """
        Given a well c, r return the mean of the well pixels
        """
        return self.well_as_array(c, r).mean()

    def well_std(self, c: int, r: int) -> float:
        """
        Given a well c, r return the stddev of the well pixels
        """
        return self.well_as_array(c, r).std()

    def plotimage(self):
        """
        Draw the image
        """

        plt.imshow(self.img)
        plt.show()
        #self.to_csv("Practice") #name file here will save to DNAS-BB-Software/DNASBB folder

    def to_csv(self, fname: Union[Path, str]):
        """
        Save the whole plate as a csv file
        :param fname:
        :return:
        """

        timestr=time.strftime("%Y%d%m_%H%M%S") #saves yeardaymonth-time
        fname=r'C:\Users\BREADBOARD1\Desktop\Thermal_CAM\ ' + fname+"_" +timestr+'.csv'

        np.savetxt(fname, self.as_array().transpose(), delimiter=',', fmt='%.2f')
        return


    def to_png(self,fname: Union[Path, str]):
        timestr = time.strftime("%Y%d%m_%H%M%S")  # saves yeardaymonth-time
        fname = r'C:\Users\BREADBOARD1\Desktop\Thermal_CAM\ ' + fname + "_" + timestr + '.png'
        plt.imsave(fname,self.img)


class ThermalImageThread:

    def __init__(self, rightFrame):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.o = Optris()
        self.thermalFrame = None    #Contains temperature data
        self.topng = None    #the frame we'll save as png
        self.frame = None   #the frame we show on the gui
        self.thermalFrame=None
        self.thread = None
        self.stopEvent = None
        self.rightFrame=rightFrame
        #ColorMap
        self.cm = plt.get_cmap('seismic')
        #Zoom Factor
        self.zoom=3

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, daemon=True)
        self.thread.start()
        #self.videoLoop()

    def videoLoop(self):

        while not self.stopEvent.is_set():

            try:


                self.thermalFrame=self.o.img()

                frame=self.thermalFrame
                #frame=frame.clip(frame.max()-10,frame.max())
                frame=(frame-frame.min())*(60.0/(frame.max()-frame.min()))
                frame=Optris.C_to_uint8(self.o,frame)

                ti = ThermalImage(self.cm(frame), default_TheramlImageParams)
                frame = Image.fromarray((ti.img[:, :, :3] * 255).astype(np.uint8)).resize((160*self.zoom,120*self.zoom))
                self.topng = frame
                self.frame = ImageTk.PhotoImage(frame)

                self.rightFrame.ImageLabel.configure(image=self.frame)
                self.rightFrame.ImageLabel.Image=self.frame

                #-5 pour le padx pady
                x = (self.rightFrame.ImageLabel.winfo_pointerx()-5-self.rightFrame.ImageLabel.winfo_rootx())/self.zoom
                y = (self.rightFrame.ImageLabel.winfo_pointery()-5-self.rightFrame.ImageLabel.winfo_rooty())/self.zoom

                if x<160 and x >-1:
                    if y<120 and y>-1:
                        self.rightFrame.tempLabel.configure(text=str(self.rightFrame.thermalThread.thermalFrame[int(y)][int(x)]) + "°C")

                self.rightFrame.update()
                sleep(0.05)

            #self.rightFrame.after(50,self.videoLoop)

            except:
                print('Couldnt update frame')
                #self.rightFrame.after(50, self.videoLoop)

    def snapshot_in_cycle(self,thermalImages,folder_path,cycle,step):
        #try:

            #if thermalImages are not active, we return
            if thermalImages==0 or self.rightFrame.parent.hardware.thermalCam==0:
                return

            # If it's just a test we dont take pictures
            if (folder_path[len(folder_path) - 4:] == "test"):
                return

            #We go to thermal cam pos
            goToWell(self.rightFrame.parent.hardware,'thermalCamera',1,0)

            sleep(1)
            root_path = "C:\\Users\\Prototype 4\\Desktop\\Prototype4\\Thermal_Camera"

            now = datetime.datetime.now()

            final_path = root_path + "\\" + folder_path + "\\" + str(cycle) + "\\" + str(now.year) + force2digits(
                now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
                now.second) + '_C' + str(cycle) + '_' + step
            os.makedirs(root_path + "\\" + folder_path + "\\" + str(cycle), exist_ok=True)



            imageio.imwrite(final_path + ".png", self.topng)
            #imageio.imwrite(final_path+"_Temp.png", self.thermalFrame.astype(np.uint8))
            np.savetxt(final_path + ".csv", self.thermalFrame, delimiter=';', fmt='%.2f')

        #except:
            #print('Couldnt take snapshot')


class FakeThermalImageThread:

    def __init__(self):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        variable='just to have a variable'

    def snapshot_in_cycle(self, thermalImages, folder_path, cycle, step):
        variable='snap'

def frameFormatting(frame):
    for pixel in frame:
        if pixel<30 :
            pixel=30

def force2digits(number):
    if number<10:
        return '0'+str(number)
    else:
        return str(number)


if __name__ == '__main__':
    import logging
    logging.disable()
    # img = imageio.imread('cam2.png')
    o = Optris()
    img = o.img()
    params = default_TheramlImageParams

    ti = ThermalImage(img, params)

    # for c in range(params.gridsize[0]):
    #     for r in range(params.gridsize[1]):
    #         x, y = ti.center(c, r)
    #         x = int(x)
    #         y = int(y)
    #         # print("Well at: %d, %d:\n%s\nMean: %.2f Std: %.2f\n" %
    #         #       (x, y, ti.well_as_array(c, r), ti.well_mean(c, r), ti.well_std(c, r)))
    #         try:
    #             oc = ti.img[x,y]
    #             s = params.wellsize
    #             ti.img[x-s:x+s+1, y-s:y+s+1] = 0
    #             ti.img[x,y] = oc
    #         except IndexError:
    #             logging.error("Point off image")
    #             pass
    #
    #     # ti.img[5, 5] = 255

    ti.plotimage()
    # ti.plotimage()
    # ti.to_csv('cam2')
