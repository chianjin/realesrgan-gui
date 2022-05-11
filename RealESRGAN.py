import gettext
import sys
from threading import Thread, Lock
from pathlib import Path
from subprocess import PIPE, Popen, STDOUT, CREATE_NO_WINDOW
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from typing import Union

from UiRealESRGAN import UiRealESRGAN

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

        self.ComboboxFormat.configure(values='png jpg webp')
        self._format = 'png'
        self.format.set(self._format)
        self.ComboboxFormat.configure(state='disabled')

        self.ComboboxMode.configure(values=MODE)
        self._mode = MODE[0]
        self.mode.set(self._mode)
        self.ComboboxMode.configure(state='disabled')

        self.CheckButtonTTAMode.configure(state='disabled')
        self.ButtonStart.configure(state='disabled')
        self.ButtonOutputFile.configure(state='disabled')
        self.ButtonOutputFolder.configure(state='disabled')

        self.TextMessage.configure(yscrollcommand=self.ScrollBarMessage.set)
        self.ScrollBarMessage.configure(command=self.TextMessage.yview)

        self._input_path: Union[None, str, Path] = None
        self._output_path: Union[None, str, Path] = None
        self._input_type: Union[None, str] = None
        self._output_custom = False

        self._message = ''
        self._message_lock = Lock()
        self._process: Union[Popen, None] = None
        self._thread: Union[Thread, None] = None

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

    def set_format(self, event=None):
        self._format = self.format.get()
        if self._output_path and self._input_type == 'file':
            self._output_path = self._output_path.parent / f'{self._output_path.stem}.{self._format}'
            self.output_path.set(self._output_path)

    def set_mode(self, event=None):
        self._mode = self.mode.get()
        self._set_output()

    def set_tta_mode(self):
        self._tta_mode = self.tta_mode.get()
        self._set_output()

    def start(self):
        if not self._realesrgan_exec:
            return None

        self._enable_widgets(False)
        if self._input_type == 'dir' and not self._output_path.exists():
            self._output_path.mkdir()
        cmd_line = [self._realesrgan_exec, '-i', self._input_path, '-o', self._output_path, '-v']
        if self._input_type == 'dir' and self._format != 'png':
            cmd_line.extend(('-f', self._format))
        if self._mode != MODE[0]:
            cmd_line.extend(('-n', self._mode))
        if self._tta_mode:
            cmd_line.append('-x')

        self.TextMessage.configure(state='normal')
        self.TextMessage.delete('0.0', 'end')
        self.TextMessage.insert('end', ' '.join([str(arg) for arg in cmd_line]))
        self.TextMessage.insert('end', '\n')
        self.TextMessage.configure(state='disabled')

        self._thread = Thread(target=self._realesrgan, args=(cmd_line,), daemon=True)
        self._thread.start()
        self._update_message()

    def stop(self):
        if self._process:
            self._process.kill()
            self.TextMessage.configure(state='normal')
            self.TextMessage.insert('end', '========== Stop ==========\n')
            self.TextMessage.configure(state='disabled')
            self._process = None
        self._enable_widgets()

    def _set_output(self):
        if self._output_custom:
            return None

        output_name = f'{self._input_path.stem}-{self._mode}'
        if self._tta_mode:
            output_name = f'{output_name}-tta'
        if self._input_type == 'file':
            output_name = f'{output_name}.{self._format}'

        self._output_path = self._input_path.parent / output_name
        self.output_path.set(self._output_path)

    def _update_message(self):
        message = ''
        with self._message_lock:
            message, self._message = self._message, ''

        if message:
            self.TextMessage.configure(state='normal')
            self.TextMessage.insert('end', message)
            self.TextMessage.see('end')
            self.TextMessage.configure(state='disabled')
        if self._thread.is_alive():
            self.TextMessage.after(500, self._update_message)

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
            self.ComboboxFormat.configure(state='readonly')
            self.ComboboxMode.configure(state='readonly')
            self.CheckButtonTTAMode.configure(state='normal')
        else:
            self.ButtonStart.configure(state='disabled')
            self.ComboboxFormat.configure(state='disabled')
            self.ComboboxMode.configure(state='disabled')
            self.CheckButtonTTAMode.configure(state='disabled')

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

    def _realesrgan(self, cmd_line):
        self._process = Popen(cmd_line, stdout=PIPE, stderr=STDOUT, encoding='UTF-8')
        try:
            while self._process.poll() is None:
                message = self._process.stdout.readline()
                with self._message_lock:
                    self._message += message
            if self._process.returncode:
                self.TextMessage.configure(state='normal')
                self.TextMessage.insert(
                        'end',
                        _(
                                '====================================\n'
                                'Something wrong, the error code is {}.\n'
                                'Please run the above commandline directly in Terminal,\n'
                                'check whether it can run correctly.\n'
                                '===================================='
                                ).format(self._process.returncode)

                        )
                self.TextMessage.configure(state='disabled')
            self._process = None
        except AttributeError:
            pass
        finally:
            self._enable_widgets()
