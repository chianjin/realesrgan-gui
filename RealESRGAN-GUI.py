import gettext
import os
import sys
import tkinter as tk

import locale
from RealESRGAN import RealESRGAN

if 'win' in sys.platform:
    os.environ['LANGUAGE'] = locale.getdefaultlocale()[0]
gettext.install(domain='RealESRGAN_GUI', localedir='locale')


class RealESRGANGui(tk.Tk):
    def __init__(self):
        super(RealESRGANGui, self).__init__()

        self._center()
        self.title('RealESRGAN GUI')
        self.iconphoto(False, tk.PhotoImage(file='realesrgan.png'))
        RealESRGAN(self).pack()

    def _center(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = screen_width * 1 // 2
        height = screen_height * 2 // 3
        screen_height = screen_height * 4 // 5
        left = (screen_width - width) // 2
        top = (screen_height - height) // 2
        self.wm_minsize(width, height)
        self.wm_resizable(True, True)
        self.wm_geometry(f'+{left}+{top}')

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    if sys.platform == 'win32':
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    RealESRGANGui().run()
