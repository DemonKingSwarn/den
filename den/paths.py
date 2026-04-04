import os
import sys
from pathlib import Path

CONFIG_DIR_PATH = ""
PROJECTS_FILE_PATH = ""
DATA_DIR_PATH = ""

if sys.platform == "linux" or sys.platform == "android":
    CONFIG_DIR_PATH = os.path.join(str(Path.home()), ".config", "den")
    PROJECTS_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "projects.json")
    DATA_DIR_PATH = os.path.join(str(Path.home()), ".local", "share", "den")
else:
    raise OSError(f"'{sys.platform}' is not supported.")
