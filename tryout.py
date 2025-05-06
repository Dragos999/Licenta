import tkinter as tk
from PIL import Image, ImageTk,ImageGrab
import ctypes
import math
import time
import cv2 as cv
import numpy as np
import os
import threading
import copy
from pynput import mouse

careu1= [
    [0, 0, 0, -1, 0, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
careu2= [
    [0, 0, 0, -1, 0, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

print(careu1==careu2,flush=True)


print("bun")





"""
        i=0
        j=1

        img = imagine[self.segmente[i][j][0] :self.segmente[i][j][1] ,
              self.segmente[i][j][2] :self.segmente[i][j][3] ]
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        hist_h_referinta = cv.calcHist([img_hsv], [0], None, [180], [0, 180])
        hist_s_referinta = cv.calcHist([img_hsv], [1], None, [256], [0, 256])
        hist_v_referinta = cv.calcHist([img_hsv], [2], None, [256], [0, 256])

        for i in range(8):
            for j in range(8):

                img=imagine[self.segmente[i][j][0]:self.segmente[i][j][1],self.segmente[i][j][2]:self.segmente[i][j][3]]
                img_hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)
                hist_h = cv.calcHist([img_hsv], [0], None, [180], [0, 180])
                hist_s = cv.calcHist([img_hsv], [1], None, [256], [0, 256])
                hist_v = cv.calcHist([img_hsv], [2], None, [256], [0, 256])
                score1 = cv.compareHist(hist_h, hist_h_referinta, cv.HISTCMP_CORREL)
                score2 = cv.compareHist(hist_s, hist_s_referinta, cv.HISTCMP_CORREL)
                score3 = cv.compareHist(hist_v, hist_v_referinta, cv.HISTCMP_CORREL)
                print((score1+score2+score3)/3)
            print()"""