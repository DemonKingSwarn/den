import os
import sys
from pathlib import Path


def get_config_dir_path():
    if sys.platform == "linux" or sys.platform == "android":
        return os.path.join(str(Path.home()), ".config", "den")


def get_registry_path():
    if sys.platform == "linux" or sys.platform == "android":
        return os.path.join(str(Path.home()), ".config", "den", "registry.json")


def get_data_dir_path():
    if sys.platform == "linux" or sys.platform == "android":
        return os.path.join(str(Path.home()), ".local", "share", "den")
