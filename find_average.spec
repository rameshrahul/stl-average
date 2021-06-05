# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['find_average.py'],
             pathex=['C:\\Users\\rr600\\Documents\\Projects\\stl_average_project\\stl-average', 'C:\\Users\\rr600\\anaconda3\\Lib\\site-packages'],
             binaries=[],
             datas=[],
             hiddenimports=['cython','sklearn','sklearn.neighbors._typedefs', 'sklearn.utils._weight_vector', 'mesh_to_sdf'],
             hookspath=['C:\\Users\\rr600\\Documents\\Projects\\stl_average_project\\stl-average\\hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='find_average',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='find_average')
