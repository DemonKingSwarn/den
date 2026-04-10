import sys
from pathlib import Path
from den.platform import Platform, platform

CONFIG_DIR_PATH = ""
DATA_DIR_PATH = ""

if platform == Platform.LINUX or platform == Platform.ANDROID:
    CONFIG_DIR_PATH = Path.home() / ".config" / "den"
    DATA_DIR_PATH = Path.home() / ".local" / "share" / "den"
else:
    raise OSError(
        f"Current platform ({platform if platform else sys.platform}) is not supported."
    )
