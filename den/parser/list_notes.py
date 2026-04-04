import os
import json
from den import paths
from den.parser import utils


def list_notes(args) -> None:
    """
    List all notes for the current project.
    """
    project_path = utils.get_project_path()

    if not str(project_path):
        print("Run inside a git project.")
        return

    if not os.path.exists(paths.PROJECTS_FILE_PATH):
        print("No projects found.")
        return

    project = utils.get_project(project_path)

    if not project:
        print("Project not registered.")
        return

    project_dir_id = project.get("dir_id")

    if not project_dir_id:
        print("Invalid project entry.")
        return

    project_dir_path = os.path.join(paths.DATA_DIR_PATH, project_dir_id)
    notes_path = os.path.join(project_dir_path, "notes.json")

    if not os.path.exists(notes_path):
        print("No notes found.")
        return

    try:
        with open(notes_path, "r") as f:
            try:
                notes = json.load(f)
            except json.JSONDecodeError:
                print("Corrupted notes file.")
                return

        if not notes:
            print("No notes yet.")
            return

        # Optional: reverse order (latest first)
        notes = list(reversed(notes))

        for i, note in enumerate(notes, start=1):
            print(f"[{i}] {note.get('created_at')}")
            print(f"    {note.get('content')}")
            print()

    except OSError as e:
        print(f"Unable to read notes: {e}")
