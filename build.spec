# -*- mode: python -*-
block_cipher = None

a = Analysis(['po_app/main.py'],
             pathex=[],
             binaries=[],
             datas=[('po_app/assets', 'assets')],
             hiddenimports=['PySide6'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['pytest', 'pytest_cov', 'pytest_qt', 'black', 'flake8'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          name='PromptOptimizer',
          icon='po_app/assets/icon.ico',
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)

