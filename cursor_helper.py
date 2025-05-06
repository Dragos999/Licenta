import ctypes
import time
class pt(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class RealCursor:
    def __init__(self):
        self.p=pt()
        self.key={'1':0x31,'2':0x32,'3':0x33,'4':0x34,'5':0x35,'6':0x36,'7':0x37,'8':0x38,'9':0x39}
    def get_cursor_position(self):


        ctypes.windll.user32.GetCursorPos(ctypes.byref(self.p))
        return self.p.x, self.p.y

    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)

        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def hold_click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)

    def release_click(self):
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def realistic_click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def press_key(self,keyToPress):
        ctypes.windll.user32.keybd_event(self.key[keyToPress], 0, 0, 0)

        ctypes.windll.user32.keybd_event(self.key[keyToPress], 0, 2, 0)

    def set_cursor_position(self,pos):
        ctypes.windll.user32.SetCursorPos(pos[0],pos[1])

    def set_cursor_position_and_lock(self,pos):
        ctypes.windll.user32.SetCursorPos(pos[0], pos[1])
        limite = ctypes.wintypes.RECT(pos[0]-2,pos[1]-2,pos[0]+2,pos[1]+2)
        ctypes.windll.user32.ClipCursor(ctypes.byref(limite))


    def unlock(self):
        ctypes.windll.user32.ClipCursor(None)