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
from checkers.checkers_detector import CheckersDetector
import checkers.checkers_solver as cs

class CheckersCursor:
    def __init__(self,root):
        self.puncte=[[[]]]
        self.careu=[[]]
        self.careu_copy=[[]]
        self.segmente=[[]]
        self.medii=[[]]
        self.root=root
        self.rc=RealCursor()
        self.stop=False
        self.stop_wait = False
        self.oprite=1
        self.bottom_right=[]
        self.top_left=[]
        self.detector=CheckersDetector()
        self.bot_turn = threading.Event()
        self.player_turn = threading.Event()
        self.thread1_stopped = threading.Event()
        self.thread2_stopped = threading.Event()
        self.done=threading.Event()


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

            self.root.focus_force()
            self.oprite += 1

        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")

            self.root.after(2, self.go_to_destination, dest_x, dest_y)

    def move_to_square(self):
        screenshot = ImageGrab.grab()
        imagine = np.array(screenshot)
        imagine= cv.cvtColor(imagine, cv.COLOR_RGB2BGR)
        self.top_left, self.bottom_right, self.segmente, self.puncte, self.medii = self.detector.extrage_careu(imagine)

        if self.top_left is None:
            self.root.event_generate("<<Rebind>>")
            return

        self.careu=self.detector.determina_configuratie(imagine,self.segmente,[])
        if self.careu is None:
            print("configuratie careu invalida!")
            self.root.event_generate("<<Rebind>>")
            return
        elif not (sum( l.count(1) for l in self.careu)==sum( l.count(-1) for l in self.careu ) ==12) :
            print("configuratie careu invalida!")
            for i in range(8):
                for j in range(8):
                    print(self.careu[i][j], end=" ")
                print()
            self.root.event_generate("<<Rebind>>")
            return


        for i in range(8):
            for j in range(8):
                print(self.careu[i][j], end=" ")
            print()


        self.careu_copy=copy.deepcopy(self.careu)
        self.bot_turn.set()
        self.player_turn.clear()
        self.oprite -= 1
        self.go_to_destination(self.bottom_right[0], self.bottom_right[1])


    def wait_for_change(self):
        while (True):
            self.player_turn.wait()
            self.player_turn.clear()

            if(self.stop_wait):
                self.thread2_stopped.set()
                print("Thread 2 done")
                return


            careu_anterior=self.careu
            counter=0
            while True:
                if (self.stop_wait ):
                    break

                screenshot = ImageGrab.grab()
                imagine = np.array(screenshot)
                imagine = cv.cvtColor(imagine, cv.COLOR_RGB2BGR)
                self.careu_copy=self.detector.determina_configuratie(imagine,self.segmente,self.careu)

                if self.careu_copy!=self.careu and self.careu_copy==careu_anterior:
                    counter+=1

                if counter==3:
                    self.careu=self.careu_copy
                    print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
                    print("mutare bot")
                    for i in range(8):
                        for j in range(8):
                            print(self.careu[i][j],end=" ")
                        print()
                    break
                careu_anterior=self.careu_copy
                time.sleep(0.1)
            time.sleep(0.1)
            self.bot_turn.set()



    def go_click(self, dest_x, dest_y,hold=False):

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
            time.sleep(0.15)
            self.rc.set_cursor_position([int(dest_x-5),int(dest_y-5)])

            if hold:

                self.rc.hold_click()
            else:

                self.rc.click()
                self.rc.set_cursor_position(ogPos)




            self.done.set()

            self.root.focus_force()
        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")

            self.root.after(2, self.go_click, dest_x, dest_y,hold)

    def go_drag_drop(self, dest_x, dest_y,ogPos):

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

            self.rc.set_cursor_position([int(dest_x-5),int(dest_y-5)])
            time.sleep(0.1)
            self.rc.release_click()

            self.rc.set_cursor_position(ogPos)

            self.done.set()

            self.root.focus_force()
        else:
            new_x = int(cx + ((dest_x - cx) / dist) * step)
            new_y = int(cy + ((dest_y - cy) / dist) * step)

            self.root.geometry(f"+{new_x}+{new_y}")

            self.root.after(2, self.go_drag_drop, dest_x, dest_y,ogPos)


    def change_in_patch(self,medieOg,i,j):
        medieAnterioara=medieOg
        st=time.time()

        while time.time()-st<3.0:
            screenshot = ImageGrab.grab(bbox=(self.segmente[i][j][2], self.segmente[i][j][0], self.segmente[i][j][3], self.segmente[i][j][1]))
            imagine = np.array(screenshot)
            imagine = cv.cvtColor(imagine, cv.COLOR_RGB2BGR)
            imagine_gri = cv.cvtColor(imagine,cv.COLOR_BGR2GRAY)
            medie = np.mean(imagine_gri)
            if medie!=medieOg and medie==medieAnterioara:

                #print("Da" ,medieOg,medie)
                return True
            medieAnterioara=medie
            time.sleep(0.1)

        return False

    def wait_for_move(self,enemy):
        type="unknown"
        while True:


            self.bot_turn.wait()
            self.bot_turn.clear()

            if (self.stop_wait):
                self.thread1_stopped.set()
                print("Thread 1 done")
                return

            _,mutari,self.careu_copy=cs.minimax(self.careu_copy, depth=10, alpha=-math.inf, beta=math.inf, maximizing_player=True,st=time.time())

            if mutari is None:
                print("final")
                continue
            self.careu = self.careu_copy

            if type=="dragdrop":
                for k in range(1,len(mutari)):
                    i, j = mutari[k-1][0], mutari[k-1][1]

                    self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1], hold=True))
                    self.done.wait()
                    self.done.clear()

                    i, j = mutari[k][0], mutari[k][1]

                    self.root.after(0, lambda: self.go_drag_drop(self.puncte[i_dest][j_dest][0], self.puncte[i_dest][j_dest][1], ogPos))
                    self.done.wait()
                    self.done.clear()



                    time.sleep(0.5)
                self.root.geometry(f"+{self.bottom_right[0]}+{self.bottom_right[1]}")



            elif type=="click":
                for k in range(1,len(mutari)):
                    i, j = mutari[k-1][0], mutari[k-1][1]

                    self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1]))
                    self.done.wait()
                    self.done.clear()

                    i, j = mutari[k][0], mutari[k][1]

                    self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1]))
                    self.done.wait()
                    self.done.clear()


                    time.sleep(0.5)
                self.root.geometry(f"+{self.bottom_right[0]}+{self.bottom_right[1]}")

            else:

                i,j=mutari[0][0],mutari[0][1]

                self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1]))
                self.done.wait()
                self.done.clear()

                time.sleep(0.1)
                i, j = mutari[1][0], mutari[1][1]
                self.root.wm_attributes("-alpha", 0.0)
                screenshot = ImageGrab.grab()
                self.root.wm_attributes("-alpha", 1.0)
                imagine = np.array(screenshot)
                imagine = cv.cvtColor(imagine, cv.COLOR_RGB2BGR)
                imagine_gri=cv.cvtColor(imagine, cv.COLOR_BGR2GRAY)
                medieOg=np.mean(imagine_gri[self.segmente[i][j][0]:self.segmente[i][j][1],self.segmente[i][j][2]:self.segmente[i][j][3]])

                #self.detector.afiseaza_imagine1("nununun",imagine_gri)


                self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1]))
                self.done.wait()
                self.done.clear()
                self.root.geometry(f"+{self.bottom_right[0]}+{self.bottom_right[1]}")

                change=self.change_in_patch(medieOg,i,j)
                if not change:

                    ogPos = self.rc.get_cursor_position()


                    i_dest,j_dest=i,j
                    i,j=mutari[0][0],mutari[0][1]

                    self.root.after(0, lambda: self.go_click(self.puncte[i][j][0], self.puncte[i][j][1],hold=True))
                    self.done.wait()
                    self.done.clear()

                    self.root.wm_attributes("-alpha", 0.0)
                    screenshot = ImageGrab.grab()
                    self.root.wm_attributes("-alpha", 1.0)
                    imagine = np.array(screenshot)
                    imagine = cv.cvtColor(imagine, cv.COLOR_RGB2BGR)
                    imagine_gri = cv.cvtColor(imagine, cv.COLOR_BGR2GRAY)
                    medieOg = np.mean(imagine_gri[self.segmente[i_dest][j_dest][0]:self.segmente[i_dest][j_dest][1],
                                      self.segmente[i_dest][j_dest][2]:self.segmente[i_dest][j_dest][3]])

                    self.root.after(0, lambda: self.go_drag_drop(self.puncte[i_dest][j_dest][0], self.puncte[i_dest][j_dest][1],ogPos))
                    self.done.wait()
                    self.done.clear()

                    self.root.geometry(f"+{self.bottom_right[0]}+{self.bottom_right[1]}")



                    type="dragdrop"
                else:
                    type="click"

            print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
            print("mutare player")
            for i in range(8):
                for j in range(8):
                    print(self.careu[i][j],end=" ")
                print()
            time.sleep(0.1)
            self.player_turn.set()

    def play_against_bot(self):
        self.root.unbind("q")
        self.root.unbind("w")
        self.oprite-=1
        t1 = threading.Thread(target=self.wait_for_move,args=(type,),daemon=True)
        t2 = threading.Thread(target=self.wait_for_change, args=(), daemon=True)

        t2.start()
        t1.start()



        self.oprite += 1


    def stop_cursor(self):
        self.root.unbind("q")
        self.root.unbind("w")
        self.stop=True
        while(True):

            if(self.oprite==1):
                break
            time.sleep(0.5)
        print("totul oprit")
        self.root.geometry(f"+{1850}+{940}")
        self.root.event_generate("<<Rebind>>")
        self.stop=False


