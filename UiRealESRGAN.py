import tkinter as tk
import tkinter.ttk as ttk

from pygubu.widgets.scrollbarhelper import ScrollbarHelper


class UiRealESRGAN(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(UiRealESRGAN, self).__init__(master, **kw)
        self.FrameTitle = ttk.Frame(self)
        self.LabelIcon = ttk.Label(self.FrameTitle)
        self.img_realesrgan = tk.PhotoImage(file='realesrgan.png')
        self.LabelIcon.configure(image=self.img_realesrgan)
        self.LabelIcon.pack(padx='20', side='left')
        self.LabelApp = ttk.Label(self.FrameTitle)
        self.LabelApp.configure(font='{Arial} 24 {bold}', text='RealESRGAN GUI')
        self.LabelApp.pack(padx='10', side='left', fill='both', expand=True)
        self.FrameProcess = ttk.Frame(self.FrameTitle)
        self.ButtonStart = ttk.Button(self.FrameProcess)
        self.ButtonStart.configure(text=_('Start'))
        self.ButtonStart.pack(ipadx='2', padx='4', pady='4', side='left')
        self.ButtonStart.configure(command=self.start)
        self.ButtonStop = ttk.Button(self.FrameProcess)
        self.ButtonStop.configure(text=_('Stop'))
        self.ButtonStop.pack(ipadx='2', padx='4', pady='4', side='top')
        self.ButtonStop.configure(command=self.stop)
        self.FrameProcess.configure(height='200', width='200')
        self.FrameProcess.pack(padx='20', pady='30', side='top')
        self.FrameTitle.configure(height='200', width='200')
        self.FrameTitle.pack(fill='x', side='top')
        self.FrameInput = ttk.Labelframe(self)
        self.EntryInput = ttk.Entry(self.FrameInput)
        self.input_path = tk.StringVar(value='')
        self.EntryInput.configure(textvariable=self.input_path)
        self.EntryInput.pack(expand='true', fill='x', ipadx='2', padx='4', pady='4', side='left')
        self.ButtonInputFile = ttk.Button(self.FrameInput)
        self.ButtonInputFile.configure(text=_('Select File'))
        self.ButtonInputFile.pack(ipadx='2', padx='4', pady='4', side='left')
        self.ButtonInputFile.configure(command=self.get_input_file)
        self.ButtonInputDir = ttk.Button(self.FrameInput)
        self.ButtonInputDir.configure(text=_('Select Folder'))
        self.ButtonInputDir.pack(ipadx='2', padx='4', pady='4', side='right')
        self.ButtonInputDir.configure(command=self.get_input_dir)
        self.FrameInput.configure(height='200', text=_('Input'), width='200')
        self.FrameInput.pack(fill='x', padx='4', pady='4', side='top')
        self.FrameOutput = ttk.Labelframe(self)
        self.EntryOutput = ttk.Entry(self.FrameOutput)
        self.output_path = tk.StringVar(value='')
        self.EntryOutput.configure(textvariable=self.output_path)
        self.EntryOutput.pack(expand='true', fill='x', ipadx='2', padx='4', pady='4', side='left')
        self.ButtonOutputFile = ttk.Button(self.FrameOutput)
        self.ButtonOutputFile.configure(text=_('Select File'))
        self.ButtonOutputFile.pack(ipadx='2', padx='4', pady='4', side='left')
        self.ButtonOutputFile.configure(command=self.set_output_file)
        self.ButtonOutputDir = ttk.Button(self.FrameOutput)
        self.ButtonOutputDir.configure(text=_('Select Folder'))
        self.ButtonOutputDir.pack(ipadx='2', padx='4', pady='4', side='right')
        self.ButtonOutputDir.configure(command=self.set_output_dir)
        self.FrameOutput.configure(height='200', text=_('Output'), width='200')
        self.FrameOutput.pack(fill='x', padx='4', pady='4', side='top')
        self.FrameOption = ttk.Labelframe(self)
        self.LabelOutputFormat = ttk.Label(self.FrameOption)
        self.LabelOutputFormat.configure(text=_('Output Format'))
        self.LabelOutputFormat.pack(padx='4', pady='4', side='left')
        self.ComboboxOutputFormat = ttk.Combobox(self.FrameOption)
        self.output_format = tk.StringVar(value='')
        self.ComboboxOutputFormat.configure(state='readonly', textvariable=self.output_format, width='4')
        self.ComboboxOutputFormat.pack(ipadx='2', side='left')
        self.ComboboxOutputFormat.bind('<<ComboboxSelected>>', self.set_output_format, add='')
        self.LabelMode = ttk.Label(self.FrameOption)
        self.LabelMode.configure(text=_('Mode'))
        self.LabelMode.pack(padx='4', pady='4', side='left')
        self.ComboboxMode = ttk.Combobox(self.FrameOption)
        self.mode = tk.StringVar(value='')
        self.ComboboxMode.configure(state='readonly', textvariable=self.mode, width='28')
        self.ComboboxMode.pack(ipadx='2', side='left')
        self.ComboboxMode.bind('<<ComboboxSelected>>', self.set_mode, add='')
        self.CheckButtonTTAMode = ttk.Checkbutton(self.FrameOption)
        self.tta_mode = tk.BooleanVar(value=False)
        self.CheckButtonTTAMode.configure(text=_('TTA Mode'), variable=self.tta_mode, command=self.set_tta_mode)
        self.CheckButtonTTAMode.pack(ipadx='2', padx='4', pady='4', side='left')
        self.FrameOption.configure(height='200', text=_('Option'), width='200')
        self.FrameOption.pack(fill='x', padx='4', pady='4', side='top')
        self.FrameMessage = ttk.Labelframe(self)
        self.Scrollbarhelper = ScrollbarHelper(self.FrameMessage, scrolltype='both')
        self.TextMessage = tk.Text(self.Scrollbarhelper.container)
        self.TextMessage.configure(font='{Consolas} 10 {}', height='10', width='50', state='disabled')
        self.TextMessage.pack(fill='both', side='top', padx=4, pady=4)
        self.Scrollbarhelper.add_child(self.TextMessage)
        self.Scrollbarhelper.configure(usemousewheel=False)
        self.Scrollbarhelper.pack(expand='true', fill='both', side='top')
        self.FrameMessage.configure(height='200', text=_('Message'), width='200')
        self.FrameMessage.pack(expand='true', fill='both', padx='4', pady='4', side='top')
        self.configure(height='200', width='200')
        self.pack(expand='true', fill='both', side='top')

    def start(self):
        pass

    def stop(self):
        pass

    def get_input_file(self):
        pass

    def get_input_dir(self):
        pass

    def set_output_file(self):
        pass

    def set_output_dir(self):
        pass

    def set_output_format(self, event=None):
        pass

    def set_mode(self, event=None):
        pass

    def set_tta_mode(self):
        pass
