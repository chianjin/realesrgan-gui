call .venv\Scripts\activate.bat
nuitka --show-progress --show-memory --standalone --windows-console-mode=disable^
 --windows-icon-from-ico=realesrgan.ico --include-raw-dir=realesrgan=realesrgan^
 --include-data-dir=locale=locale --include-data-file=realesrgan.png=realesrgan.png^
 --plugin-enable=tk-inter --output-dir=build RealESRGAN-GUI.py --verbose
