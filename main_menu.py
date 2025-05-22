import sys
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from idle_cursor import Cursor
from screen_info import initial_y, initial_x,cale_catre_resurse
import os

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.inchide_tot)
        self.title("SecondCursorMainMenu")

        logo_path = os.path.join(cale_catre_resurse, "logo_cursor.ico")
        self.iconbitmap(logo_path)
        self.geometry(f"800x600")
        self.resizable(False, False)

        background_path = os.path.join(cale_catre_resurse, "background.png")
        self.imagine_background = Image.open(background_path)
        self.imagine_background = self.imagine_background.resize((800, 600))
        self.imagine_background = ImageTk.PhotoImage(self.imagine_background)

        background_label = tk.Label(self, image=self.imagine_background)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        cursor_path = os.path.join(cale_catre_resurse, "cursor1.png")
        image = Image.open(cursor_path).convert("RGBA")
        image = image.resize((50, 61), Image.NEAREST)
        data = np.array(image)
        verde = np.array([0, 255, 0, 255])
        mask = np.all(np.abs(data[:, :, :3] - verde[:3]) < 130, axis=-1)
        data[mask] = [0, 0, 0, 0]
        self.imagine_cursor = Image.fromarray(data)
        self.imagine_cursor = ImageTk.PhotoImage(self.imagine_cursor)
        self.label_cursor = tk.Label(self, image=self.imagine_cursor, bg="white")
        self.pozitie = [645, 74]
        self.label_cursor.place(x=self.pozitie[0], y=self.pozitie[1])

        self.cr = Cursor()

        instructiuni = """
        Odata lansat, cursorul devine idle in coltul stanga-jos al ecranului si poate fi comandat astfel:
            1.Click pe el pentru a-i oferi focus;
            2.Apesi tasta aferenta jocului dorit pentru detectie (Sudoku - "S", X si 0 - "X", Checkers - "C");
            3.Odata detectat careul de joc, in functie de jocul ales, ai urmatoarele perechi tasta-functie:
            
            •Pentru Sudoku:
                "Q" - completeaza integral sudoku 
                "W" - completeaza o anumita celula selectata de user prin click pe celula
            
            •Pentru X si 0:
                "Q" - joaca best out of 3 impotriva botului implicit al jocului
                "W" - joaca best out of 3 impotriva userului
            
            •Pentru Checkers:
                "Q" - joaca impotriva botului implicit al site-ului, respectand regula de force-jump
                
            4.In orice moment, pentru a intoarce cursorul in starea de repaus, apasati "ESC"
        """

        label_instructiuni = tk.Label(self, text=instructiuni, font=("Arial", 10), justify="left", anchor="w")
        label_instructiuni.pack(padx=10, pady=(150, 0), fill="x")

        buton_actiune = tk.Button(self,
                                  text="Lanseaza Cursor",
                                  font=("Arial", 20, "bold"),
                                  bg="black",
                                  fg="white",
                                  activebackground="gray",
                                  activeforeground="white",
                                  relief="groove",
                                  bd=0,
                                  command=lambda: self.lanseaza_cursor(buton_actiune)
                                  )
        buton_actiune.pack(pady=10)

    def lanseaza_cursor(self, buton_actiune):

        buton_actiune.config(text="Stop Cursor")
        buton_actiune.config(command=lambda: self.opreste_cursor(buton_actiune))
        self.label_cursor.place_forget()
        self.cr.lanseaza(self.label_cursor.winfo_rootx(), self.label_cursor.winfo_rooty())

    def opreste_cursor(self, buton_actiune):
        if self.cr.root.winfo_x() != initial_x and self.cr.root.winfo_y() != initial_y:
            return
        buton_actiune.config(text="Lanseaza Cursor")
        buton_actiune.config(command=lambda: self.lanseaza_cursor(buton_actiune))
        self.cr.opreste(self.label_cursor.winfo_rootx(), self.label_cursor.winfo_rooty())
        self.label_cursor.place(x=self.pozitie[0], y=self.pozitie[1])

    def inchide_tot(self):
        if self.cr.root is not None:
            try:
                self.cr.cleanup()
            except:
                pass
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    menu = Menu()
    menu.mainloop()
