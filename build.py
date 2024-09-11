import subprocess
import os
import glob
import platform
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

APP_NAME = "RealESRGAN-GUI"
APP_VERSION = "0.4"
BUILD_DIR = Path("build")
RELEASE_DIR = Path("release")
REALESRGAN_DIR = Path("realesrgan")
ARCH = platform.architecture()[0][:2]

nuitka_cmd = [
    "nuitka",
    "--show-progress",
    "--show-memory",
    "--standalone",
    "--windows-console-mode=disable",
    "--windows-icon-from-ico=realesrgan.ico",
    "--include-data-dir=locale=locale",
    "--include-data-file=realesrgan.png=realesrgan.png",
    "--plugin-enable=tk-inter",
    f"--output-dir={BUILD_DIR}",
    "--verbose",
    "RealESRGAN-GUI.py"
]

def build_exec():
    process = subprocess.run(nuitka_cmd, shell=True)
    if process.returncode != 0:
        raise ChildProcessError('Nuitka building failed.')

def copy_realesrgan():
    os.system(f"XCOPY {REALESRGAN_DIR} {BUILD_DIR}\\{APP_NAME}.dist\\{REALESRGAN_DIR}\\ /S")

def create_portable():
    if not RELEASE_DIR.exists():
        RELEASE_DIR.mkdir()
    file_list = glob.glob(pathname=f'{BUILD_DIR}/{APP_NAME}.dist/**', recursive=True)
    file_list.sort()
    portable_file = RELEASE_DIR / f'{APP_NAME}_{APP_VERSION}_{ARCH}.zip'

    print('Creating portable package...')
    with ZipFile(portable_file, mode='w', compression=ZIP_DEFLATED) as zf:
        for file in file_list:
            print(file)
            file = Path(file)
            name_in_zip = "/".join(file.parts[2:])
            print(name_in_zip)
            if file.is_file():
                zf.write(file, name_in_zip)
    print('Creating portable package done.')


build_exec()
copy_realesrgan()
create_portable()

