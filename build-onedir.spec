# PyInstaller spec for onedir debug build with robust Qt collection
# Usage: pdm run pyinstaller build-onedir.spec

import os
from PyInstaller.utils.hooks import collect_all

# Collect everything from PySide6 and shiboken6
pyside6_datas, pyside6_binaries, pyside6_hiddenimports = collect_all('PySide6')
shiboken6_datas, shiboken6_binaries, shiboken6_hiddenimports = collect_all('shiboken6')

datas = pyside6_datas + shiboken6_datas + [
    ('po_app/assets', 'assets'),
]

binaries = pyside6_binaries + shiboken6_binaries

hiddenimports = list(set(pyside6_hiddenimports + shiboken6_hiddenimports + [
    'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtNetwork',
    'openai', 'google.generativeai', 'httpx', 'anyio', 'idna', 'certifi',
    'sqlalchemy', 'aiosqlite',
]))

block_cipher = None

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

a = Analysis(
    ['po_app/main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookconfig={
        'collect_qt_plugins': 'platforms,styles,imageformats,tls',
    },
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='PromptOptimizer',
    icon='po_app/assets/icon.ico',
    console=False,  # windowed GUI app
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='PromptOptimizer',
)

