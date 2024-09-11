import gettext
import sys
from threading import Thread
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from typing import Union

from UiRealESRGAN import UiRealESRGAN

REALESRGAN_EXEC = Path('realesrgan/realesrgan-ncnn-vulkan')
if 'win' in sys.platform:
    REALESRGAN_EXEC = REALESRGAN_EXEC.with_suffix('.exe')

gettext.install(domain='RealESRGAN_GUI', localedir='locale')

FILE_TYPES = (
        (_('Image File'), '*.png;*.jpg;*.jpeg;*.webp'),
        (_('PNG Image'), '*.png'),
        (_('JPEG Image'), '*.jpg;*.jpeg'),
        (_('Webp Image'), '*.webp')
    )

MODEL = (
        "realesrgan-x4plus",
        "realesrgan-x4plus-anime",
        "realesr-animevideov3-x2",
        "realesr-animevideov3-x3",
        "realesr-animevideov3-x4"
    )


class RealESRGAN(UiRealESRGAN):
    def __init__(self, master=None, **kw):
        super(RealESRGAN, self).__init__(master=master, **kw)

        # set ui configure
        self._tta_mode = 0
        self.tta_mode.set(self._tta_mode)

        self.ComboboxScale.configure(values='2 3 4')
        self._scale = 4
        self.scale.set(self._scale)
        self.ComboboxScale.configure(state='disable')

        self.ComboboxFormat.configure(values='png jpg webp')
        self._format = 'png'
        self.format.set(self._format)
        self.ComboboxFormat.configure(state='disabled')

        self.ComboboxModel.configure(values=MODEL)
        self._model = MODEL[0]
        self.model.set(self._model)
        self.ComboboxModel.configure(state='disabled')

        self.CheckButtonTTAMode.configure(state='disabled')
        self.ButtonStart.configure(state='disabled')
        self.ButtonStop.configure(state='disable')
        self.ButtonOutputFile.configure(state='disabled')
        self.ButtonOutputFolder.configure(state='disabled')

        self._input_path: Union[None, str, Path] = None
        self._output_path: Union[None, str, Path] = None
        self._input_type: Union[None, str] = None
        self._output_custom = False
        self._is_folder = False
        self._process = None

        if REALESRGAN_EXEC.exists():
            self._realesrgan_exec = REALESRGAN_EXEC
        else:
            self._realesrgan_exec = None

        self._check_exec()

    def get_input_file(self):
        input_file = askopenfilename(title=_('Select Image File'), filetypes=FILE_TYPES)
        if input_file:
            self._output_custom = False
            self._input_path = Path(input_file)
            self.input_path.set(self._input_path)
            self._input_type = 'file'
            self._set_output()
            self.ButtonOutputFile.configure(state='normal')
            self.ButtonOutputFolder.configure(state='disabled')

        self._toggle_start()

    def get_input_folder(self):
        input_folder = askdirectory(title=_('Select Images Folder'), mustexist=True)
        if input_folder:
            self._output_custom = False
            self._is_folder = True
            self._input_path = Path(input_folder)
            self.input_path.set(self._input_path)
            self._input_type = 'dir'
            self._set_output()
            self.ButtonOutputFile.configure(state='disabled')
            self.ButtonOutputFolder.configure(state='normal')
        self._toggle_start()

    def set_output_file(self):
        output_file = asksaveasfilename(
                title=_('Set Output File'),
                confirmoverwrite=True,
                defaultextension=f'.{self._format}',
                filetypes=FILE_TYPES,
                initialdir=self._input_path.parent if self._input_path else None,
                initialfile=self._output_path.stem if self._input_path else None
                )
        if output_file:
            self._output_custom = True
            self._output_path = Path(output_file)
            self._format = self._output_path.suffix[1:]
            self.output_path.set(self._output_path)
            self.format.set(self._format)
        self._toggle_start()

    def set_output_folder(self):
        output_folder = askdirectory(title=_('Set Output Folder'))
        if output_folder:
            self._output_custom = True
            self._output_path = Path(output_folder)
            self.output_path.set(self._output_path)
        self._toggle_start()

    def set_scale(self, event=None):
        self._scale = self.scale.get()
        self._set_output()

    def set_format(self, event=None):
        self._format = self.format.get()
        self._set_output()

    def set_model(self, event=None):
        self._model = self.model.get()
        self._set_output()

    def set_tta_mode(self):
        self._tta_mode = self.tta_mode.get()
        self._set_output()

    def start(self):
        if not self._realesrgan_exec:
            return None

        if self._is_folder:
            output_folder = Path(self.output_path.get())
            if not output_folder.exists():
                if askyesno(
                    title=_("Create Folder"),
                    message=_("Output folder dose not exists. Create it?"),
                ):
                    output_folder.mkdir()
                else:
                    return None

        self.ButtonStart.configure(state= tk.DISABLED)
        self.ButtonStop.configure(state=tk.NORMAL)
        # Launch the process in a separate thread
        process_thread = Thread(target=self._run_process)
        process_thread.start()

    def stop(self):
        self._process.kill()
        self._process.wait()
        self.TextMessage.insert(tk.END, _('\nrealesrgan-ncnn-vulkan process terminated.\n'))
        self.ButtonStart.configure(state=tk.NORMAL)
        self.ButtonStop.configure(state=tk.DISABLED)

    def _set_output(self):
        if self._output_custom:
            return None

        output_name = f'{self._input_path.stem}-{self._scale}x-{self._model}'
        print(self._tta_mode)
        if self._tta_mode:
            output_name = f'{output_name}-tta'
        if self._input_type == 'file':
            output_name = f'{output_name}.{self._format}'

        self._output_path = self._input_path.parent / output_name
        self.output_path.set(self._output_path)

    def _run_process(self):
        command = [
            str(REALESRGAN_EXEC),
            "-i", self.input_path.get(),
            "-o", self.output_path.get(),
            "-s", self.scale.get(),
            "-n", self.model.get(),
            "-f", self.format.get(),
            "-v"
        ]

        if self.tta_mode.get():
            command.append("-x")

        self.TextMessage.insert(tk.END, " ".join(command) + "\n")

        self._process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        # Read and display real-time output in the GUI
        with self._process.stdout:
            for line in iter(self._process.stdout.readline, ''):
                self.TextMessage.insert(tk.END, line)
                self.TextMessage.yview(tk.END)
                #self.master.update()
        # Enable the button after the process completes
        self.ButtonStart.configure(state=tk.NORMAL)

    def _enable_widgets(self, enable=True):
        buttons = (
                self.ButtonStart,
                self.ButtonInputFile,
                self.ButtonInputFolder,
                self.ButtonOutputFile,
                self.ButtonOutputFolder,
                self.CheckButtonTTAMode,
                self.EntryInputPath,
                self.EntryOutputPath,
                )
        combobox = (
                self.ComboboxFormat,
                self.ComboboxModel,
                )
        if enable:
            for w in buttons:
                w.configure(state='normal')
            for w in combobox:
                w.configure(state='readonly')
        else:
            for widgets in (buttons, combobox):
                for w in widgets:
                    w.configure(state='disabled')

    def _toggle_start(self):
        if self._input_path and self._input_path.exists() and self._output_path:
            self.ButtonStart.configure(state='normal')
            self.ComboboxScale.configure(state='readonly')
            self.ComboboxFormat.configure(state='readonly')
            self.ComboboxModel.configure(state='readonly')
            self.CheckButtonTTAMode.configure(state='normal')
        else:
            self.ButtonStart.configure(state='disabled')
            self.ComboboxScale.configure(state='disabled')
            self.ComboboxFormat.configure(state='disabled')
            self.ComboboxModel.configure(state='disabled')
            self.CheckButtonTTAMode.configure(state='disabled')

    def _check_exec(self):
        if not self._realesrgan_exec:
            self.TextMessage.configure(state='normal')
            self.TextMessage.insert(
                    'end',
                    _(
                            'realesrgan-ncnn-vulkan executable file not found! \n'
                            'Please download from https://github.com/xinntao/Real-ESRGAN '
                            'and extract to realesrgan folder.'
                            )
                    )
            self.TextMessage.configure(state='disabled')