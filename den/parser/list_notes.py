import os
import json
import argparse
from den import paths
from den.parser.project import get_project_path, get_project


def list_notes(_args: argparse.Namespace) -> None:
    """
    List all notes for the current project.
    """
    project_path = get_project_path()

    if not str(project_path):
        print("Run inside a git project.")
        return

    if not os.path.exists(os.path.join(paths.CONFIG_DIR_PATH, "projects.json")):
        print("No projects found.")
        return

    project = get_project(project_path)

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

        notes = list(notes)
        len_notes = len(notes)

        for i, note in enumerate(notes, start=1):
            print(f"[{len_notes - i + 1}] {note.get('created_at')}")
            print(f"    {note.get('content')}")
            print()

    except OSError as e:
        print(f"Unable to read notes: {e}")
