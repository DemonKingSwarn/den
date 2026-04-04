import os
import json
import uuid
import datetime
import argparse
from pathlib import Path


def create_notes_file(project_dir_path: str) -> Path:
    os.makedirs(project_dir_path, exist_ok=True)

    notes_path = os.path.join(project_dir_path, "notes.json")

    if not os.path.exists(notes_path):
        with open(notes_path, "w") as f:
            json.dump([], f)

    return Path(notes_path)


def add_note_in_notes_file(
    project_notes_file_path: Path, args: argparse.Namespace
) -> None:
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
