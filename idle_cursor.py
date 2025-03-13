import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import time
from sudoku.sudoku_cursor import SudokuCursor
from xo.xo_cursor import XoCursor
import os
import sys
import keyboard
import threading
response_time=time.time()


ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = tk.Tk()
initial_x,initial_y=1850,940

root.title("SecondCursor")
root.geometry(f"60x73+{initial_x}+{initial_y}")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "#008000")
image = Image.open("C:/Users/mihae/OneDrive/Desktop/cursor1.png")
image = image.resize((60, 73), Image.NEAREST)
tk_image = ImageTk.PhotoImage(image)
label = tk.Label(root, image=tk_image, bg="white")
label.pack()


print(f"timp tkinter1: {time.time()-response_time}")


xc,sdc=None,None


def sudoku_solver(event=None):
        global sdc
        root.unbind("q")
        root.unbind("w")
        root.unbind("x")
        root.unbind("s")
        sdc = SudokuCursor(root)

        sdc.move_to_square()


def xo_solver(event=None):
        global xc
        root.unbind("q")
        root.unbind("w")
        root.unbind("s")
        root.unbind("x")

        xc=XoCursor(root)

        xc.move_to_square()


def stop_cursor(event=None):

        global xc,sdc
        print(xc, sdc)
        if xc is not None:
                xc.stop_cursor()
        if sdc is not None:
                sdc.stop_cursor()

def rebind_cursor(event=None):
        print("rebinding")
        root.bind("s", sudoku_solver)
        root.bind("x", xo_solver)

keyboard.hook_key("esc",stop_cursor)
root.bind("s", sudoku_solver)
root.bind("x",xo_solver)
root.bind("<<Rebind>>",rebind_cursor)
root.mainloop()

