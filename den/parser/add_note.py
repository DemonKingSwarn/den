import os
import json
import uuid
import datetime
from pathlib import Path
from den import paths
from den.parser import utils


def _add_project(project_path: Path) -> dict:
    try:
        with open(paths.PROJECTS_FILE_PATH, "r+") as f:
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


def _create_notes_file(project_dir_path: str) -> Path:
    os.makedirs(project_dir_path, exist_ok=True)

    notes_path = os.path.join(project_dir_path, "notes.json")

    if not os.path.exists(notes_path):
        with open(notes_path, "w") as f:
            json.dump([], f)

    return Path(notes_path)


def _add_note_file(project_notes_file_path: Path, args) -> None:
    try:
        with open(project_notes_file_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            content = " ".join(args.note)

            note = {
                "created_at": str(datetime.datetime.now()),
                "id": str(uuid.uuid4()),
                "content": content,
            }

            data.append(note)

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    except OSError as e:
        print(f"Unable to write note: {e}")


def add_note(args) -> None:
    project_path = utils.get_project_path()

    if not str(project_path):
        print("Run inside a git project.")
        return

    if not os.path.exists(paths.PROJECTS_FILE_PATH):
        utils.create_projects_file()

    project = utils.get_project(project_path)

    if not project:
        project = _add_project(project_path)

    project_dir_id = project.get("dir_id")

    if not project_dir_id:
        print("Invalid project entry.")
        return

    project_dir_path = os.path.join(paths.DATA_DIR_PATH, project_dir_id)

    notes_path = _create_notes_file(project_dir_path)

    _add_note_file(notes_path, args)
