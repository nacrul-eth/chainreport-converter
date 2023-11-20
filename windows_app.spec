# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
block_cipher = None
 
a = Analysis(['src\\chainreport_converter_app.py'],
    pathex=[],
    datas=[],
    hiddenimports=['win32timezone'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    noarchive=False,
)
 
pyz = PYZ(a.pure, a.zipped_data,
        cipher=block_cipher)

exe = EXE(pyz, Tree('src'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          debug=False,
          strip=False,
          upx=True,
          icon=['src\\assets\\app-logo.ico'],
          name='chain.report converter')
