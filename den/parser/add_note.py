import os
import argparse

from den import paths
from den.parser.project import (
    get_project_path,
    create_projects_file,
    get_project,
    add_project,
)
from den.parser.note import (
    create_notes_file,
    add_note_in_notes_file,
)


def add_note(args: argparse.Namespace) -> None:
    project_path = get_project_path()

    if not str(project_path):
        print("Run inside a git project.")
        return

    if not os.path.exists(os.path.join(paths.CONFIG_DIR_PATH, "projects.json")):
        create_projects_file()

    project = get_project(project_path)

    if not project:
        project = add_project(project_path)

    project_dir_id = project.get("dir_id")

    if not project_dir_id:
        print("Invalid project entry.")
        return

    project_dir_path = os.path.join(paths.DATA_DIR_PATH, project_dir_id)

    notes_path = create_notes_file(project_dir_path)

    add_note_in_notes_file(notes_path, args)
