import tkinter as tk
from PIL import Image, ImageTk
import math
import cv2 as cv
import numpy as np
import os
import time
root_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(root_dir, "templates")


class Sudoku:
    def __init__(self):
        self.scoruri = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.corners_dict={}
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

    def extrage_grila(self,image):
        copie = image.copy()
        originala = image.copy()
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        image_median = cv.medianBlur(image, 3)
        image_gaussian = cv.GaussianBlur(image_median, (0, 0), 5)
        image_sharpened = cv.addWeighted(image_median, 1.2, image_gaussian, -0.8, 0)
        #self.afiseaza_imagine('image_sharpened',image_sharpened)
        _, thresh = cv.threshold(image_sharpened, 80, 255, cv.THRESH_BINARY)
        #self.afiseaza_imagine1('image_thresholded',thresh)

        kernel = np.ones((3, 3), np.uint8)
        eroded = cv.erode(thresh, kernel,iterations=1)
        #self.afiseaza_imagine1('image_thresholded',eroded)

        edges = cv.Canny(eroded, 200, 400)
        #self.afiseaza_imagine1('edges',edges)
        contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        image_contours = cv.drawContours(copie, contours, -1, (0, 255, 0), 4)
        #self.afiseaza_imagine1('dadadada',image_contours)

        max_area = 0

        top_left, top_right, bottom_right, bottom_left=[[0,0],[0,0],[0,0],[0,0]]
        for i in range(len(contours)):
            if (len(contours[i]) > 3):
                top_left_candidate = None
                bottom_right_candidate = None
                for point in contours[i].squeeze():
                    if top_left_candidate is None or point[0] + point[1] < top_left_candidate[0] + top_left_candidate[1]:
                        top_left_candidate = point

                    if bottom_right_candidate is None or point[0] + point[1] > bottom_right_candidate[0] + bottom_right_candidate[1]:
                        bottom_right_candidate = point

                dif =np.diff(contours[i].squeeze(), axis=1)
                top_right_candidate = contours[i].squeeze()[np.argmin(dif)]
                bottom_left_candidate = contours[i].squeeze()[np.argmax(dif)]

                contour_area=cv.contourArea(np.array(
                        [[top_left_candidate], [top_right_candidate], [bottom_right_candidate], [bottom_left_candidate]]))
                key = "_".join([str(x) for x in top_left_candidate] + [str(x) for x in bottom_right_candidate])
                if contour_area > max_area and key not in self.corners_dict:
                    max_area = contour_area
                    top_left = top_left_candidate
                    bottom_right = bottom_right_candidate
                    top_right = top_right_candidate
                    bottom_left = bottom_left_candidate

        height = 900
        width = 900


        image_copy = cv.cvtColor(image.copy(), cv.COLOR_GRAY2BGR)
        cv.circle(image_copy, tuple(top_left), 5, (0, 0, 255), -1)
        cv.circle(image_copy, tuple(top_right), 5, (0, 0, 255), -1)
        cv.circle(image_copy, tuple(bottom_left), 5, (0, 0, 255), -1)
        cv.circle(image_copy, tuple(bottom_right), 5, (0, 0, 255), -1)
        #self.afiseaza_imagine("detected corners",image_copy)

        detected_corners = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
        correct_corners = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

        transformarea = cv.getPerspectiveTransform(detected_corners, correct_corners)

        result = cv.warpPerspective(originala, transformarea, (width, height))

        return result, top_left, top_right, bottom_left, bottom_right





    def prelucrare(self,img,lines_horizontal,lines_vertical):

        for i in range(len(lines_horizontal)-1):
            for j in range(len(lines_vertical)-1):
                y1 = lines_vertical[j][0][0] + 10
                y2 = lines_vertical[j + 1][1][0] - 10
                x1 = lines_horizontal[i][0][1] + 10
                x2 = lines_horizontal[i + 1][1][1] - 10
                cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=-1)

        return img




    def clasifica_cifra(self,patch, ok=1, cx=1.75, cy=1.75):

        indici = [1, 2, 3, 4, 5,6,7  ]
        numere = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        maxi = -np.inf
        poz = -1
        for i in indici:
            for j in numere:

                img_template = cv.imread(templates_path+'/t' + str(i) + '/' + str(j) + '.png')
                img_template = cv.resize(img_template, (0, 0), fx=cx, fy=cy)
                img_template = cv.cvtColor(img_template, cv.COLOR_BGR2GRAY)

                corr = cv.matchTemplate(patch, img_template, cv.TM_CCOEFF_NORMED)
                corr = np.max(corr)

                if corr > maxi:
                    maxi = corr
                    poz = j


        #self.afiseaza_imagine2(f"{poz}|{maxi}",patch)
        if (ok == 1 and maxi < 0.8):
            if self.scoruri[poz - 1] < maxi:
                self.scoruri[poz - 1] = maxi
            return 0
        if (ok == 2):
            if self.scoruri[poz - 1] < maxi:
                self.scoruri[poz - 1] = maxi
            if maxi < 0.8:
                return 0
            return poz
        if (ok == 3):
            if self.scoruri[poz - 1] < maxi:
                self.scoruri[poz - 1] = maxi
            return poz
        return poz


    def configurare_grila(self,img, thresh, lines_horizontal, lines_vertical):

        matrix = np.empty((9, 9), dtype='int')
        for i in range(len(lines_horizontal) - 1):
            for j in range(len(lines_vertical) - 1):
                ty_min = lines_vertical[j][0][0] + 15
                ty_max = lines_vertical[j + 1][1][0] - 15
                tx_min = lines_horizontal[i][0][1] + 15
                tx_max = lines_horizontal[i + 1][1][1] - 15
                y_min = lines_vertical[j][0][0] + 5
                y_max = lines_vertical[j + 1][1][0] - 5
                x_min = lines_horizontal[i][0][1] + 5
                x_max = lines_horizontal[i + 1][1][1] - 5
                patch = thresh[tx_min:tx_max, ty_min:ty_max].copy()
                patch_orig = img[x_min:x_max, y_min:y_max].copy()
                patch_orig = cv.cvtColor(patch_orig, cv.COLOR_BGR2GRAY)
                medie_patch = np.mean(patch)
                # print(medie_patch)
                #self.afiseaza_imagine2(f"{medie_patch}",patch)
                if medie_patch > 0:
                    # afiseaza_imagine2(f"{medie_patch}",patch)
                    matrix[i][j] = self.clasifica_cifra(patch_orig)

                    if matrix[i][j] == 0:

                        patch_orig = img[x_min + 10:x_max - 10, y_min + 10:y_max - 10].copy()
                        patch_orig = cv.cvtColor(patch_orig, cv.COLOR_BGR2GRAY)
                        # afiseaza_imagine2("asa da",patch_orig)
                        matrix[i][j] = self.clasifica_cifra(patch_orig, 2, 1.5, 1.5)

                        if matrix[i][j] == 0:
                            matrix[i][j] = self.clasifica_cifra(patch_orig, 3, 1.25, 1.25)
                        # print(self.scoruri)
                        matrix[i][j] = self.scoruri.index(max(self.scoruri)) + 1

                        self.scoruri = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    matrix[i][j] = 0
        return matrix


    def defineste_puncte(self,top_left, top_right, bottom_left, bottom_right):
        puncte = []

        pasx = (top_right[0] - top_left[0]) // 9
        pasy = (bottom_left[1] - top_left[1]) // 9

        for i in range(top_left[1], bottom_left[1] - pasy + 1, pasy):
            y = i + pasy // 2
            v = []
            for j in range(top_left[0], top_right[0] - pasx + 1, pasx):
                x = j + pasx // 2
                v.append([x, y])
            puncte.append(v)

        return puncte




    def isSafe(self,mat, i, j, num, row, col, box):
        if (row[i] & (1 << num)) or (col[j] & (1 << num)) or (box[i // 3 * 3 + j // 3] & (1 << num)):
            return False
        return True

    def sudokuSolverRec(self,mat, i, j, row, col, box):
        n = len(mat)

        # base case: Reached nth column of last row
        if i == n - 1 and j == n:
            return True

        # If reached last column of the row go to next row
        if j == n:
            i += 1
            j = 0

        # If cell is already occupied then move forward
        if mat[i][j] != 0:
            return self.sudokuSolverRec(mat, i, j + 1, row, col, box)

        for num in range(1, n + 1):
            # If it is safe to place num at current position
            if self.isSafe(mat, i, j, num, row, col, box):
                mat[i][j] = num

                # Update masks for the corresponding row, column and box
                row[i] |= (1 << num)
                col[j] |= (1 << num)
                box[i // 3 * 3 + j // 3] |= (1 << num)

                if self.sudokuSolverRec(mat, i, j + 1, row, col, box):
                    return True

                # Unmask the number num in the corresponding row, column and box masks
                mat[i][j] = 0
                row[i] &= ~(1 << num)
                col[j] &= ~(1 << num)
                box[i // 3 * 3 + j // 3] &= ~(1 << num)

        return False

    def solveSudoku(self,mat):
        n = len(mat)
        row = [0] * n
        col = [0] * n
        box = [0] * n

        # Set the bits in bitmasks for values that are initially present
        for i in range(n):
            for j in range(n):

                if mat[i][j] != 0:
                    row[i] |= (1 << mat[i][j])
                    col[j] |= (1 << mat[i][j])
                    box[(i // 3) * 3 + j // 3] |= (1 << mat[i][j])

        self.sudokuSolverRec(mat, 0, 0, row, col, box)


    """
    solveSudoku(matrice)
    print(matrice.tolist())
    print(matr_og.tolist())"""



    def rezolva(self,img):
        start_time=time.time()
        self.corners_dict={}
        #self.afiseaza_imagine1("asta este",img)
        lines_horizontal = []
        for i in range(0, 901, 100):
            l = []
            l.append((0, i))
            l.append((899, i))
            lines_horizontal.append(l)

        lines_vertical = []
        for i in range(0, 901, 100):
            l = []
            l.append((i, 0))
            l.append((i, 899))
            lines_vertical.append(l)
        gasit=False
        for i in range(0,10):
            image_copy = img.copy()
            result, top_left, top_right, bottom_left, bottom_right = self.extrage_grila(image_copy)
            cheie="_".join([str(x) for x in top_left]+[str(x) for x in bottom_right])

            self.corners_dict["_".join([str(x) for x in top_left]+[str(x) for x in bottom_right])]=1



            verificare = result.copy()
            verificare = self.prelucrare(verificare, lines_horizontal, lines_vertical)
            verificare = cv.cvtColor(verificare, cv.COLOR_BGR2GRAY)

            careu = cv.imread(templates_path+"/tabla.jpg")
            careu = cv.resize(careu, (900, 900))
            careu = cv.cvtColor(careu, cv.COLOR_BGR2GRAY)
            cor = cv.matchTemplate(verificare, careu, cv.TM_CCOEFF_NORMED)

            cor = np.max(cor)
            print(cor)
            #self.afiseaza_imagine1(f"{cor}", result)
            #self.afiseaza_imagine(f"{cor}",result)
            #self.afiseaza_imagine("1111",careu)
            #self.afiseaza_imagine("2222",verificare)
            if(cor>0.5):
                gasit=True
                break

        if not gasit:
            return None,None,None,None,None
        #print(top_left, top_right, bottom_left, bottom_right)
        puncte = self.defineste_puncte(top_left, top_right, bottom_left, bottom_right)

        copie1 = result.copy()
        copie1 = cv.cvtColor(copie1, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(copie1, 150, 255, cv.THRESH_BINARY_INV)
        #self.afiseaza_imagine1('normala',thresh)
        self.scoruri = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        matrice = self.configurare_grila(result, thresh, lines_horizontal, lines_vertical)
        matr_og = matrice.copy()
        print(matrice)
        #print("pana aici")
        print(f"timp: {time.time() - start_time}")
        self.solveSudoku(matrice)

        print(f"timp: {time.time() - start_time}")
        #print(matrice.tolist())
        #print(matr_og.tolist())
        return puncte,matr_og,matrice,top_left,bottom_right

































