import subprocess
import sys
import importlib

REQUIRED_LIBRARIES = [
    "librosa",
    "soundfile",
    "numpy",
    "yt-dlp",
    "audioread"
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for lib in REQUIRED_LIBRARIES:
    try:
        importlib.import_module(lib.replace("-", "_"))  # yt-dlp -> yt_dlp
    except ImportError:
        print(f"📦 Устанавливаем {lib}...")
        install(lib)