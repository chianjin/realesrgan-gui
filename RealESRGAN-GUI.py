import gettext
import locale
import os
import platform
import tkinter as tk

from RealESRGAN import RealESRGAN

if platform.system() == 'Windows':
    os.environ['LANGUAGE'] = locale.getdefaultlocale()[0]
gettext.install(domain='RealESRGAN_GUI', localedir='locale')


class RealESRGANGui(tk.Tk):
    def __init__(self):
        super(RealESRGANGui, self).__init__()

        self.title('RealESRGAN GUI')
        self.iconphoto(False, tk.PhotoImage(file='realesrgan.png'))
        RealESRGAN(self).pack()
        self._center()

    def _center(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = screen_width * 1 // 2
        window_height = screen_height * 2 // 3
        screen_height = screen_height * 4 // 5
        left = (screen_width - window_width) // 2
        top = (screen_height - window_height) // 2
        self.wm_minsize(window_width, window_height)
        self.wm_resizable(True, True)
        self.wm_geometry(f'+{left}+{top}')

    def run(self):
        #self.eval('tk::PlaceWindow . center')
        self.mainloop()


if __name__ == '__main__':
    if platform.system() == 'Windows' and int(platform.version().split('.')[0]) >= 10:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    RealESRGANGui().run()
