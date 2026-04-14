import sys
from pathlib import Path
from .utils.platform import Platform, platform

CONFIG_DIR_PATH = ""
DATA_DIR_PATH = ""

if platform == Platform.LINUX or platform == Platform.ANDROID:
    CONFIG_DIR_PATH = (
        Path.home() / ".local" / "share" / "den"
    )  # Both in the same place so source control becomes easy.
    DATA_DIR_PATH = Path.home() / ".local" / "share" / "den"
else:
    raise OSError(
        f"Current platform ({platform if platform else sys.platform}) is not supported."
    )
