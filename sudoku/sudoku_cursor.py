import tkinter as tk
from PIL import Image, ImageTk,ImageGrab
import ctypes
import math
import time
import cv2 as cv
import numpy as np
import os
import threading

from cursor_helper import RealCursor

from sudoku.sudoku_detector import Sudoku
from sudoku.sudoku_mask import SudokuMask

class SudokuCursor:

    def __init__(self,root):
        self.puncte=[[]]
        self.complet=[[]]
        self.incomplet=[[]]
        self.bottom_right=[]
        self.top_left=[]
        self.root=root
        self.rc=RealCursor()
        self.stop=False
        self.mask=SudokuMask()
        self.nr_incomplet=0
        self.oprite=4

    def go_to_destination(self,dest_x,dest_y):
        if self.stop:
            self.root.geometry(f"+{1850}+{940}")
            self.oprite+=1
            return
        cx = self.root.winfo_x()
        cy = self.root.winfo_y()
        step = 5
        dist = math.sqrt((dest_x - cx) ** 2 + (dest_y - cy) ** 2)
        if dist < step:
            self.root.geometry(f"+{dest_x}+{dest_y}")
            self.root.bind("q", lambda event: self.solve_whole_sudoku())
            self.root.bind("w", lambda event: self.solve_one_by_one())

            self.root.focus_force()
            self.oprite += 1
        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")
            self.root.after(2, self.go_to_destination, dest_x, dest_y)



    def move_to_square(self):

        screenshot = ImageGrab.grab()
        screenshot.save("C:/Users/mihae/OneDrive/Desktop/temp/ss.jpg")
        screenshot.close()
        imagine = cv.imread("C:/Users/mihae/OneDrive/Desktop/temp/ss.jpg")
        sdk=Sudoku()
        self.puncte,self.incomplet,self.complet,self.top_left,self.bottom_right=sdk.rezolva(imagine)
        if(self.puncte is None or self.complet is None):
            self.root.event_generate("<<Rebind>>")
            return
        self.mask.set_mask(self.top_left,self.bottom_right)
        self.nr_incomplet=np.count_nonzero(self.incomplet == 0)
        self.oprite-=1
        self.go_to_destination(self.bottom_right[0],self.bottom_right[1])
        print("colturi: ",self.top_left,self.bottom_right)
        print("incomplet: ",self.incomplet.tolist())
        print("complet: ",self.complet)


    def click_and_set(self, move):
        ogPos = self.rc.get_cursor_position()
        self.rc.set_cursor_position([int(a-5) for a in move[:2]])

        self.rc.click()
        time.sleep(0.01)
        self.rc.set_cursor_position(ogPos)
        self.rc.press_key(str(move[2]))



    def go_through_sudoku(self,moves):

        l=len(moves)
        if l==0:
            self.oprite += 1
            self.root.geometry(f"+{1850}+{940}")
            self.root.event_generate("<<Rebind>>")
            return


        if self.stop:
            print("bine bine")

            self.oprite += 1
            self.root.geometry(f"+{1850}+{940}")
            return
        cx = self.root.winfo_x()
        cy = self.root.winfo_y()
        step = 5

        dist = math.sqrt((moves[l-1][0] - cx) ** 2 + (moves[l-1][1] - cy) ** 2)

        if dist < step:
            self.root.geometry(f"+{moves[l-1][0]}+{moves[l-1][1]}")

            self.click_and_set(moves[l-1])
            moves.pop()

            self.root.after(100, self.go_through_sudoku, moves)
        else:
            new_x = int(cx + ((moves[l-1][0] - cx) / dist) * step)
            new_y = int(cy + ((moves[l-1][1] - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")
            self.root.after(2, self.go_through_sudoku, moves)




    def solve_whole_sudoku(self):
        print(self.oprite)
        self.root.unbind("q")
        self.root.unbind("w")
        moves=[]
        for i in range(8,-1,-1):
            for j in range(8,-1,-1):
                if (self.incomplet[i][j] == 0):
                    moves.append([self.puncte[i][j][0], self.puncte[i][j][1],self.complet[i][j]])
                    self.incomplet[i][j]=self.complet[i][j]
        self.oprite-=1
        self.go_through_sudoku(moves)

    def go_set_digit(self,dest_x,dest_y,key):
        if self.stop:
            self.root.geometry(f"+{1850}+{940}")
            self.oprite+=1
            return
        cx = self.root.winfo_x()
        cy = self.root.winfo_y()
        step = 5
        dist = math.sqrt((dest_x - cx) ** 2 + (dest_y - cy) ** 2)
        if dist < step:
            self.root.geometry(f"+{dest_x}+{dest_y}")
            self.click_and_set([dest_x,dest_y,key])
            self.oprite+=1
            if self.nr_incomplet == 0:

                self.root.geometry(f"+{1850}+{940}")
                self.root.event_generate("<<Rebind>>")
                return
            self.oprite -= 1
            self.go_to_destination(self.bottom_right[0],self.bottom_right[1])

        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")
            self.root.after(2, self.go_set_digit, dest_x, dest_y,key)
    def solve_one_by_one(self):
        self.root.unbind("q")
        self.root.unbind("w")
        self.oprite-=1
        while True:
            self.mask.run()

            if self.stop:
                break
            x_punct,y_punct=self.mask.coord
            if self.incomplet[x_punct][y_punct]==0:
                self.nr_incomplet-=1
                self.incomplet[x_punct][y_punct]=self.complet[x_punct][y_punct]

                self.go_set_digit(self.puncte[x_punct][y_punct][0], self.puncte[x_punct][y_punct][1],self.complet[x_punct][y_punct])


                break


    def stop_cursor(self):
        self.root.unbind("q")
        self.root.unbind("w")
        self.stop=True
        while(True):
            print(self.oprite)
            if self.oprite==4:
                break
            time.sleep(0.1)
        print("Toate oprite")
        self.root.geometry(f"+{1850}+{940}")
        self.root.event_generate("<<Rebind>>")
        self.stop=False



