import sys
from enum import Enum, auto
from typing import Optional


class Platform(Enum):
    LINUX = auto()
    ANDROID = auto()
    DARWIN = auto()
    WIN32 = auto()


platform: Optional[Platform] = None

if sys.platform == "linux":
    platform = Platform.LINUX
elif sys.platform == "android":
    platform = Platform.ANDROID
elif sys.platform == "darwin":
    platform = Platform.DARWIN
elif sys.platform == "win32":
    platform = Platform.WIN32
