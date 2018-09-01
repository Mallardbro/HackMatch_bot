import time
import win32gui
from directkeys import PressKey, ReleaseKey, J, K
import time
import win32gui

from directkeys import PressKey, ReleaseKey, J, K

toplist, winlist = [], []


def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


win32gui.EnumWindows(enum_cb, toplist)
# matching = [(hwnd, title) for hwnd, title in winlist if 'notepad' in title.lower()]
window = win32gui.FindWindow(None, 'Untitled - Notepad')
win32gui.SetForegroundWindow(window)
# bbox = win32gui.GetWindowRect(window)
# img = ImageGrab.grab(bbox)
# img.show()


for _ in [J, J, K, J]:
    PressKey(_)
    time.sleep(0.02)
    ReleaseKey(_)
    time.sleep(0.02)
