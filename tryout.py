import keyboard
import time
from pynput import mouse

def on_click(x, y, button, pressed):
    conditie1=button==mouse.Button.left
    conditie2=pressed==True
    conditie3=0<x<500 and 0<y<500
    if conditie1 and conditie2 and conditie3:
        print(1)
        for i in range(100000000):
            x=1
        return False



with mouse.Listener(
        on_click=on_click) as listener:
    listener.join()
