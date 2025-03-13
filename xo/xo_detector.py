import tkinter as tk
from PIL import Image, ImageTk
import math
import cv2 as cv
import numpy as np
import os
import time
import itertools


class XoDetector:
    def __init__(self):
        self.segmente=[[]]
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

    def orizontal_vertical(self,linie):
        if linie[0][1] == linie[0][3]:
            return "orizontal", "vertical"
        return "vertical", "orizontal"



    def intersectat_orizontale(self,orizontal, vertical, ok='0'):
        orizontal = orizontal[0]
        vertical = vertical[0]
        diferenta = 50
        conditie1 = min(orizontal[0], orizontal[2]) - vertical[0] < -diferenta and max(orizontal[0], orizontal[2]) - vertical[0] > diferenta
        conditie2 = min(vertical[1], vertical[3]) - orizontal[1] < -diferenta and max(vertical[1], vertical[3]) -  orizontal[1] > diferenta
        if conditie1 and conditie2:

            dif = 15
            lungime = max(orizontal[0], orizontal[2]) - min(orizontal[0], orizontal[2])
            conditie3 = abs((max(orizontal[0], orizontal[2]) - lungime / 3) - vertical[0]) < dif
            conditie4 = abs((max(orizontal[0], orizontal[2]) - (2 * lungime) / 3) - vertical[0]) < dif
            if ok == '0':
                if conditie3:
                    return True, '2/3'
                if conditie4:
                    return True, '1/3'
            elif ok == '2/3':
                if conditie4:
                    return True, '1/3'
            elif ok == '1/3':
                if conditie3:
                    return True, '2/3'

            return False, '0'
        return False, '0'

    def intersectat_verticale(self,orizontal, vertical, ok='0'):
        orizontal = orizontal[0]
        vertical = vertical[0]
        diferenta = 50
        conditie1 = min(orizontal[0], orizontal[2]) - vertical[0] < -diferenta and max(orizontal[0], orizontal[2]) - \
                    vertical[0] > diferenta
        conditie2 = min(vertical[1], vertical[3]) - orizontal[1] < -diferenta and max(vertical[1], vertical[3]) - \
                    orizontal[1] > diferenta
        if conditie1 and conditie2:

            dif = 15
            lungime = max(vertical[1], vertical[3]) - min(vertical[1], vertical[3])
            conditie3 = abs((max(vertical[1], vertical[3]) - lungime / 3) - orizontal[1]) < dif
            conditie4 = abs((max(vertical[1], vertical[3]) - (2 * lungime) / 3) - orizontal[1]) < dif
            if ok == '0':
                if conditie3:
                    return True, '2/3'
                if conditie4:
                    return True, '1/3'
            elif ok == '2/3':
                if conditie4:
                    return True, '1/3'
            elif ok == '1/3':
                if conditie3:
                    return True, '2/3'

            return False, '0'
        return False, '0'

    def filtreaza(self,orizontal, vertical):

        resturiv = []
        resturio = []
        aproape_perfect1 = False
        aproape_perfect2 = False
        perfect = False
        orizontal_filtrate = []
        for lo in orizontal:
            counter = 0
            ok = '0'
            for lv in vertical:
                conditie = self.intersectat_orizontale(lo, lv, ok)
                if conditie[0]:
                    ok = conditie[1]
                    counter += 1
                if counter >= 2:
                    aproape_perfect1 = True
                    orizontal_filtrate.append(lo)
                    break
            if counter == 1:
                resturio.append(lo)

        vertical_filtrate = []
        for lv in vertical:
            counter = 0
            ok = '0'
            for lo in orizontal:
                conditie = self.intersectat_verticale(lo, lv, ok)
                if conditie[0]:
                    ok = conditie[1]
                    counter += 1
                if counter >= 2:
                    aproape_perfect2 = True
                    vertical_filtrate.append(lv)
                    break
            if counter == 1:
                resturiv.append(lv)

        if aproape_perfect1 and aproape_perfect2:
            perfect = True
        #print(aproape_perfect1,"    ",aproape_perfect2,"      ",perfect,"      ",len(orizontal)+len(vertical))
        if perfect:
            return perfect, orizontal_filtrate, vertical_filtrate,None,None
        else:
            return perfect, orizontal_filtrate, vertical_filtrate, resturio + orizontal_filtrate, resturiv + vertical_filtrate

    def get_lungime(self,line):
        return np.sqrt((line[0][2] - line[0][0])**2 +( line[0][3]- line[0][1])**2 )

    def elimina_surplus(self,orizontal, vertical, lungime):
        x1, x2, y1, y2 = [], [], [], []
        for l in orizontal + vertical:
            x1.append(min(l[0][0], l[0][2]))
            y1.append(min(l[0][1], l[0][3]))
            x2.append(max(l[0][0], l[0][2]))
            y2.append(max(l[0][1], l[0][3]))
        medie_x1 = np.mean(x1)
        medie_y1 = np.mean(y1)
        medie_x2 = np.mean(x2)
        medie_y2 = np.mean(y2)

        diferenta = 20
        filtrateo = []
        filtratev = []
        for l in orizontal:
            conditie1 = abs(medie_x1 -max(l[0][0], l[0][2])) <= 2 * lungime + diferenta
            conditie2 = abs(medie_x2 -min(l[0][0], l[0][2])) <= 2 * lungime + diferenta
            conditie3 = abs(medie_y1 -min(l[0][1], l[0][3])) <= 2 * lungime + diferenta
            conditie4 = abs(medie_y2 -max(l[0][1], l[0][3])) <= 2 * lungime + diferenta
            if conditie1 and conditie2 and conditie3 and conditie4:
                filtrateo.append(l)
        for l in vertical:
            conditie1 = abs(medie_x1 -max(l[0][0], l[0][2])) <= 2 * lungime + diferenta
            conditie2 = abs(medie_x2 -min(l[0][0], l[0][2])) <= 2 * lungime + diferenta
            conditie3 = abs(medie_y1 -min(l[0][1], l[0][3])) <= 2 * lungime + diferenta
            conditie4 = abs(medie_y2 -max(l[0][1], l[0][3])) <= 2 * lungime + diferenta
            if conditie1 and conditie2 and conditie3 and conditie4:
                filtratev.append(l)
        return filtrateo, filtratev

    def get_posibile_careuri(self,lines):
        diferenta = 20
        grupuri = []
        for l in lines:
            lungime = self.get_lungime(l)
            gata = False
            for grup in grupuri:
                lungime_grup = grup["lungime"]
                conditie1 = abs(lungime - lungime_grup) <= diferenta

                if conditie1:
                    grup[self.orizontal_vertical(l)[0]].append(l)

                    gata = True
                    break
            if not gata:
                grupuri.append({"perfect": False, "lungime": lungime, f"{self.orizontal_vertical(l)[0]}": [l],f"{self.orizontal_vertical(l)[1]}": [], "resturi_orizontal": [], "resturi_vertical": []})

        for grup in grupuri:
            lv = grup["vertical"]
            lo = grup["orizontal"]

            grup["perfect"], grup["orizontal"], grup["vertical"], grup["resturi_orizontal"], grup["resturi_vertical"] = self.filtreaza(lo, lv)
        first = []
        second = []

        for grup in grupuri:
            if grup["perfect"]:
                first.append(grup)
            elif len(grup["resturi_orizontal"]) > 0 and len(grup["resturi_vertical"]) > 0:
                second.append(grup)
        first.sort(key=lambda grup: grup["lungime"], reverse=True)
        second.sort(key=lambda grup: grup["lungime"], reverse=True)
        for fs in first:
            fs["orizontal"], fs["vertical"] = self.elimina_surplus(fs["orizontal"], fs["vertical"], fs["lungime"])
        for sc in second:
            sc["resturi_orizontal"], sc["resturi_vertical"] = self.elimina_surplus(sc["resturi_orizontal"],sc["resturi_vertical"], sc["lungime"])
        return first, second

    def valideaza(self,verificare):

        lines_verificare = cv.HoughLinesP(
            verificare,
            1,
            np.pi / 2,
            threshold=100,
            minLineLength=100,
            maxLineGap=30
        )
        if lines_verificare is None:
            return False

        orizontal, vertical = [], []
        for line in lines_verificare:
            if line[0][0] == line[0][2]:
                vertical.append(line)
            else:
                orizontal.append(line)
        perfect, _, _, _, _ = self.filtreaza(orizontal, vertical)
        if perfect:
            return True
        return False

    def detecteaza_careu(self,image):

        result = image.copy()
        copie = image.copy()
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


        thresh = cv.adaptiveThreshold(
            image, 255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY_INV,
            11, 3
        )
        # afiseaza_imagine1("thresh",thresh)

        edges = cv.Canny(thresh, 200, 400, apertureSize=3)
        # afiseaza_imagine1("edges",edges)

        lines = cv.HoughLinesP(
            edges,
            1,
            np.pi / 2,
            threshold=100,
            minLineLength=100,
            maxLineGap=25
        )
        if lines is None:
            return False, None,None
        print(len(lines))
        if (len(lines) > 1050):
            gaussian = cv.GaussianBlur(image, (3, 3), 1)
            # afiseaza_imagine1("blurred",blurred)

            clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            clahe_image = clahe.apply(gaussian)
            # afiseaza_imagine1("contrast",contrast)

            edges = cv.Canny(clahe_image, 200, 400, apertureSize=3)
            # afiseaza_imagine1("edges",edges)

            kernel = np.ones((3, 3), np.uint8)
            dilated = cv.dilate(edges, kernel, iterations=1)
            # afiseaza_imagine1("dilated",dilated)

            closed = cv.morphologyEx(dilated, cv.MORPH_CLOSE, kernel, iterations=1)
            # afiseaza_imagine1("closed",closed)

            lines = cv.HoughLinesP(
                closed,
                1,
                np.pi / 2,
                threshold=100,
                minLineLength=100,
                maxLineGap=25
            )

        for linie in lines:
            cv.line(copie, (linie[0][0], linie[0][1]), (linie[0][2], linie[0][3]), (0, 0, 255), 2)
        #self.afiseaza_imagine1("copie",copie)

        first, second = self.get_posibile_careuri(lines)
        """
        for g in first:

            sablon=result.copy()
            l=g["lungime"]
            for linie in g["orizontal"]:
                cv.line(sablon,(linie[0][0],linie[0][1]),(linie[0][2],linie[0][3]),(0,0,255),2)
            for linie in g["vertical"]:
                cv.line(sablon,(linie[0][0],linie[0][1]),(linie[0][2],linie[0][3]),(0,0,255),2)

            self.afiseaza_imagine1(f"fst{l}",sablon)
        for g in second:

            sablon=result.copy()
            l=g["lungime"]
            for linie in g["resturi_orizontal"]:
                cv.line(sablon,(linie[0][0],linie[0][1]),(linie[0][2],linie[0][3]),(0,0,255),2)
            for linie in g["resturi_vertical"]:
                cv.line(sablon,(linie[0][0],linie[0][1]),(linie[0][2],linie[0][3]),(0,0,255),2)

            self.afiseaza_imagine1(f"scd{l}",sablon)"""
        top_left, top_right, bottom_left, bottom_right = [0, 0], [0, 0], [0, 0], [0, 0]
        gasit = False
        if len(first) > 0:
            gasit = True
            if (len(first[0]["orizontal"]) == 0 or len(first[0]["vertical"]) == 0):
                return False, None,None
            orizontala = max(first[0]["orizontal"], key=self.get_lungime)
            verticala = max(first[0]["vertical"], key=self.get_lungime)
            top_left = [min(orizontala[0][0], orizontala[0][2]), min(verticala[0][1], verticala[0][3])]
            top_right = [max(orizontala[0][0], orizontala[0][2]), min(verticala[0][1], verticala[0][3])]
            bottom_left = [min(orizontala[0][0], orizontala[0][2]), max(verticala[0][1], verticala[0][3])]
            bottom_right = [max(orizontala[0][0], orizontala[0][2]), max(verticala[0][1], verticala[0][3])]
        elif len(second) > 0:
            for i in range(len(second)):
                if (len(second[i]["resturi_orizontal"]) == 0 or len(second[i]["resturi_vertical"]) == 0):
                    continue
                orizontala = max(second[i]["resturi_orizontal"], key=self.get_lungime)
                verticala = max(second[i]["resturi_vertical"], key=self.get_lungime)
                x1, y1, x2, y2 = 0, 0, 0, 0
                x1 = min(orizontala[0][0], orizontala[0][2])
                x2 = max(orizontala[0][0], orizontala[0][2])
                y1 = min(verticala[0][1], verticala[0][3])
                y2 = max(verticala[0][1], verticala[0][3])
                verificare = edges.copy()
                verificare = verificare[y1:y2, x1:x2]
                verdict = self.valideaza(verificare)
                if verdict == True:
                    gasit = True
                    top_left = [min(orizontala[0][0], orizontala[0][2]), min(verticala[0][1], verticala[0][3])]
                    top_right = [max(orizontala[0][0], orizontala[0][2]), min(verticala[0][1], verticala[0][3])]
                    bottom_left = [min(orizontala[0][0], orizontala[0][2]), max(verticala[0][1], verticala[0][3])]
                    bottom_right = [max(orizontala[0][0], orizontala[0][2]), max(verticala[0][1], verticala[0][3])]
                    break

        if not gasit:
            return False,None,None

        height = 900
        width = 900

        detected_corners = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
        correct_corners = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

        transformarea = cv.getPerspectiveTransform(detected_corners, correct_corners)

        result = cv.warpPerspective(result, transformarea, (width, height))

        return True, result,[top_left,top_right,bottom_left,bottom_right]

    def defineste_puncte(self,corners):
        top_left, top_right, bottom_right, bottom_left = corners[0], corners[1], corners[2], corners[3]
        puncte=[]
        pasx = (top_right[0] - top_left[0]) // 3
        pasy = (bottom_left[1] - top_left[1]) // 3

        for i in range(top_left[1], bottom_left[1] - pasy + 1, pasy):
            y = i + pasy // 2
            v = []
            for j in range(top_left[0], top_right[0] - pasx + 1, pasx):
                x = j + pasx // 2
                v.append([x, y])
            puncte.append(v)

        return puncte

    def get_segmente(self,corners):
        top_left, top_right, bottom_right, bottom_left=corners[0],corners[1],corners[2],corners[3]
        segmente=[]
        pasx = (top_right[0] - top_left[0]) // 3
        pasy = (bottom_left[1] - top_left[1]) // 3
        diferenta=5
        for i in range(top_left[1], bottom_left[1] - pasy + 1, pasy):
            y1=i+diferenta
            y2=i+pasy-diferenta
            v = []
            for j in range(top_left[0], top_right[0] - pasx + 1, pasx):
                x1=j+diferenta
                x2=j+pasx-diferenta
                v.append([y1,y2,x1,x2])
            segmente.append(v)

        return segmente

    def get_medii(self,imagine,segmente):
        gri=cv.cvtColor(imagine, cv.COLOR_BGR2GRAY)
        medii=[]
        for i in range(3):
            v=[]
            for j in range(3):
                img_segmentata=gri[segmente[i][j][0]:segmente[i][j][1],segmente[i][j][2]:segmente[i][j][3]]
                v.append(np.mean(img_segmentata))
            medii.append(v)
        return medii



    def get_xo(self,image):
        #self.afiseaza_imagine1("initial", imagine)

        verdict, result, corners = self.detecteaza_careu(image)
        if verdict == True:
            #self.afiseaza_imagine1("result", result)
            self.segmente = self.get_segmente(corners)
            #print(segmente)
            puncte = self.defineste_puncte(corners)
            medii = self.get_medii(image, self.segmente)

            return puncte,self.segmente,medii,corners[3],corners[0]
        return None,None,None,None,None


    def verifica_schimbare(self,image,segmente,medii,careu):

        for i in range(3):
            for j in range(3):
                medie=np.mean(image[segmente[i][j][0]:segmente[i][j][1],segmente[i][j][2]:segmente[i][j][3]])

                if abs(medie-medii[i][j])>0.0 and careu[i][j]=='_':
                    return i,j

        return -1,-1

    def verifica_joc_nou(self,image,segmente,medii):
        counter=0
        for i in range(3):
            for j in range(3):
                medie=np.mean(image[segmente[i][j][0]:segmente[i][j][1],segmente[i][j][2]:segmente[i][j][3]])

                if abs(medie-medii[i][j])==0.0 :
                    counter+=1

        if counter>=8:
            return True
        return False

    def patch_schimbat(self,image,segment,medie_og):
        medie=np.mean(image[segment[0]:segment[1],segment[2]:segment[3]])
        print(abs(medie-medie_og))
        if abs(medie-medie_og)>0.0:
            return True

        return False


"""
st = time.time()
xo_solve=XoDetector()
for i in range(1, 2):

    imagine = cv.imread("C:/Users/mihae/OneDrive/Desktop/xo/xo" + str(i) + ".png")
    xo_solve.get_xo(imagine)

print(time.time() - st)"""