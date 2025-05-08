import time


class Nod:
    def __init__(self, id_linie=None, id_coloana=None):

        #toate atributele necesare pentru un nod in toroidala
        self.st = self.dr = self.sus = self.jos = self

        self.coloana = self
        self.id_linie = id_linie
        self.id_coloana = id_coloana

        self.counter = 0



class DLX:
    def __init__(self, matrice_exact_cover, valori_reale):
        #aici se creeaza matricea toroidala

        self.careu=None
        self.stop=False
        self.nLin = len(matrice_exact_cover)
        self.nCol = len(matrice_exact_cover[0])
        #definim un cap al toroidalei, de el se vor lega toti reprezentantii coloanelor
        #util in a determina daca avem solutie
        self.cap = Nod()
        self.solutii = []
        self.valori_reale = valori_reale

        #cream si conectam intre ei reprezentantii coloanelor, cu utilitate in gestionarea parcurgerii toroidalei si in cover/uncover
        self.reprezentanti_coloane = [Nod(0, j) for j in range(self.nCol)]

        for i in range(self.nCol):
            self.reprezentanti_coloane[i].st = self.reprezentanti_coloane[i - 1]
            self.reprezentanti_coloane[i - 1].dr = self.reprezentanti_coloane[i]
        self.reprezentanti_coloane[0].st = self.cap
        self.reprezentanti_coloane[-1].dr = self.cap
        self.cap.dr = self.reprezentanti_coloane[0]
        self.cap.st = self.reprezentanti_coloane[-1]

        # cream celelalte noduri, un nod simbolizeaza o valoare de 1(True) in matricea de exact cover
        self.linii = []
        for i in range(self.nLin):
            capat_linie = None
            for j in range(self.nCol):
                if matrice_exact_cover[i][j]:
                    nod_nou = Nod(i, j)
                    col_header = self.reprezentanti_coloane[j]
                    nod_nou.coloana = col_header

                    #inserare nod pe verticala
                    nod_nou.jos = col_header
                    nod_nou.sus = col_header.sus
                    col_header.sus.jos = nod_nou
                    col_header.sus = nod_nou
                    col_header.counter += 1

                    #inserare nod pe orizontala
                    if capat_linie is None:
                        capat_linie = nod_nou
                        nod_nou.dr = nod_nou.st = nod_nou
                    else:
                        nod_nou.dr = capat_linie
                        nod_nou.st = capat_linie.st
                        capat_linie.st.dr = nod_nou
                        capat_linie.st = nod_nou
            if capat_linie:
                self.linii.append(capat_linie)

    def reconstruieste(self):
        #reconstruim careul propriu-zis de sudoku dupa mapare pozitii-valoare

        self.careu = [[0 for _ in range(9)] for _ in range(9)]

        for nod in self.solutii:

            i, j, k = self.valori_reale[nod.id_linie]
            self.careu[i][j] = k


        return

    def cover(self, nod_col):
        #"dezlegam" coloana gasita si liniile ce au noduri pe acea coloana

        nod_col.dr.st = nod_col.st
        nod_col.st.dr = nod_col.dr

        i = nod_col.jos
        while i != nod_col:

            j =i.dr
            while j!=i:
                j.jos.sus= j.sus
                j.sus.jos= j.jos
                j.coloana.counter -= 1

                j = j.dr

            i = i.jos

    def uncover(self, nod_col):
        #"legam" la loc coloana si liniile ce au noduri pe acaesta coloana
        #folosit atunci cand nu gasim solutie mergand pe un anumit branch
        i = nod_col.sus
        while i !=nod_col:
            j = i.st
            while j!= i:
                j.coloana.counter += 1

                j.jos.sus = j
                j.sus.jos = j
                j = j.st
            i = i.sus

        nod_col.dr.st = nod_col
        nod_col.st.dr = nod_col

    def get_min_column(self):
        col = self.cap.dr
        min_col = col
        while col != self.cap:
            if col.counter < min_col.counter:
                min_col = col
            col = col.dr
        return min_col

    def cauta(self, depth=0):

        if self.stop:
            return

        if self.cap.dr == self.cap:
            #daca matricea nu mai are nicio coloana,i.e. a ramas doar capul matricei, ne oprim, am gasit solutie
            self.reconstruieste()
            self.stop=True
            return

        #parcurgem pasii algoritmului x
        col = self.get_min_column()
        self.cover(col)

        lin = col.jos
        while lin != col:
            self.solutii.append(lin)
            j = lin.dr
            while j != lin:
                #cover se ocupa si de liniile ce trebuie eliminate, nu doar de coloana
                self.cover(j.coloana)
                j = j.dr

            self.cauta(depth + 1)

            #refacem pasii si mergem pe alt branch, pe alta solutie
            lin = self.solutii.pop()
            col = lin.coloana
            j = lin.st
            while j != lin:
                self.uncover(j.coloana)
                j = j.st
            lin = lin.jos

        self.uncover(col)



def sablon_exact_cover(grila):
    #formam matricea de exact cover corespunzatoare sudoku-ului, aplicand constrangerile specifice jocului
    #fiecare combinatie de pozitie si valoare (9x9x9 = 729) corespunde liniilor matricei
    #constrangerile corespund coloanelor:
    #fiecare casuta din sudoku completata exact o data => 81 de coloane
    #fiecare valoare o singura data pe un rand => 81 de coloane
    #fiecare valoare o singura data pe o coloana => 81 de coloane
    #fiecare valoare o singura data in blocul din care face parte => 81 de coloane
    #Total = 324 coloane
    #practic, aceasta matrice de exact cover descrie toate felurile in care poate fi completat sudoku-ul
    matrice = []
    valori_reale = []
    for i in range(9):
        for j in range(9):
            #daca o celula din sudoku e deja completata, putem elimina din numarul de linii, scazand spatiul pe care lucram
            if grila[i][j]==0:
                for k in range(1, 10):
                    lin = [0] * 324
                    lin[9*i + j] = 1
                    lin[81 + 9*i + (k - 1)] = 1
                    lin[162 + 9*j + (k - 1)] = 1
                    b = (i // 3) * 3 + (j // 3)
                    lin[243 + 9*b + (k - 1)] = 1
                    matrice.append(lin)
                    valori_reale.append((i, j, k))
            else:
                k=grila[i][j]
                lin = [0] * 324
                lin[9 * i + j] = 1
                lin[81 + 9 * i + (k - 1)] = 1
                lin[162 + 9 * j + (k - 1)] = 1
                b = (i // 3) * 3 + (j // 3)
                lin[243 + 9 * b + (k - 1)] = 1
                matrice.append(lin)
                valori_reale.append((i, j, k))

    return matrice, valori_reale







def solve_sudoku(grila):

    matrice_exact_cover, valori_reale = sablon_exact_cover(grila)


    dlx = DLX(matrice_exact_cover, valori_reale)
    dlx.cauta()
    return dlx.careu



