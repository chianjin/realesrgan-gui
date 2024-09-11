#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class UiRealESRGAN(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(UiRealESRGAN, self).__init__(master, **kw)

        # Top Frame
        self.FrameTop = ttk.Frame(self)
        ## Title Frame
        self.FrameTitle = ttk.Frame(self.FrameTop)
        ## Title Icon
        self.img_realesrgan = tk.PhotoImage(file="realesrgan.png")
        self.LabelIcon = ttk.Label(self.FrameTitle, image=self.img_realesrgan, text="RN")
        self.LabelIcon.pack(side="left")
        ## Title Text
        self.LabelTitle = ttk.Label(self.FrameTitle, font="{Arial} 24 {bold}", text="RealESRGAN GUI")
        self.LabelTitle.pack(padx="20", side="left")
        ## Title Frame Pack
        self.FrameTitle.pack(padx="20", pady="10", side="left")
        ## Button Frame
        self.FrameButton = ttk.Frame(self.FrameTop)
        ### Start Button
        self.ButtonStart = ttk.Button(self.FrameButton, text=_("Start"), command=self.start)
        self.ButtonStart.pack(padx="4", side="left")
        ### Stop Button
        self.ButtonStop = ttk.Button(self.FrameButton, text=_("Stop"), command=self.stop)
        self.ButtonStop.pack(padx="4", side="left")
        ## Button Frame Pack
        self.FrameButton.pack(padx="20", side="right")
        # Top Frame Pack
        self.FrameTop.pack(fill="x", side="top")
        
        # Input Frame
        self.FrameInput = ttk.Labelframe(self, text=_("Input"))
        ## Input Path
        self.input_path = tk.StringVar(value="")
        self.EntryInputPath = ttk.Entry(self.FrameInput, textvariable=self.input_path)
        self.EntryInputPath.pack(
            expand=True, fill="x", padx="4", pady="4", side="left"
        )
        ## Input File Button
        self.ButtonInputFile = ttk.Button(self.FrameInput, text=_("Select File"), command=self.get_input_file)
        self.ButtonInputFile.pack(padx="4", pady="4", side="left")
        ## Input Folder Button
        self.ButtonInputFolder = ttk.Button(self.FrameInput, text=_("Select Folder"), command=self.get_input_folder)
        self.ButtonInputFolder.pack(padx="4", pady="4", side="left")
        ## Input Frame Pack
        self.FrameInput.pack(fill="x", padx="4", pady="4", side="top")
        # Output Frame
        self.FrameOutput = ttk.Labelframe(self, text=_("Output"))
        ## Output Path
        self.output_path = tk.StringVar(value="")
        self.EntryOutputPath = ttk.Entry(self.FrameOutput, textvariable=self.output_path)
        self.EntryOutputPath.pack(
            expand=True, fill="x", padx="4", pady="4", side="left"
        )
        ## Output File Button
        self.ButtonOutputFile = ttk.Button(self.FrameOutput, text=_("Select File"), command=self.set_output_file)
        self.ButtonOutputFile.pack(padx="4", pady="4", side="left")
        ## Output Folder Button
        self.ButtonOutputFolder = ttk.Button(self.FrameOutput, text=_("Select Folder"), command=self.set_output_folder)
        self.ButtonOutputFolder.pack(padx="4", pady="4", side="left")
        # Output Frame Pack
        self.FrameOutput.pack(fill="x", padx="4", pady="4", side="top")
        
        # Option Frame
        self.FrameOption = ttk.Labelframe(self, text=_("Option"))
        ## Scale Frame
        self.FrameScale = ttk.Frame(self.FrameOption)
        self.LabelScale = ttk.Label(self.FrameScale, text=_("Scale"))
        self.LabelScale.pack(side="left")
        self.scale = tk.StringVar(value="4")
        self.ComboboxScale = ttk.Combobox(self.FrameScale, state="readonly", textvariable=self.scale, width=2)
        self.ComboboxScale.pack(padx=4, pady=4, side="left")
        self.ComboboxScale.bind("<<ComboboxSelected>>", self.set_scale)
        self.FrameScale.pack(padx=4, pady=4, side="left")
        ## Format Frame
        self.FrameFormat = ttk.Frame(self.FrameOption)
        ### Format Label
        self.LabelFormat = ttk.Label(self.FrameFormat, text=_("Format"))
        self.LabelFormat.pack(side="left")
        ### Format Combobox
        self.format = tk.StringVar()
        self.ComboboxFormat = ttk.Combobox(self.FrameFormat, state="readonly", textvariable=self.format, width=6)
        self.ComboboxFormat.pack(padx="4", side="left")
        self.ComboboxFormat.bind("<<ComboboxSelected>>", self.set_format)
        self.FrameFormat.pack(padx="4", pady="4", side="left")
        ## Mode Frame
        self.FrameModel = ttk.Frame(self.FrameOption)
        ### Mode Label
        self.LabelModel = ttk.Label(self.FrameModel, text=_("Model"))
        self.LabelModel.pack(side="left")
        ### Model Combobox
        self.model = tk.StringVar()
        self.ComboboxModel = ttk.Combobox(self.FrameModel, state="readonly", textvariable=self.model, width=28)
        self.ComboboxModel.pack(padx="4", side="left")
        self.ComboboxModel.bind("<<ComboboxSelected>>", self.set_model, add="")
        ## Frame Model Pack
        self.FrameModel.pack(padx="4", pady="4", side="left")
        ## Check Button TTA Mode
        self.tta_mode = tk.IntVar()
        self.CheckButtonTTAMode = ttk.Checkbutton(
            self.FrameOption,
            text=_("TTA Mode"),
            variable=self.tta_mode,
            command=self.set_tta_mode)
        self.CheckButtonTTAMode.pack(padx="4", pady="4", side="left")
        # Option Frame Pack
        self.FrameOption.pack(fill="x", padx="4", pady="4", side="top")
        
        # Message Frame
        self.FrameMessage = ttk.Labelframe(self, text=_("Message"))
        ## Frame Text
        self.FrameText = ttk.Frame(self.FrameMessage)
        ## Text Message
        self.TextMessage = tk.Text(self.FrameText, font='{Microsoft Yahei Mono} 10 {}', height="10", width=50)
        self.TextMessage.pack(expand=True, fill="both", side="left")
        self.ScrollBarMessage = ttk.Scrollbar(self.FrameText, orient="vertical")
        self.ScrollBarMessage.pack(expand=True, fill="y", side="top")
        self.TextMessage.configure(yscrollcommand=self.ScrollBarMessage.set)
        self.ScrollBarMessage.configure(command=self.TextMessage.yview)
        ## Frame Text Pack
        self.FrameText.pack(expand=True, fill="both", padx="4", pady="4", side="top")
        # Frame Message Pack
        self.FrameMessage.pack(expand=True, fill="both", padx="4", pady="4", side="top")
        
        # Self Frame
        self.pack(expand=True, fill="both", side="top")

    def start(self):
        pass

    def stop(self):
        pass

    def get_input_file(self):
        pass

    def get_input_folder(self):
        pass

    def set_output_file(self):
        pass

    def set_output_folder(self):
        pass

    def set_scale(self, event=None):
        pass

    def set_format(self, event=None):
        pass

    def set_model(self, event=None):
        pass

    def set_tta_mode(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = UiRealESRGAN(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
