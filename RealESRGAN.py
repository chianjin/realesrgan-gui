import gettext
import sys
import tkinter as tk
from multiprocessing import Process, Queue
from pathlib import Path
from subprocess import PIPE, Popen, STDOUT
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

from UiRealESRGAN import UiRealESRGAN

CREATE_NO_WINDOW = 134217728  # win32process.134217728

if 'win' in sys.platform:
    REALESRGAN_EXEC = Path('realesrgan/realesrgan-ncnn-vulkan.exe')
else:
    REALESRGAN_EXEC = Path('realesrgan/realesrgan-ncnn-vulkan')

gettext.install(domain='RealESRGAN_GUI', localedir='locale')

FILE_TYPES = (
        (_('Image File'), '*.png;*.jpg;*.jpeg;*.webp'),
        (_('PNG Image'), '*.png'),
        (_('JPEG Image'), '*.jpg;*.jpeg'),
        (_('Webp Image'), '*.webp')
        )

MODE = (
        'realesrgan-x4plus',
        'realesrgan-x4plus-anime',
        'realesrnet-x4plus',
        'RealESRGANv2-animevideo-xsx2',
        'RealESRGANv2-animevideo-xsx4',
        # 'RealESRGANv2-anime-xsx2',
        # 'RealESRGANv2-anime-xsx4'
        )


