# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, hookspath, runtime_hooks
block_cipher = None
 
a = Analysis(['src\\chainreport_converter_app.py'],
    pathex=[],
    datas=[],
    hookspath=hookspath(),
    hooksconfig={},
    runtime_hooks=runtime_hooks(),
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
          debug=False,
          strip=False,
          upx=True,
          name='chain.report converter')
