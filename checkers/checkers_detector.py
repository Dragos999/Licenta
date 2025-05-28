import tkinter as tk
from PIL import Image, ImageTk
import math
import cv2 as cv
import numpy as np
import os
import time
import itertools
from screen_info import xratio,yratio


class CheckersDetector:
    def __init__(self):
        self.inamic=None
        self.player=None
        self.gol=None
        self.adaos=None
    def afiseaza_imagine(self,title, image):
        copie = cv.resize(image, (0, 0), fx=1, fy=1)
        cv.imshow(title, copie)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def afiseaza_imagine1(self,title, image):
        copie = cv.resize(image, (0, 0), fx=0.5, fy=0.5)
        cv.imshow(title, copie)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def afiseaza_imagine2(self,title, image):
        copie = cv.resize(image, (0, 0), fx=3, fy=3)
        cv.imshow(title, copie)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def get_lungime(self,line):
        return np.sqrt((line[0][2] - line[0][0]) ** 2 + (line[0][3] - line[0][1]) ** 2)

    def orizontal(self,linie):
        diferenta = 0.5
        unghi = abs(np.degrees(np.arctan2((linie[3] - linie[1]), (linie[2] - linie[0]))))
        conditie1 = unghi < diferenta or unghi > 180 - diferenta

        return conditie1

    def vertical(self,linie):
        diferenta = 0.5
        unghi = abs(np.degrees(np.arctan2((linie[3] - linie[1]), (linie[2] - linie[0]))))
        conditie1 = 90 - diferenta < unghi < diferenta + 90

        return conditie1

    def intersectat_vertical(self,vertical, orizontal, corecte):
        diferenta = 30

        cond1 = min(orizontal[0], orizontal[2]) - vertical[0] < -diferenta and max(orizontal[0], orizontal[2]) - \
                vertical[0] > diferenta
        cond2 = min(vertical[1], vertical[3]) - orizontal[1] < -diferenta and max(vertical[1], vertical[3]) - \
                orizontal[1] > diferenta

        if cond1 and cond2:
            dif = 20
            lungime = max(vertical[1], vertical[3]) - min(vertical[1], vertical[3])
            conditie1 = abs((max(vertical[1], vertical[3]) - (1 * lungime) // 8) - orizontal[1]) < dif
            if conditie1:
                corecte[0] = 1
                return True, corecte
            conditie2 = abs((max(vertical[1], vertical[3]) - (2 * lungime) // 8) - orizontal[1]) < dif
            if conditie2:
                corecte[1] = 1
                return True, corecte
            conditie3 = abs((max(vertical[1], vertical[3]) - (3 * lungime) // 8) - orizontal[1]) < dif
            if conditie3:
                corecte[2] = 1
                return True, corecte
            conditie4 = abs((max(vertical[1], vertical[3]) - (4 * lungime) // 8) - orizontal[1]) < dif
            if conditie4:
                corecte[3] = 1
                return True, corecte
            conditie5 = abs((max(vertical[1], vertical[3]) - (5 * lungime) // 8) - orizontal[1]) < dif
            if conditie5:
                corecte[4] = 1
                return True, corecte
            conditie6 = abs((max(vertical[1], vertical[3]) - (6 * lungime) // 8) - orizontal[1]) < dif
            if conditie6:
                corecte[5] = 1
                return True, corecte
            conditie7 = abs((max(vertical[1], vertical[3]) - (7 * lungime) // 8) - orizontal[1]) < dif
            if conditie7:
                corecte[6] = 1
                return True, corecte

        return False, corecte

    def intersectat_orizontal(self,vertical, orizontal, corecte):
        diferenta = 30
        cond1 = min(orizontal[0], orizontal[2]) - vertical[0] < -diferenta and max(orizontal[0], orizontal[2]) - \
                vertical[0] > diferenta
        cond2 = min(vertical[1], vertical[3]) - orizontal[1] < -diferenta and max(vertical[1], vertical[3]) - \
                orizontal[1] > diferenta
        if cond1 and cond2:
            dif = 20
            lungime = max(orizontal[0], orizontal[2]) - min(orizontal[0], orizontal[2])
            conditie1 = abs((max(orizontal[0], orizontal[2]) - (1 * lungime) / 8) - vertical[0]) < dif
            if conditie1:
                corecte[0] = 1
                return True, corecte
            conditie2 = abs((max(orizontal[0], orizontal[2]) - (2 * lungime) / 8) - vertical[0]) < dif
            if conditie2:
                corecte[1] = 1
                return True, corecte
            conditie3 = abs((max(orizontal[0], orizontal[2]) - (3 * lungime) / 8) - vertical[0]) < dif
            if conditie3:
                corecte[2] = 1
                return True, corecte
            conditie4 = abs((max(orizontal[0], orizontal[2]) - (4 * lungime) / 8) - vertical[0]) < dif
            if conditie4:
                corecte[3] = 1
                return True, corecte
            conditie5 = abs((max(orizontal[0], orizontal[2]) - (5 * lungime) / 8) - vertical[0]) < dif
            if conditie5:
                corecte[4] = 1
                return True, corecte
            conditie6 = abs((max(orizontal[0], orizontal[2]) - (6 * lungime) / 8) - vertical[0]) < dif
            if conditie6:
                corecte[5] = 1
                return True, corecte
            conditie7 = abs((max(orizontal[0], orizontal[2]) - (7 * lungime) / 8) - vertical[0]) < dif
            if conditie7:
                corecte[6] = 1
                return True, corecte

        return False, corecte

    def filtreaza(self,verticale, orizontale):
        v_filtrate = []
        o_filtrate = []
        respinse = 0
        for v in verticale:
            corecte = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter = 0
            for o in orizontale:
                cond, corecte = self.intersectat_vertical(v, o, corecte)
                if cond:
                    counter += 1

            if sum(corecte) == 7:
                v_filtrate.append(v)
            else:
                respinse += 1

        for o in orizontale:
            corecte = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            for v in verticale:
                cond, corecte = self.intersectat_orizontal(v, o, corecte)

            if sum(corecte) == 7:
                o_filtrate.append(o)
            else:
                respinse += 1
        return v_filtrate, o_filtrate, respinse

    def extragere_totala(self,image):
        img_cpy = image.copy()
        originala = image.copy()
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        image_m_blur = cv.medianBlur(image, 5)
        image_g_blur = cv.GaussianBlur(image_m_blur, (3, 3), 4)
        image_sharpened = cv.addWeighted(image_m_blur, 1.4, image_g_blur, -0.6, 0)

        #self.afiseaza_imagine1("image_sharpened",image_sharpened)

        normalized = cv.normalize(image_sharpened, None, 0, 255, cv.NORM_MINMAX)
        #self.afiseaza_imagine1("normalized",normalized)

        clahe = cv.createCLAHE(clipLimit=2.5, tileGridSize=(7, 7))
        clahe_image = clahe.apply(normalized)
        #self.afiseaza_imagine1("clahe_image",clahe_image)
        edges = cv.Canny(clahe_image, 100, 150, apertureSize=3)
        #self.afiseaza_imagine1("edges",edges)

        kernel = np.ones((3, 3), np.uint8)
        dilated = cv.dilate(edges, kernel, iterations=1)
        #self.afiseaza_imagine1("dilated",dilated)

        lines = cv.HoughLinesP(
            dilated,
            1,
            np.pi / 180,
            threshold=200,
            minLineLength=200,
            maxLineGap=100
        )
        verticale = []
        orizontale = []
        vanterioare = []
        oanterioare = []

        if lines is None:
            return [],[],0

        for linie in lines:
            linie = linie[0]
            if (self.vertical(linie)):
                ok = True
                for va in vanterioare:
                    if va - 20 < linie[0] < va + 20:
                        ok = False
                if ok:
                    verticale.append(linie)
                    vanterioare.append(linie[0])
            elif self.orizontal(linie):
                ok = True
                for vo in oanterioare:
                    if vo - 20 < linie[1] < vo + 20:
                        ok = False
                if ok:
                    orizontale.append(linie)
                    oanterioare.append(linie[1])
        """        
        for linie in verticale+orizontale:

            cv.line(originala,(linie[0],linie[1]),(linie[2],linie[3]),(0,0,255),2)
       self.afiseaza_imagine1("originala",originala)"""
        v_filtrate, o_filtrate, respinse = self.filtreaza(verticale, orizontale)

        return v_filtrate, o_filtrate, respinse

    def get_segmente_puncte(self,top_left, top_right, bottom_left, bottom_right,latime):
        puncte = []
        segmente = []
        pasx = (top_right[0] - top_left[0]) // 8
        pasy = (bottom_left[1] - top_left[1]) // 8
        diferenta = (8*latime)//250
        print("Diferenta: ",diferenta)
        for i in range(top_left[1], bottom_left[1] - pasy + 1, pasy):
            y = i + pasy // 2
            p = []
            #
            y1 = i + diferenta
            y2 = i + pasy - diferenta
            s = []

            for j in range(top_left[0], top_right[0] - pasx + 1, pasx):
                x = j + pasx // 2
                p.append([x, y])
                #
                x1 = j + diferenta
                x2 = j + pasx - diferenta
                s.append([y1, y2, x1, x2])

            puncte.append(p)
            segmente.append(s)
        return segmente, puncte

    def get_medii(self,imagine,segmente):
        gri = cv.cvtColor(imagine, cv.COLOR_BGR2GRAY)

        medii = []
        for i in range(8):
            v = []
            for j in range(8):
                img_segmentata = gri[segmente[i][j][0]:segmente[i][j][1], segmente[i][j][2]:segmente[i][j][3]]
                v.append(np.mean(img_segmentata))
            medii.append(v)
        return medii

    def get_histograme(self,img_hsv):
        hist_h = cv.calcHist([img_hsv], [0], None, [180], [0, 180])
        hist_s = cv.calcHist([img_hsv], [1], None, [256], [0, 256])
        hist_v = cv.calcHist([img_hsv], [2], None, [256], [0, 256])

        return [hist_h,hist_s,hist_v]

    def comp_histograme(self,hist1,hist2):
        score1 = cv.compareHist(hist1[0], hist2[0], cv.HISTCMP_CORREL)
        score2 = cv.compareHist(hist1[1], hist2[1], cv.HISTCMP_CORREL)
        score3 = cv.compareHist(hist1[2], hist2[2], cv.HISTCMP_CORREL)
        return(score1 + score2 + score3) / 3

    def tip_clasic(self,imagine,segmente):
        i,j=0,0
        patch1=imagine[segmente[i][j][0] :segmente[i][j][1], segmente[i][j][2] :segmente[i][j][3] ]
        patch_hsv1 = cv.cvtColor(patch1, cv.COLOR_BGR2HSV)
        hist1=self.get_histograme(patch_hsv1)

        i,j=4,0
        patch2=imagine[segmente[i][j][0] :segmente[i][j][1], segmente[i][j][2] :segmente[i][j][3] ]
        patch_hsv2 = cv.cvtColor(patch2, cv.COLOR_BGR2HSV)
        hist2=self.get_histograme(patch_hsv2)
        print("Asemanare: ",self.comp_histograme(hist1,hist2))
        return self.comp_histograme(hist1,hist2)>=0.73



    def determina_configuratie(self,imagine,segmente,careuOg):
        if len(careuOg)==0:
            careuOg = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        careu=[]
        if self.inamic is None:
            return None

        pozitie_initiala=None
        pozitie_finala=None
        for i in range(8):
            linie=[]
            for j in range(8):
                patch=imagine[segmente[i][j][0] :segmente[i][j][1], segmente[i][j][2] :segmente[i][j][3] ]
                patch_hsv = cv.cvtColor(patch, cv.COLOR_BGR2HSV)
                hist=self.get_histograme(patch_hsv)

                if self.comp_histograme(hist,self.inamic) >=0.75:
                    if careuOg[i][j]==-2:
                        linie.append(-2)
                    else:
                        linie.append(-1)
                elif self.comp_histograme(hist,self.player) >=0.75:
                    if careuOg[i][j]==2:
                        linie.append(2)
                    else:
                        linie.append(1)
                else:

                    if self.comp_histograme(hist,self.gol) >=0.25 or (i+j+self.adaos)%2==0 or (self.comp_histograme(hist,self.inamic)<0 and self.comp_histograme(hist,self.player)<0):
                        linie.append(0)
                    else:

                        if self.comp_histograme(hist,self.inamic) > self.comp_histograme(hist,self.player):
                            linie.append(-2)

                        else:
                            linie.append(2)
                if careuOg[i][j]==-2 and linie[j]!=-2:
                    pozitie_initiala=[i,j]
                if careuOg[i][j]==0 and linie[j]!=0:
                    pozitie_finala=[i,j]
            careu.append(linie)

        if pozitie_initiala is not None and pozitie_finala is not None:

            careu[pozitie_finala[0]][pozitie_finala[1]]=careuOg[pozitie_initiala[0]][pozitie_initiala[1]]

        i=0
        for j in range(8):
            if careu[i][j]==1:
                careu[i][j]=2
        i=7
        for j in range(8):
            if careu[i][j]==-1:
                careu[i][j]=-2
        return careu





    def extrage_careu(self,image,imagine_reala):
        pt_medii=imagine_reala.copy()



        originala = image.copy()
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        image_m_blur = cv.medianBlur(image, 3)
        image_g_blur = cv.GaussianBlur(image_m_blur, (5, 5), 4)
        image_sharpened = cv.addWeighted(image_m_blur, 1.2, image_g_blur, -0.9, 0)
        #self.afiseaza_imagine1("image_sharpened",image_sharpened)

        clahe = cv.createCLAHE(clipLimit=2.5, tileGridSize=(7, 7))
        clahe_image = clahe.apply(image_sharpened)
        #self.afiseaza_imagine1("clahe_image",clahe_image)

        edges = cv.Canny(clahe_image, 110, 150, apertureSize=3)
        #self.afiseaza_imagine1("edges",edges)

        kernel = np.ones((3, 3), np.uint8)
        dilated = cv.dilate(edges, kernel, iterations=1)
        #self.afiseaza_imagine1("dilated",dilated)
        contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cont = []

        for c in contours:
            approx = cv.approxPolyDP(c, 0.02 * cv.arcLength(c, True), True)
            if len(approx) >= 4:
                x, y, w, h = cv.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.8 < aspect_ratio < 1.2 and w > 200:

                    cont.append(c)


        """img_cpy=originala.copy()
        cv.drawContours(img_cpy, cont, -1, (0, 255, 0), 4)
        self.afiseaza_imagine1('dadadada',img_cpy)"""

        #print(len(cont))
        v, o, respinse = None, None, 9999
        for c in cont:
            minimx = [9999, 0]
            maximx = [-1, 0]
            minimy = [0, 9999]
            maximy = [0, -1]
            for p in c:
                p = p[0]
                if p[0] < minimx[0]:
                    minimx = p
                if p[0] > maximx[0]:
                    maximx = p
                if p[1] < minimy[1]:
                    minimy = p
                if p[1] > maximy[1]:
                    maximy = p

            p1, p2, p3, p4 = [], [], [], []
            p1 = [minimx[0], minimy[1]]
            p2 = [maximx[0], minimy[1]]
            p3 = [minimx[0], maximy[1]]
            p4 = [maximx[0], maximy[1]]

            puzzle = np.array([p1, p2, p4, p3], dtype=np.int32)

            mask = np.zeros_like(originala)

            cv.fillPoly(mask, [puzzle], (255, 255, 255))

            white_background = np.ones_like(originala) * 0

            result = np.where(mask == 255, originala, white_background)

            #self.afiseaza_imagine1("result",result)

            v_filtrate, o_filtrate, r = self.extragere_totala(result)
            #print(v_filtrate,o_filtrate,r)
            if len(v_filtrate) >= 7 and len(o_filtrate) >= 7 and r < respinse:
                v = v_filtrate
                o = o_filtrate
                respinse = r

        top_left, top_right, bottom_left, bottom_right = None, None, None, None
        segmente, puncte,medii = None, None, None
        if v is not None:
            linie1 = min(v, key=lambda x: max(x[1], x[3]) - min(x[1], x[3]))
            linie2 = min(o, key=lambda x: max(x[0], x[2]) - min(x[0], x[2]))
            top_left = [round(min(linie2[0], linie2[2])*xratio), round(min(linie1[1], linie1[3])*yratio)]
            top_right = [round(max(linie2[0], linie2[2])*xratio), round(min(linie1[1], linie1[3])*yratio)]
            bottom_left = [round(min(linie2[0], linie2[2])*xratio), round(max(linie1[1], linie1[3])*yratio)]
            bottom_right = [round(max(linie2[0], linie2[2])*xratio), round(max(linie1[1], linie1[3])*yratio)]

            #print(min(linie2[0], linie2[2]),"  |  ",round(min(linie2[0], linie2[2])*xratio))

            latime= top_right[0] - top_left[0]
            print("Latime: ",latime)

            segmente, puncte = self.get_segmente_puncte(top_left, top_right, bottom_left, bottom_right,latime)

            if self.tip_clasic(imagine_reala,segmente):

                i, j = 0, 1
                patch_inamic=imagine_reala[segmente[i][j][0]:segmente[i][j][1], segmente[i][j][2]:segmente[i][j][3]]
                patch_inamic_hsv = cv.cvtColor(patch_inamic, cv.COLOR_BGR2HSV)
                self.inamic=self.get_histograme(patch_inamic_hsv)

                i, j = 7, 0
                patch_player = imagine_reala[segmente[i][j][0]:segmente[i][j][1],
                               segmente[i][j][2]:segmente[i][j][3]]
                patch_player_hsv = cv.cvtColor(patch_player, cv.COLOR_BGR2HSV)
                self.player = self.get_histograme(patch_player_hsv)

                i, j = 4, 7
                patch_gol=imagine_reala[segmente[i][j][0]:segmente[i][j][1],
                               segmente[i][j][2]:segmente[i][j][3]]
                patch_gol_hsv = cv.cvtColor(patch_gol, cv.COLOR_BGR2HSV)
                self.gol = self.get_histograme(patch_gol_hsv)

                self.adaos=0

            else:
                i, j = 0, 0
                patch_inamic = imagine_reala[segmente[i][j][0]:segmente[i][j][1],
                               segmente[i][j][2]:segmente[i][j][3]]
                patch_inamic_hsv = cv.cvtColor(patch_inamic, cv.COLOR_BGR2HSV)
                self.inamic = self.get_histograme(patch_inamic_hsv)

                i, j = 7, 1
                patch_player = imagine_reala[segmente[i][j][0]:segmente[i][j][1],
                               segmente[i][j][2]:segmente[i][j][3]]
                patch_player_hsv = cv.cvtColor(patch_player, cv.COLOR_BGR2HSV)
                self.player = self.get_histograme(patch_player_hsv)

                i, j = 4, 6
                patch_gol = imagine_reala[segmente[i][j][0]:segmente[i][j][1],
                            segmente[i][j][2]:segmente[i][j][3]]
                patch_gol_hsv = cv.cvtColor(patch_gol, cv.COLOR_BGR2HSV)
                self.gol = self.get_histograme(patch_gol_hsv)

                self.adaos=1

            medii=self.get_medii(pt_medii,segmente)
        """self.afiseaza_imagine1("originala",originala)
        if top_left is not None:
            self.afiseaza_imagine1("originala", originala[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]])"""
        return top_left, bottom_right, segmente, puncte,medii

    def verifica_schimbare(self,image,segmente,medii,careu):
        y_schimbat,x_schimbat=-1,-1
        y_initial,x_initial=-1,-1
        capturati=[]
        for i in range(8):
            for j in range(8):
                medie=np.mean(image[segmente[i][j][0]:segmente[i][j][1],segmente[i][j][2]:segmente[i][j][3]])

                if abs(medie-medii[i][j])>0.1:
                    if careu[i][j]==0:
                        y_schimbat,x_schimbat=i,j
                    elif careu[i][j]==-1 or careu[i][j]==-2:
                        y_initial,x_initial=i,j
                    elif careu[i][j]==1 or careu[i][j]==2:
                        capturati.append(i,j)

                    medii[i][j]=medie

        return y_schimbat,x_schimbat,y_initial,x_initial,capturati


"""
cr=CheckersDetector()
for i in range(25,26):
    img=cv.imread(f"C:/Users/mihae/OneDrive/Desktop/checkers/checkers{i}.png")
    top_left, bottom_right, segmente, puncte, medii =cr.extrage_careu(img)
    careuOg = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    tare=(cr.determina_configuratie(img,segmente,careuOg))
    for k in range(8):
        for j in range(8):
            print(tare[k][j],end=" ")
        print()"""












