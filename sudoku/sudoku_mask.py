import tkinter as tk
from PIL import Image, ImageTk,ImageGrab
import ctypes
import math
import time
import cv2 as cv
import numpy as np
import os

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class SudokuMask:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Grila")
        self.root.wm_attributes("-alpha", 0.0)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.coord=[0,0]


    def button_pressed(self,i,j):
        self.root.wm_attributes("-alpha", 0.0)
        self.coord=[i,j]
        self.root.quit()
    def set_mask(self,top_left,bottom_right):
        self.root.geometry(
            f"{bottom_right[0] - top_left[0]}x{bottom_right[1] - top_left[1]}+{top_left[0]}+{top_left[1]}")
        w = (bottom_right[0] - top_left[0]) // 9
        h = (bottom_right[1] - top_left[1]) // 9
        for i in range(9):
            for j in range(9):
                buton = tk.Button(self.root)
                buton.place(x=j * w, y=i * h, width=w, height=h)
                buton.bind("<Button-1>", lambda event, i=i, j=j: self.button_pressed(i, j))
        self.root.bind("<<Opreste>>", self.stop)
        self.root.bind("<<Ascunde>>", self.hide)
        self.root.bind("<<Arata>>", self.show)
    def run(self):
        self.root.wm_attributes("-alpha", 0.01)
        self.root.mainloop()

    def show(self):
        self.root.wm_attributes("-alpha",1.0)

    def hide(self):
        self.root.wm_attributes("-alpha", 0.0)

    def stop(self):
        self.root.quit()




