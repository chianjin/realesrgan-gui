#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class UiRealESRGAN(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(UiRealESRGAN, self).__init__(master, **kw)
        self.FrameTop = ttk.Frame(self)
        self.FrameTitle = ttk.Frame(self.FrameTop)
        self.LabelIcon = ttk.Label(self.FrameTitle)
        self.img_realesrgan = tk.PhotoImage(file="realesrgan.png")
        self.LabelIcon.configure(image=self.img_realesrgan, text="RN")
        self.LabelIcon.pack(side="left")
        self.LabelTitle = ttk.Label(self.FrameTitle)
        self.LabelTitle.configure(font="{Arial} 24 {bold}", text="RealESRGAN GUI")
        self.LabelTitle.pack(padx="20", side="left")
        self.FrameTitle.configure(height="200", width="200")
        self.FrameTitle.pack(padx="20", pady="10", side="left")
        self.FrameButton = ttk.Frame(self.FrameTop)
        self.ButtonStart = ttk.Button(self.FrameButton)
        self.ButtonStart.configure(text=_("Start"))
        self.ButtonStart.pack(padx="4", side="left")
        self.ButtonStart.configure(command=self.start)
        self.ButtonStop = ttk.Button(self.FrameButton)
        self.ButtonStop.configure(text=_("Stop"))
        self.ButtonStop.pack(side="left")
        self.ButtonStop.configure(command=self.stop)
        self.FrameButton.configure(height="200", width="200")
        self.FrameButton.pack(padx="20", side="right")
        self.FrameTop.configure(height="200", width="200")
        self.FrameTop.pack(fill="x", side="top")
        self.FrameInput = ttk.Labelframe(self)
        self.EntryInputPath = ttk.Entry(self.FrameInput)
        self.input_path = tk.StringVar(value="")
        self.EntryInputPath.configure(textvariable=self.input_path)
        self.EntryInputPath.pack(
            expand="true", fill="x", padx="4", pady="4", side="left"
        )
        self.ButtonInputFile = ttk.Button(self.FrameInput)
        self.ButtonInputFile.configure(text=_("Select File"))
        self.ButtonInputFile.pack(padx="4", pady="4", side="left")
        self.ButtonInputFile.configure(command=self.get_input_file)
        self.ButtonInputFolder = ttk.Button(self.FrameInput)
        self.ButtonInputFolder.configure(text=_("Select Folder"))
        self.ButtonInputFolder.pack(padx="4", pady="4", side="left")
        self.ButtonInputFolder.configure(command=self.get_input_folder)
        self.FrameInput.configure(height="200", text=_("Input"), width="200")
        self.FrameInput.pack(fill="x", padx="4", pady="4", side="top")
        self.FrameOutput = ttk.Labelframe(self)
        self.EntryOutputPath = ttk.Entry(self.FrameOutput)
        self.output_path = tk.StringVar(value="")
        self.EntryOutputPath.configure(textvariable=self.output_path)
        self.EntryOutputPath.pack(
            expand="true", fill="x", padx="4", pady="4", side="left"
        )
        self.ButtonOutputFile = ttk.Button(self.FrameOutput)
        self.ButtonOutputFile.configure(text=_("Select File"))
        self.ButtonOutputFile.pack(padx="4", pady="4", side="left")
        self.ButtonOutputFile.configure(command=self.set_output_file)
        self.ButtonOutputFolder = ttk.Button(self.FrameOutput)
        self.ButtonOutputFolder.configure(text=_("Select Folder"))
        self.ButtonOutputFolder.pack(padx="4", pady="4", side="left")
        self.ButtonOutputFolder.configure(command=self.set_output_folder)
        self.FrameOutput.configure(height="200", text=_("Output"), width="200")
        self.FrameOutput.pack(fill="x", padx="4", pady="4", side="top")
        self.FrameOption = ttk.Labelframe(self)
        self.FrameFormat = ttk.Frame(self.FrameOption)
        self.LabelFormat = ttk.Label(self.FrameFormat)
        self.LabelFormat.configure(text=_("Format"))
        self.LabelFormat.pack(side="left")
        self.ComboboxFormat = ttk.Combobox(self.FrameFormat)
        self.format = tk.StringVar(value="")
        self.ComboboxFormat.configure(
            state="readonly", textvariable=self.format, width="6"
        )
        self.ComboboxFormat.pack(padx="4", side="left")
        self.ComboboxFormat.bind("<<ComboboxSelected>>", self.set_format, add="")
        self.FrameFormat.configure(height="200", width="200")
        self.FrameFormat.pack(padx="4", pady="4", side="left")
        self.FrameMode = ttk.Frame(self.FrameOption)
        self.LabelMode = ttk.Label(self.FrameMode)
        self.LabelMode.configure(text=_("Mode"))
        self.LabelMode.pack(side="left")
        self.ComboboxMode = ttk.Combobox(self.FrameMode)
        self.mode = tk.StringVar(value="")
        self.ComboboxMode.configure(
            state="readonly", textvariable=self.mode, width="28"
        )
        self.ComboboxMode.pack(padx="4", side="left")
        self.ComboboxMode.bind("<<ComboboxSelected>>", self.set_mode, add="")
        self.FrameMode.configure(height="200", width="200")
        self.FrameMode.pack(padx="12", pady="4", side="left")
        self.CheckButtonTTAMode = ttk.Checkbutton(self.FrameOption)
        self.tta_mode = tk.StringVar(value="")
        self.CheckButtonTTAMode.configure(text=_("TTA Mode"), variable=self.tta_mode)
        self.CheckButtonTTAMode.pack(padx="4", pady="4", side="left")
        self.CheckButtonTTAMode.configure(command=self.use_tta_mode)
        self.FrameOption.configure(height="200", text=_("Option"), width="200")
        self.FrameOption.pack(fill="x", padx="4", pady="4", side="top")
        self.FrameMessage = ttk.Labelframe(self)
        self.FrameText = ttk.Frame(self.FrameMessage)
        self.TextMessage = tk.Text(self.FrameText)
        self.TextMessage.configure(font="TkFixedFont", height="10", width="50")
        self.TextMessage.pack(expand="true", fill="both", side="left")
        self.ScrollBarMessage = ttk.Scrollbar(self.FrameText)
        self.ScrollBarMessage.configure(orient="vertical")
        self.ScrollBarMessage.pack(expand="true", fill="y", side="top")
        self.FrameText.configure(height="200", width="200")
        self.FrameText.pack(expand="true", fill="both", padx="4", pady="4", side="top")
        self.FrameMessage.configure(height="200", text=_("Message"), width="200")
        self.FrameMessage.pack(
            expand="true", fill="both", padx="4", pady="4", side="top"
        )
        self.configure(height="200", width="200")
        self.pack(expand="true", fill="both", side="top")

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

    def set_format(self, event=None):
        pass

    def set_mode(self, event=None):
        pass

    def use_tta_mode(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = UiRealESRGAN(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
