import os
import json
import uuid
from pathlib import Path

from .. import paths


def _get_path() -> Path:
    """
    Get the project path.
    """
    curr = Path.cwd()

    while curr != curr.parent:
        if (curr / ".git").exists():
            return curr
        curr = curr.parent

    return Path()


def _create_projects_file() -> None:
    """
    Create the projects.json file.
    """
    # Create config dir if not exists.
    os.makedirs(paths.CONFIG_DIR_PATH, exist_ok=True)

    # Create and initialize projects file.
    try:
        with open(os.path.join(paths.CONFIG_DIR_PATH, "projects.json"), "w") as f:
            json.dump([], f)
    except OSError as e:
        raise OSError("Unable to create projects file", e)


def add(project_path: Path) -> dict:
    """
    Add the project to the projects file.
    """
    projects_file = os.path.join(paths.CONFIG_DIR_PATH, "projects.json")

    try:
        with open(projects_file, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            for proj in data:
                if proj.get("path") == str(project_path):
                    return proj

            new_project = {
                "path": str(project_path),
                "uid": str(uuid.uuid4()),
            }

            data.append(new_project)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            return new_project

    except FileNotFoundError:
        _create_projects_file()

        new_project = {
            "path": str(project_path),
            "uid": str(uuid.uuid4()),
        }

        try:
            with open(projects_file, "w") as f:
                json.dump([new_project], f, indent=4)
            return new_project
        except OSError as e:
            print(f"Unable to add project after creation: {e}")
            return None

    except OSError as e:
        print(f"Unable to add project: {e}")
        return None


def get() -> dict:
    """
    Get the project from the projects file.
    """
    project_path = _get_path()

    if not project_path.name and not project_path.parts:
        raise ValueError("Run inside a git project.")

    if not os.path.exists(os.path.join(paths.CONFIG_DIR_PATH, "projects.json")):
        _create_projects_file()

    try:
        with open(os.path.join(paths.CONFIG_DIR_PATH, "projects.json"), "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            for p in data:
                if p.get("path") == str(project_path):
                    return p

    except OSError as e:
        raise OSError(
            f"Unable to read {os.path.join(paths.CONFIG_DIR_PATH, 'projects.json')}", e
        )

    return add(project_path)
