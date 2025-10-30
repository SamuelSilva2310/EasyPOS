# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from pathlib import Path

# --- Project paths ---
base_path = Path(__name__).parent
src_path = base_path / "src" / "easypos"

# --- Include escpos data ---
escpos_datas = collect_data_files("escpos")

# --- Include app static data ---
app_datas = [
    ("images", "images"),
    ("db", "db"),
    ("easypos_config.json", "."),
]

datas = escpos_datas + app_datas

# --- Analysis ---
a = Analysis(
    [str(src_path / "main.py")],
    pathex=[str(src_path)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# --- Python archive ---
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# --- Executable (Windows GUI) ---
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="EasyPOS",
    debug=False,
    strip=False,
    upx=True,
    console=False,  # No terminal for GUI
    icon=str(base_path / "images" / "logo.ico"),  # Windows icon
)

# --- Collect everything ---
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EasyPOS",
)