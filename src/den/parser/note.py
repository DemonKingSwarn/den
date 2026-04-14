import os
import json
import uuid
import datetime
import argparse
from pathlib import Path
from typing import Optional

from ..paths import DATA_DIR_PATH


def _create_notes_file(project_uid: str) -> Path:
    """
    Create the notes file if not exists.
    """
    # Create the notes directory if not exists.
    note_dir = os.path.join(DATA_DIR_PATH, project_uid)
    os.makedirs(note_dir, exist_ok=True)

    # Create the notes file if not exists.
    notes_path = os.path.join(note_dir, "notes.json")

    if not os.path.exists(notes_path):
        with open(notes_path, "w") as f:
            json.dump([], f, indent=4)

    return Path(notes_path)


def add(project_uid: str, args: argparse.Namespace) -> None:
    """
    Add a note to the notes file.
    """
    if not project_uid:
        raise ValueError("Invalid project entry.")

    notes_path = _create_notes_file(project_uid)

    try:
        with open(notes_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            content = " ".join(args.note).strip()

            if not content:
                print("Empty note, skipped.")
                return

            reference = None
            if hasattr(args, "ref") and args.ref:
                try:
                    filepath, lines = args.ref.split(":", 1)
                    start_str, end_str = lines.split(",", 1)
                    start_line = int(start_str)
                    end_line = int(end_str)

                    abs_filepath = Path(filepath).resolve()
                    if abs_filepath.exists():
                        reference = {
                            "filepath": str(filepath),
                            "start_line": start_line,
                            "end_line": end_line,
                        }
                    else:
                        print(
                            f"Warning: Reference file '{abs_filepath}' does not exist."
                        )
                except Exception as e:
                    print(f"Warning: Failed to parse ref ({e})")

            note = {
                "created_at": str(datetime.datetime.now()),
                "id": str(uuid.uuid4()),
                "content": content,
            }
            if reference:
                note["reference"] = reference

            data.append(note)

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    except OSError as e:
        print(f"Unable to write note: {e}")


def _get_notes_path(project_uid: str) -> Path:
    """
    Get the notes file path for a project.
    """
    return Path(os.path.join(DATA_DIR_PATH, project_uid, "notes.json"))


def _display_index_to_list_index(display_id: int, total: int) -> int:
    """
    Convert a display index (newest=1) to a list index (oldest=0).
    """
    return total - display_id


def remove(project_uid: str, display_id: int) -> Optional[dict]:
    """
    Remove a note by its display index.
    Returns the removed note dict, or None on failure.
    """
    if not project_uid:
        print("Invalid project entry.")
        return None

    notes_path = _get_notes_path(project_uid)

    try:
        with open(notes_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Corrupted notes file.")
                return None

            if not data:
                print("No notes to remove.")
                return None

            idx = _display_index_to_list_index(display_id, len(data))

            if idx < 0 or idx >= len(data):
                print(f"Invalid note ID. Use a number between 1 and {len(data)}.")
                return None

            removed = data.pop(idx)

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            return removed

    except FileNotFoundError:
        print("No notes found.")
        return None
    except OSError as e:
        print(f"Unable to remove note: {e}")
        return None


def edit(project_uid: str, display_id: int, new_content: str) -> Optional[dict]:
    """
    Edit a note's content by its display index.
    Returns the updated note dict, or None on failure.
    """
    if not project_uid:
        print("Invalid project entry.")
        return None

    notes_path = _get_notes_path(project_uid)

    try:
        with open(notes_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Corrupted notes file.")
                return None

            if not data:
                print("No notes to edit.")
                return None

            idx = _display_index_to_list_index(display_id, len(data))

            if idx < 0 or idx >= len(data):
                print(f"Invalid note ID. Use a number between 1 and {len(data)}.")
                return None

            data[idx]["content"] = new_content

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            return data[idx]

    except FileNotFoundError:
        print("No notes found.")
        return None
    except OSError as e:
        print(f"Unable to edit note: {e}")
        return None
