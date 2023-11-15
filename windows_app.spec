# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
block_cipher = None
 
a = Analysis(['src\\chainreport_converter_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32timezone'],
    hookspath=hookspath(),
    hooksconfig={},
    runtime_hooks=untime_hooks(),
    excludes=[],
    noarchive=False,
    **get_deps_minimal(video=None, audio=None)
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
