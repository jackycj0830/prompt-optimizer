# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('po_app/assets', 'assets'), ('D:\\JackyZou_WorkSpace\\projects\\AI\\AugmentCode_AI\\prompt-optimizer\\.venv\\Lib\\site-packages\\PySide6\\plugins\\platforms', 'PySide6/plugins/platforms'), ('D:\\JackyZou_WorkSpace\\projects\\AI\\AugmentCode_AI\\prompt-optimizer\\.venv\\Lib\\site-packages\\PySide6\\plugins\\styles', 'PySide6/plugins/styles'), ('D:\\JackyZou_WorkSpace\\projects\\AI\\AugmentCode_AI\\prompt-optimizer\\.venv\\Lib\\site-packages\\PySide6\\plugins\\imageformats', 'PySide6/plugins/imageformats'), ('D:\\JackyZou_WorkSpace\\projects\\AI\\AugmentCode_AI\\prompt-optimizer\\.venv\\Lib\\site-packages\\PySide6\\plugins\\iconengines', 'PySide6/plugins/iconengines'), ('D:\\JackyZou_WorkSpace\\projects\\AI\\AugmentCode_AI\\prompt-optimizer\\.venv\\Lib\\site-packages\\PySide6\\plugins\\tls', 'PySide6/plugins/tls')]
binaries = []
hiddenimports = []
datas += collect_data_files('PySide6')
datas += collect_data_files('shiboken6')
binaries += collect_dynamic_libs('PySide6')
hiddenimports += collect_submodules('PySide6')
tmp_ret = collect_all('PySide6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['po_app\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'pytest_cov', 'pytest_qt', 'black', 'flake8'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PromptOptimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['po_app\\assets\\icon.ico'],
)
