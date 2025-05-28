import ctypes
import os
import sys

ctypes.windll.user32.SetProcessDPIAware(1)

screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

initial_x = screen_width - 70
initial_y = screen_height - 140

xratio = screen_width / 1920
yratio = screen_height / 1080

if getattr(sys, 'frozen', False):
    cale_catre_resurse = os.path.join(sys._MEIPASS, "resources")
else:
    cale_catre_resurse = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

if getattr(sys, 'frozen', False):
    cale_catre_templates = os.path.join(sys._MEIPASS, "sudoku/templates")
else:
    cale_catre_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sudoku/templates")