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
from cursor_helper import RealCursor
from xo.xo_detector import XoDetector
from xo.xo_solver import XoSolver

class XoCursor:
    def __init__(self,root):
        self.puncte=[[[]]]
        self.careu=[[]]
        self.careu_copy=[[]]
        self.segmente=[[]]
        self.medii=[[]]
        self.root=root
        self.rc=RealCursor()
        self.stop=False
        self.liber=0
        self.bottom_right=[]
        self.top_left=[]
        self.detector=XoDetector()
        self.done=threading.Event()
        self.stop_wait=False
        self.turn='player'
        self.solver=XoSolver()
        self.ev=threading.Event()
        self.bot_turn=threading.Event()
        self.player_turn=threading.Event()
        self.thread1_stopped=threading.Event()
        self.thread2_stopped=threading.Event()
        self.oprite=2
        self.clicked_patch=[]
        self.click_listener=None

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
            self.root.bind("q", lambda event: self.play_against_bot())
            self.root.bind("w", lambda event: self.play_against_user())
            self.root.focus_force()
            self.oprite += 1
        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")

            self.root.after(2, self.go_to_destination, dest_x, dest_y)





    def move_to_square(self):
        screenshot = ImageGrab.grab()
        screenshot.save("C:/Users/mihae/OneDrive/Desktop/temp/ss.png")
        screenshot.close()
        imagine = cv.imread("C:/Users/mihae/OneDrive/Desktop/temp/ss.png")

        self.puncte, self.segmente, self.medii,self.bottom_right,self.top_left=self.detector.get_xo(imagine)
        if(self.puncte is None):
            self.root.event_generate("<<Rebind>>")
            return
        self.careu = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
        ]
        self.careu_copy=copy.deepcopy(self.careu)
        self.liber=9
        self.bot_turn.set()
        self.player_turn.clear()
        self.oprite-=1
        self.go_to_destination(self.bottom_right[0], self.bottom_right[1])


    def go_click(self, dest_x, dest_y):

        if self.stop:
            self.root.geometry(f"+{1850}+{940}")
            self.done.set()
            return
        cx = self.root.winfo_x()
        cy = self.root.winfo_y()
        step = 5
        dist = math.sqrt((dest_x - cx) ** 2 + (dest_y - cy) ** 2)
        if dist < step:
            self.root.geometry(f"+{dest_x}+{dest_y}")
            ogPos = self.rc.get_cursor_position()
            self.rc.set_cursor_position([int(dest_x-5),int(dest_y-5)])

            self.rc.click()
            self.rc.set_cursor_position(ogPos)
            self.root.geometry(f"+{self.bottom_right[0]}+{self.bottom_right[1]}")
            self.done.set()

            self.root.focus_force()
        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")

            self.root.after(2, self.go_click, dest_x, dest_y)

    def wait_for_change(self):
        while (True):
            self.player_turn.wait()
            self.player_turn.clear()

            if(self.stop_wait):
                self.thread1_stopped.set()
                print("Thread 1 done")
                return


            start=time.time()
            while True:
                if (self.stop_wait ):
                    break
                if (time.time()-start>5.0):
                    print("mno bine")
                    self.bot_turn.set()
                    break
                screenshot = ImageGrab.grab()
                imagine = np.array(screenshot)
                imagine = cv.cvtColor(imagine, cv.COLOR_RGB2GRAY)
                i,j = self.detector.verifica_schimbare(imagine, self.segmente, self.medii, self.careu)
                if i!=-1:

                    self.careu[i][j] = 'o'
                    self.careu_copy[i][j] = 'o'
                    print("schimbare bot: ", i, j)
                    self.liber -= 1
                    time.sleep(1)
                    self.bot_turn.set()

                    break
                time.sleep(0.1)

    def on_click(self,x, y, button, pressed):
        conditie1 = button == mouse.Button.left
        conditie2 = pressed == True
        conditie3 = self.top_left[0] < x < self.bottom_right[0] and self.top_left[1] < y < self.bottom_right[1]
        if conditie1 and conditie2 and conditie3:
            for i in range(3):
                for j in range(3):
                    if self.segmente[i][j][2]<x<self.segmente[i][j][3] and self.segmente[i][j][0]<y<self.segmente[i][j][1] and self.careu[i][j]=='_':
                        self.clicked_patch=[i,j]

                        return False


    def wait_for_user(self):
        while (True):
            self.player_turn.wait()
            self.player_turn.clear()
            print("waiting for user playx")
            if(self.stop_wait):
                self.thread1_stopped.set()
                print("Thread 1 done")
                return
            while True:
                if (self.stop_wait):
                    break
                self.click_listener= mouse.Listener(on_click=self.on_click)
                self.click_listener.start()

                self.click_listener.join()
                if (self.stop_wait):
                    break
                i,j=self.clicked_patch[0],self.clicked_patch[1]

                time.sleep(0.5)
                screenshot = ImageGrab.grab()
                imagine = np.array(screenshot)
                imagine = cv.cvtColor(imagine, cv.COLOR_RGB2GRAY)

                if self.detector.patch_schimbat(imagine, self.segmente[i][j], self.medii[i][j]):
                    self.careu[i][j] = 'o'
                    self.careu_copy[i][j] = 'o'
                    print("schimbare bot: ", i, j)
                    self.liber -= 1
                    break

            time.sleep(1)
            self.bot_turn.set()






    def wait_for_move(self,enemy):
        while True:


            self.bot_turn.wait()
            self.bot_turn.clear()

            if (self.stop_wait):
                self.thread2_stopped.set()
                print("Thread 2 done")
                return

            i,j=self.solver.findBestMove(self.careu_copy)
            if i==-1:
                continue

            self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1]))
            self.done.wait()
            self.done.clear()
            self.careu[i][j]='x'
            self.careu_copy[i][j] = 'x'
            self.liber -= 1
            if enemy=='bot':
                time.sleep(1)
            else:
                time.sleep(0.1)
            print("schimbare player: ", i, j)
            self.player_turn.set()


    def check_if_done(self):
        while(True):
            #print("ok")
            if (self.liber <= 0 or self.solver.evaluate(self.careu) != 0 or self.stop==True):
                self.thread1_stopped.clear()
                self.thread2_stopped.clear()

                self.stop_wait = True
                self.player_turn.set()

                self.thread1_stopped.wait()
                self.thread1_stopped.clear()
                self.bot_turn.set()

                self.thread2_stopped.wait()
                self.thread2_stopped.clear()
                print("Thread 3 done")
                return
            time.sleep(0.1)

    def playing_best_out_of_n(self,nr_of_rounds,type):
        for i in range(nr_of_rounds):
            if(self.stop==True):

                break
            self.done.clear()
            first_turn=self.turn
            if type=='bot':
                t1 = threading.Thread(target=self.wait_for_change,daemon=True)
            else:
                t1=threading.Thread(target=self.wait_for_user,daemon=True)
            t2 = threading.Thread(target=self.wait_for_move,args=(type,),daemon=True)
            t3= threading.Thread(target=self.check_if_done,daemon=True)
            t3.start()
            t1.start()
            t2.start()
            t2.join()
            t1.join()
            t3.join()



            self.stop_wait=False
            self.careu = [
                ['_', '_', '_'],
                ['_', '_', '_'],
                ['_', '_', '_']
            ]
            self.careu_copy=[
                ['_', '_', '_'],
                ['_', '_', '_'],
                ['_', '_', '_']
            ]
            self.liber = 9
            if first_turn=='player':
                self.turn='bot'
            else:
                self.turn='player'
            if self.turn=='player':
                self.bot_turn.set()
                self.player_turn.clear()
            else:
                self.bot_turn.clear()
                self.player_turn.set()
            while True:
                if (self.stop == True):
                    break
                screenshot = ImageGrab.grab()
                imagine = np.array(screenshot)
                imagine = cv.cvtColor(imagine, cv.COLOR_RGB2GRAY)
                gata=self.detector.verifica_joc_nou(imagine, self.segmente, self.medii)
                if gata:
                    print("gata")
                    break
                time.sleep(0.1)
        print("best out of 5 done")
        if(not self.stop):
            self.root.bind("q", lambda event: self.play_against_bot())
            self.root.bind("w", lambda event: self.play_against_user())

        self.oprite+=1

    def play_against_bot(self):
        self.root.unbind("q")
        self.root.unbind("w")
        nr_of_rounds=3
        self.oprite-=1
        main_thread=threading.Thread(target=self.playing_best_out_of_n,args=(nr_of_rounds,'bot'),daemon=True)
        main_thread.start()


    def play_against_user(self):
        self.root.unbind("q")
        self.root.unbind("w")
        nr_of_rounds = 3
        self.oprite -= 1
        main_thread = threading.Thread(target=self.playing_best_out_of_n, args=(nr_of_rounds, 'user'), daemon=True)
        main_thread.start()

    def stop_cursor(self):
        self.root.unbind("q")
        self.root.unbind("w")
        self.stop=True
        self.stop_wait=True
        if self.click_listener is not None and self.click_listener.running:
            self.click_listener.stop()
        while(True):

            if(self.oprite==2):
                break
            time.sleep(0.5)
        print("totul oprit")
        self.root.geometry(f"+{1850}+{940}")
        self.root.event_generate("<<Rebind>>")
        self.stop=False


