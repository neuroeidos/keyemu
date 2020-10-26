import keyboard, sys, win32gui, re, time, win32api, win32con

config = {'processName': 'KurtzPel  ', 'status': False, 'hwnd': None}
combos = {
  "list": [
    "mouse1,mouse1,mouse1",
    "mouse1,mouse1,mouse2",
    "mouse1,mouse1,mouse1_hold",
    "mouse1,mouse2,mouse2,mouse2",
    "shift,mouse1,mouse1,mouse1_hold",
    "shift,mouse1,mouse1,mouse2"
  ]
}

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
w = WindowMgr()

def getGameName(hwnd, ctx):
    if win32gui.IsWindowVisible( hwnd ):
        if win32gui.GetWindowText(hwnd) == config['processName']:
            config['status'] = True
            config['hwnd'] = hwnd
            w.find_window_wildcard(win32gui.GetWindowText(hwnd))
            w.set_foreground()
            print('> Window found: ' + hex(hwnd), win32gui.GetWindowText(hwnd))
            print('> Key-binds: [1-6] numkeys')
        else:
            config['status'] = False

def loadWindow():
    win32gui.EnumWindows(getGameName, None)

def mouse1():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse1_hold():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse2():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def combo_loader(data):
    data = data.split(',')
    print(data)
    for str in data:
        time.sleep(.1)
        if str == "shift":
            keyboard.press_and_release('shift')
        time.sleep(.1)
        if str == "mouse1":
            mouse1()
        time.sleep(.1)
        if str == "mouse1_hold":
            mouse1_hold()
        if str == "mouse2":
            mouse2()

def main():
    loadWindow()
    keyboard.add_hotkey('1', lambda: combo_loader(combos['list'][0]))
    keyboard.add_hotkey('2', lambda: combo_loader(combos['list'][1]))
    keyboard.add_hotkey('3', lambda: combo_loader(combos['list'][2]))
    keyboard.add_hotkey('4', lambda: combo_loader(combos['list'][3]))
    keyboard.add_hotkey('5', lambda: combo_loader(combos['list'][4]))
    keyboard.add_hotkey('6', lambda: combo_loader(combos['list'][5]))
    keyboard.wait()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(e)