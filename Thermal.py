"""
This module handles extracting well temperatures from Optris images
"""
from Optris import *
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
import cv2 as cv
import pandas as pd
import pickle
from MTM import matchTemplates


#from action import thermal_is384
__all__ = ['ThermalImage', 'ThermalImageParams', 'default_TheramlImageParams']
thermal_is384 = 0
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
        self.thermal_is384 = thermal_is384
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
        self.zoom=1.2
        self.width=382
        self.height=288

        if self.thermal_is384:
            protoTF = 305
            self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
        else:
            protoTF = 5
            self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        db_template = pickle.load(open('db_template_proto' + str(protoTF) + '.p', "rb"))

        self.listTemplate = db_template['listTemplates']
        self.dictTemplates = db_template['dictTemplates']
        self.line_coordinates = db_template['line_coordinates']
        self.column_coordinates = db_template['column_coordinates']
        self.detection_limit = db_template['detection_limit']

        self.nb_numbers = len(self.line_coordinates)
        self.nb_letters = len(self.column_coordinates)

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, daemon=True)
        self.thread.start()
        #self.videoLoop()

    def in_video_loop(self):
        self.thermalFrame = self.o.img()

        frame = self.thermalFrame
        # frame=frame.clip(frame.max()-10,frame.max())
        frame = (frame - frame.min()) * (60.0 / (frame.max() - frame.min()))
        frame = Optris.C_to_uint8(self.o, frame)

        ti = ThermalImage(self.cm(frame), default_TheramlImageParams)
        frame = Image.fromarray((ti.img[:, :, :3] * 255).astype(np.uint8)).resize((int(self.width * self.zoom), int(self.height * self.zoom)))
        self.topng = frame
        #self.img_to_display = np.array(self.topng)
        # self.frame = ImageTk.PhotoImage(frame)
        self.mean_temperature()
        self.frame = ImageTk.PhotoImage(Image.fromarray(self.img_to_display.astype(np.uint8)))

        self.rightFrame.ImageLabel.configure(image=self.frame)
        self.rightFrame.ImageLabel.Image = self.frame

        # moins quelque chose pour le décalage
        x = (self.rightFrame.ImageLabel.winfo_pointerx() - 11 - self.rightFrame.ImageLabel.winfo_rootx()) / self.zoom
        y = (self.rightFrame.ImageLabel.winfo_pointery() - 8 - self.rightFrame.ImageLabel.winfo_rooty()) / self.zoom

        if x < self.width and x > -1:
            if y < self.height and y > -1:
                self.rightFrame.tempLabel.configure(
                    text=str(self.rightFrame.thermalThread.thermalFrame[int(y)][int(x)]) + "°C")

        self.rightFrame.update()
        sleep(0.05)

    def videoLoop(self):
        while not self.stopEvent.is_set():
            #try:
            self.in_video_loop()
            #except:
            #    print('Couldnt update frame')
                #self.rightFrame.after(50, self.videoLoop)

    def snapshot_in_cycle(self,thermalImages,folder_path,cycle,step):
        try:

            #if thermalImages are not active, we return
            if thermalImages==0 or self.rightFrame.parent.hardware.thermalCam==0:
                return

            # If it's just a test we dont take pictures
            if (folder_path[len(folder_path) - 4:] == "test"):
                return

            #We go to thermal cam pos
            goToWell(self.rightFrame.parent.hardware,'thermalCamera',1,0)

            sleep(0.3)
            self.in_video_loop()

            root_path = "C:\\Users\\SynthesisDNASCRIPT\\Desktop\\Proto6\\Thermal_Camera"

            now = datetime.datetime.now()

            final_path = root_path + "\\" + folder_path + "\\" + str(cycle) + "\\" + str(now.year) + force2digits(
                now.month) + force2digits(now.day) + '_' + force2digits(now.hour) + force2digits(now.minute) + force2digits(
                now.second) + '_C' + str(cycle) + '_' + step
            os.makedirs(root_path + "\\" + folder_path + "\\" + str(cycle), exist_ok=True)



            imageio.imwrite(final_path + ".png", self.img_to_display)
            #imageio.imwrite(final_path + "_detection.png", self.img_to_display)
            #imageio.imwrite(final_path+"_Temp.png", self.thermalFrame.astype(np.uint8))


            self.generate_temperature_table(final_path)
            np.savetxt(final_path + ".csv", self.thermalFrame, delimiter=';', fmt='%.2f')

        except:
            print('Couldnt take snapshot')

    def generate_temperature_table(self, final_path):
        wells_dict = {'Temperatures': self.letters}

        input_img = np.array(self.topng)
        img_c = input_img
        input_img = cv.cvtColor(input_img, cv.COLOR_BGR2GRAY)
        img_p, img_q = input_img.shape[0], input_img.shape[1]
        img_for_matching = input_img[self.detection_limit[0]:self.detection_limit[1], :]

        hits = matchTemplates(self.listTemplate,
                              img_for_matching,
                              score_threshold=0,
                              N_object=1,
                              method=cv.TM_CCOEFF_NORMED,
                              maxOverlap=0)
        dictTemplate = self.dictTemplates[hits[:1]['TemplateName'].values[0]]
        w = dictTemplate['width']
        h = dictTemplate['height']
        offset_line = dictTemplate['base_line']
        offset_column = dictTemplate['base_column']

        top_left0 = hits[:1]['BBox'].values[0][:2]
        top_left = (top_left0[0], top_left0[1] + self.detection_limit[0])

        bottom_right = (top_left[0] + w, top_left[1] + h)

        line_coordinates_shifted = self.line_coordinates + top_left[1] - offset_line
        column_coordinates_shifted = self.column_coordinates + top_left[0] - offset_column

        temperature_table = self.thermalFrame
        xl_p, xl_q = temperature_table.shape[0], temperature_table.shape[1]
        fp, fq = img_p / xl_p, img_q / xl_q

        idx = 0
        for n in range(self.nb_numbers):
            idx += 1
            wells_dict[idx] = []
            for m in range(self.nb_letters):
                x = column_coordinates_shifted[m, n]
                y = line_coordinates_shifted[n, m]
                try:
                    wells_dict[idx].append(temperature_table[int(y / fp), int(x/fq)])
                except:
                    wells_dict[idx].append(None)

        df = pd.DataFrame(wells_dict)
        df.to_excel(final_path + '_wells.xlsx', sheet_name='temp_table', index=False)

    def mean_temperature(self):
        temperatures = []
        self.img_to_display = np.array(self.topng)
        img_p, img_q = self.img_to_display.shape[0], self.img_to_display.shape[1]
        input_img = cv.cvtColor(self.img_to_display, cv.COLOR_BGR2GRAY)
        img_for_matching = input_img[self.detection_limit[0]:self.detection_limit[1], :]

        hits = matchTemplates(self.listTemplate,
                              img_for_matching,
                              score_threshold=0,
                              N_object=1,
                              method=cv.TM_CCOEFF_NORMED,
                              maxOverlap=0)

        dictTemplate = self.dictTemplates[hits[:1]['TemplateName'].values[0]]
        w = dictTemplate['width']
        h = dictTemplate['height']
        offset_line = dictTemplate['base_line']
        offset_column = dictTemplate['base_column']

        top_left0 = hits[:1]['BBox'].values[0][:2]
        top_left = (top_left0[0], top_left0[1] + self.detection_limit[0])

        bottom_right = (top_left[0] + w, top_left[1] + h)

        line_coordinates_shifted = self.line_coordinates + top_left[1] - offset_line
        column_coordinates_shifted = self.column_coordinates + top_left[0] - offset_column
        xl_p, xl_q = self.thermalFrame.shape
        fp, fq = img_p / xl_p, img_q / xl_q
        # Comment the next line to avoid displaying the green rectangle around the handle
        #cv.rectangle(self.img_to_display, top_left, bottom_right, (0, 255, 0), 2)
        for n in range(self.nb_numbers):
            for m in range(self.nb_letters):
                x = int(column_coordinates_shifted[m, n])
                y = int(line_coordinates_shifted[n, m])
                # Comment the next line to avoid displaying the green circles on the wells
                #self.img_to_display = cv.circle(self.img_to_display, (x, y), radius=2, color=(0, 255, 0), thickness=-1)
                try:
                    temperatures.append(self.thermalFrame[int(y / fp), int(x/fq)])
                except:
                    pass
        self.rightFrame.tempmeanLabel.configure(text="Mean temperature " + str(round(np.mean(temperatures), 2)) + "°C")

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
