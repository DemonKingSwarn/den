import os
import json
import uuid
import datetime
from pathlib import Path
from .utils import paths


def p_den(args) -> None:
    print(args)


def p_list(args) -> None:
    print("list")


def p_add(args) -> None:
    """
    Add a note.
    """

    # Find the project path.
    curr_dir_path = Path.cwd()
    project_path = ""
    found_project_path = False

    while not found_project_path:
        if str(curr_dir_path) == str(Path.cwd().root):
            break
        for name in os.listdir(curr_dir_path):
            if name == ".git":
                project_path = curr_dir_path
                found_project_path = True
        curr_dir_path = curr_dir_path.parent

    if project_path == "":
        print('Please run "den add ..." inside a git project.')
        return

    # If the project path is not in the registry, add it
    if not os.path.exists(paths.get_config_dir_path()):
        try:
            os.makedirs(paths.get_config_dir_path())
        except OSError as e:
            print(f"Unable to create {paths.get_config_dir_path()}. ", e)
            return

    if not os.path.exists(paths.get_registry_path()):
        try:
            with open(paths.get_registry_path(), "w") as registry_file:
                json.dump([], registry_file)
        except OSError as e:
            print(f"Unable to create {paths.get_registry_path()}", e)
            return

    try:
        with open(paths.get_registry_path(), "r+") as registry_file:
            registry_file_data: list[dict] = []

            try:
                registry_file_data = json.load(registry_file)
            except json.JSONDecodeError as e:
                print(f"Unable to decode {paths.get_registry_path()}", e)
                return

            found_project_path = False
            for registry in registry_file_data:
                if "project_path" in registry:
                    if registry.get("project_path") == str(project_path):
                        found_project_path = True
                        break

            registry_file.seek(0)

            if not found_project_path:
                registry_file_data.append(
                    {"project_path": str(project_path), "project_id": str(uuid.uuid4())}
                )
                json.dump(registry_file_data, registry_file, indent=4)

    except OSError as e:
        print(f"Unable to operate on {paths.get_registry_path()}", e)
        return

    # Finally, add the note in notes.json
    project_id = ""

    try:
        with open(paths.get_registry_path(), "r+") as registry_file:
            registry_file_data: list[dict] = []

            try:
                registry_file_data = json.load(registry_file)
            except json.JSONDecodeError as e:
                print(f"Unable to decode {paths.get_registry_path()}", e)
                return

            for registry in registry_file_data:
                if "project_path" in registry:
                    if registry.get("project_path") == str(project_path):
                        project_id = registry.get("project_id")
                        break

    except OSError as e:
        print(f"Unable to operate on {paths.get_registry_path()}", e)
        return

    project_data_dir_path = os.path.join(
        paths.get_data_dir_path(), project_id if project_id is not None else ""
    )

    if not os.path.exists(project_data_dir_path):
        try:
            os.makedirs(project_data_dir_path)
        except OSError as e:
            print(f"Unable to create {project_data_dir_path}. ", e)
            return

    project_notes_path = os.path.join(project_data_dir_path, "notes.json")

    if not os.path.exists(project_notes_path):
        try:
            with open(project_notes_path, "w") as note_file:
                json.dump([], note_file)
        except OSError as e:
            print(f"Unable to create {project_notes_path}", e)
            return

    try:
        with open(project_notes_path, "r+") as note_file:
            note_file_data: list[dict] = []

            try:
                note_file_data = json.load(note_file)
            except json.JSONDecodeError as e:
                print(f"Unable to decode {project_notes_path}", e)
                return

            note_file.seek(0)

            note = ""

            for word in args.note:
                note += word + " "

            note_file_data.append(
                {
                    "created_at": str(datetime.datetime.now()),
                    "note_id": str(uuid.uuid4()),
                    "note": note,
                }
            )

            json.dump(
                note_file_data,
                note_file,
                indent=4,
            )

    except OSError as e:
        print(f"Unable to create {project_notes_path}. ", e)
        return


def p_edit(args) -> None:
    print("edit")


def p_remove(args) -> None:
    print("remove")
