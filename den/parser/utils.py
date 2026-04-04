import os
import json
from pathlib import Path
from den import paths


def get_project_path() -> Path:
    curr = Path.cwd()

    while curr != curr.parent:
        if (curr / ".git").exists():
            return curr
        curr = curr.parent

    return Path()


def create_projects_file() -> None:
    os.makedirs(paths.CONFIG_DIR_PATH, exist_ok=True)

    with open(paths.PROJECTS_FILE_PATH, "w") as f:
        json.dump([], f)


def get_project(project_path: Path) -> dict:
    try:
        with open(paths.PROJECTS_FILE_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return {}

            for proj in data:
                if proj.get("path") == str(project_path):
                    return proj

    except OSError as e:
        raise OSError(f"Unable to read {paths.PROJECTS_FILE_PATH}", e)

    return {}
