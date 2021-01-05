import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--hidden-import=PySide2.QtXml',
    '--name=Camera',
    '--onefile',
    '--windowed',
])

# pyinstaller --onefile --windowed --hidden-import PySide2.QtXml main.py