class RealESRGAN(UiRealESRGAN):
    def __init__(self, master=None, **kw):
        super(RealESRGAN, self).__init__(master=master, **kw)

        # set ui configure
        self._tta_mode = False
        self.tta_mode.set(self._tta_mode)

        self.ComboboxOutputFormat.configure(values='png jpg webp')
        self._output_format = 'png'
        self.output_format.set(self._output_format)

        self.ComboboxMode.configure(values=MODE)
        self._mode = MODE[0]
        self.mode.set(self._mode)

        self.ButtonStart.configure(state='disabled')

        self.ButtonOutputFile.configure(state='disabled')
        self.ButtonOutputDir.configure(state='disabled')

        self._input_path: None | str | Path = None
        self._output_path: None | str | Path = None
        self._input_type: None | str = None

        self._queue: Queue | None = None
        self._sub_process: Process | None = None

        if REALESRGAN_EXEC.exists():
            self._realesrgan_exec = REALESRGAN_EXEC
        else:
            self._realesrgan_exec = None

        self._check_exec()

    def get_input_file(self):
        input_file = askopenfilename(title=_('Select Image File'), filetypes=FILE_TYPES)
        if input_file:
            self._input_path = Path(input_file)
            self._output_path = self._input_path.parent / f'{self._input_path.stem}-{self._mode}.{self._output_format}'
            self.input_path.set(self._input_path)
            self.output_path.set(self._output_path)
            self._input_type = 'file'
            self.ButtonOutputFile.configure(state='normal')
            self.ButtonOutputDir.configure(state='disabled')

        self._toggle_start()

    def get_input_dir(self):
        input_dir = askdirectory(title=_('Select Images Folder'), mustexist=True)
        if input_dir:
            self._input_path = Path(input_dir)
            self._output_path = self._input_path.parent / f'{self._input_path.stem}-{self._mode}'
            self.input_path.set(self._input_path)
            self.output_path.set(self._output_path)
            self._input_type = 'dir'
            self.ButtonOutputFile.configure(state='disabled')
            self.ButtonOutputDir.configure(state='normal')
        self._toggle_start()

    def set_output_file(self):
        output_file = asksaveasfilename(
                title=_('Set Output File'),
                confirmoverwrite=True,
                defaultextension=f'.{self._output_format}',
                filetypes=FILE_TYPES,
                initialdir=self._input_path.parent if self._input_path else None,
                initialfile=self._output_path.stem if self._input_path else None
                )
        if output_file:
            self._output_path = Path(output_file)
            self._output_format = self._output_path.suffix[1:]
            self.output_path.set(self._output_path)
            self.output_format.set(self._output_format)
        self._toggle_start()

    def set_output_dir(self):
        output_dir = askdirectory(title=_('Set Output Folder'))
        if output_dir:
            self._output_path = Path(output_dir)
            self.output_path.set(self._output_path)
        self._toggle_start()

    def set_output_format(self, event=None):
        self._output_format = self.output_format.get()
        if self._output_path and self._input_type == 'file':
            self._output_path = self._output_path.parent / f'{self._output_path.stem}.{self._output_format}'
            self.output_path.set(self._output_path)

    def set_mode(self, event=None):
        self._mode = self.mode.get()
        if self._output_path and self._input_type == 'file':
            self._output_path = self._output_path.parent / f'{self._input_path.stem}-{self._mode}.{self._output_format}'
        else:
            self._output_path = self._input_path.parent / f'{self._input_path.name}-{self._mode}'
        self.output_path.set(self._output_path)

    def start(self):
        if not self._realesrgan_exec:
            return None

        self._enable_widgets(False)
        if self._input_type == 'dir' and not self._output_path.exists():
            self._output_path.mkdir()
        cmd_line = [self._realesrgan_exec, '-i', self._input_path, '-o', self._output_path, '-v']
        if self._input_type == 'dir' and self._output_format != 'png':
            cmd_line.extend(('-f', self._output_format))
        if self._mode != MODE[0]:
            cmd_line.extend(('-n', self._mode))
        if self._tta_mode:
            cmd_line.append('-x')

        self.TextMessage.configure(state='normal')
        self.TextMessage.delete('0.0', 'end')
        self.TextMessage.insert('end', ' '.join([str(arg) for arg in cmd_line]))
        self.TextMessage.insert('end', '\n')
        self.TextMessage.configure(state='disabled')

        self._queue = Queue()
        self._sub_process = Process(
                target=realesrgan,
                args=(self._queue, cmd_line)
                )
        self._sub_process.start()
        self._get_messages()

    def stop(self):
        if self._sub_process and self._sub_process.is_alive():
            self._sub_process.terminate()
            self.TextMessage.configure(state='normal')
            self.TextMessage.insert('end', _('!!!!!!!!!! User Terminate !!!!!!!!!!\n'))
            self.TextMessage.configure(state='disabled')
            # self.TextMessage.update_idletasks()
        self._enable_widgets()

    def _get_messages(self):
        self.TextMessage.configure(state='normal')
        while not self._queue.empty():
            self.TextMessage.insert('end', self._queue.get())
            self.TextMessage.see('end')
        self.TextMessage.configure(state='disabled')

        if self._sub_process.is_alive():
            self.TextMessage.after(500, self._get_messages)
        else:
            self._enable_widgets()

        # self.TextMessage.update_idletasks()

    def _enable_widgets(self, enable=True):
        buttons = (
                self.ButtonStart,
                self.ButtonInputFile,
                self.ButtonInputDir,
                self.ButtonOutputFile,
                self.ButtonOutputDir,
                self.CheckButtonTTAMode,
                self.EntryInput,
                self.EntryOutput,
                )
        combobox = (
                self.ComboboxOutputFormat,
                self.ComboboxMode,
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
        else:
            self.ButtonStart.configure(state='disabled')

    def _check_exec(self):
        if not self._realesrgan_exec:
            self.TextMessage.configure(state='normal')
            self.TextMessage.insert(
                    'end',
                    _(
                            'realesrgan-ncnn-vulkan executable file not found! \n'
                            '================================================= \n'
                            'Please download from https://github.com/xinntao/Real-ESRGAN '
                            'and extract to realesrgan folder.'
                            )
                    )
            self.TextMessage.configure(state='disabled')


def realesrgan(queue: Queue, cmd_line):
    with Popen(cmd_line, stdout=PIPE, stderr=STDOUT, creationflags=134217728) as sub_process:
        while True:
            return_code = sub_process.poll()
            if return_code is None:
                queue.put(sub_process.stdout.readline())
            else:
                queue.put(sub_process.stdout.read())
                break
    return return_code
