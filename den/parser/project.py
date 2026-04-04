import os
import json
import uuid
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

    with open(os.path.join(paths.CONFIG_DIR_PATH, "projects.json"), "w") as f:
        json.dump([], f)


def get_project(project_path: Path) -> dict:
    try:
        with open(os.path.join(paths.CONFIG_DIR_PATH, "projects.json"), "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return {}

            for proj in data:
                if proj.get("path") == str(project_path):
                    return proj

    except OSError as e:
        raise OSError(
            f"Unable to read {os.path.join(paths.CONFIG_DIR_PATH, 'projects.json')}", e
        )

    return {}


def add_project(project_path: Path) -> dict:
    try:
        with open(os.path.join(paths.CONFIG_DIR_PATH, "projects.json"), "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            for proj in data:
                if proj.get("path") == str(project_path):
                    return proj

            new_project = {
                "path": str(project_path),
                "dir_id": str(uuid.uuid4()),
            }

            data.append(new_project)

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            return new_project

    except OSError as e:
        raise OSError("Unable to add project", e)
