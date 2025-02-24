# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\DELL\\PycharmProjects\\PythonProject\\projectpython'],
    binaries=[],
    datas=[
        ('interface.py', '.'),
        ('database.py', '.'),
        ('candidat.py', '.'),
        ('jury.py', '.'),
        ('deliberation.py', '.'),
        ('statistiques.py', '.'),
        ('releve_notes.py', '.'),
        ('repechage.py', '.'),
        ('pdf_generator.py', '.'),
        ('anonymat.py', '.'),
        ('gestionsecondtour.py', '.'),
    ],
    hiddenimports=[
        'sqlite3',
        'tkinter',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='GestionBfem',  # Changez le nom de l'exécutable si nécessaire
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Activez la console pour le débogage
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
