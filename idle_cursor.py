import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import time
from sudoku.sudoku_cursor import SudokuCursor
from xo.xo_cursor import XoCursor
from checkers.checkers_cursor import CheckersCursor
from screen_info import screen_height, screen_width, initial_y, initial_x, cale_catre_resurse
import os
import sys
import keyboard
import threading
import math


class Cursor:

    def __init__(self):
        self.xc, self.sdc, self.cc = None, None, None
        self.root = None

        cursor_path = os.path.join(cale_catre_resurse, "cursor1.png")
        image = Image.open(cursor_path)
        image = image.resize((60, 73), Image.NEAREST)
        self.tk_image = ImageTk.PhotoImage(image)


    def go_to_destination(self, dest_x, dest_y):

        cx = self.root.winfo_x()
        cy = self.root.winfo_y()
        step = 5
        dist = math.sqrt((dest_x - cx) ** 2 + (dest_y - cy) ** 2)
        if dist < step:
            self.root.geometry(f"+{dest_x}+{dest_y}")

            self.root.focus_force()

        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")
            self.root.after(2, self.go_to_destination, dest_x, dest_y)

    def lanseaza(self, main_x, main_y):
        response_time = time.time()
        self.root = tk.Toplevel()
        self.root.title("SecondCursor")
        self.root.geometry(f"60x73+{main_x}+{main_y}")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "#008000")

        label = tk.Label(self.root, image=self.tk_image, bg="white")
        label.pack()

        print(f"timp tkinter1: {time.time() - response_time}")

        self.root.update()
        self.go_to_destination(initial_x, initial_y)

        def sudoku_solver(event=None):

            self.root.unbind("q")
            self.root.unbind("w")
            self.root.unbind("x")
            self.root.unbind("s")
            self.root.unbind("c")
            self.sdc = SudokuCursor(self.root)

            self.sdc.move_to_square()

        def xo_solver(event=None):

            self.root.unbind("q")
            self.root.unbind("w")
            self.root.unbind("s")
            self.root.unbind("x")
            self.root.unbind("c")

            self.xc = XoCursor(self.root)

            self.xc.move_to_square()

        def checkers_solver(event=None):

            self.root.unbind("q")
            self.root.unbind("w")
            self.root.unbind("s")
            self.root.unbind("x")
            self.root.unbind("c")

            self.cc = CheckersCursor(self.root)

            self.cc.move_to_square()

        def stop_cursor(event=None):
            print("se incearca")
            if self.xc is not None:
                self.xc.stop_cursor()
            if self.sdc is not None:
                self.sdc.stop_cursor()
            if self.cc is not None:
                self.cc.stop_cursor()

        def rebind_cursor(event=None):
            print("rebinding")
            self.root.bind("s", sudoku_solver)
            self.root.bind("x", xo_solver)
            self.root.bind("c", checkers_solver)

        keyboard.hook_key("esc", stop_cursor)
        self.root.bind("s", sudoku_solver)
        self.root.bind("x", xo_solver)
        self.root.bind("c", checkers_solver)
        self.root.bind("<<Rebind>>", rebind_cursor)


        print("Ia uite unde sa ajuns")

    def opreste(self,dest_x,dest_y):
        self.root.destroy()

    def cleanup(self):

        if self.xc:
            self.xc.stop_cursor()

        if self.sdc:
            self.sdc.stop_cursor()

        if self.cc:
            self.cc.stop_cursor()


        keyboard.unhook_all()
        keyboard.unhook_all_hotkeys()


        if self.root is not None:
            try:
                self.root.destroy()
            except tk.TclError:
                pass