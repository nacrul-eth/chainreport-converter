# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
block_cipher = None
 
a = Analysis(['src\\chainreport_converter_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32timezone'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
          debug=True,
          strip=False,
          upx=True,
          name='chain.report converter')
 
coll = COLLECT(exe, Tree('src'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='chain.report converter')
