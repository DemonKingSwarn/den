import os
import tempfile
import subprocess
import argparse

from .. import colors
from ..parser import note, project
from ..parser.notes_helper import (
    load_notes,
    format_editor_content,
    parse_editor_content,
)


def execute(args: argparse.Namespace) -> None:
    """
    Edit a note by its display index using $EDITOR.
    """
    try:
        proj = project.get()
    except ValueError as e:
        print(e)
        return
    except OSError as e:
        print(f"Project error: {e}")
        return

    project_uid = proj.get("uid")

    if not project_uid:
        print("Invalid project entry.")
        return

    notes = load_notes(project_uid)

    if not notes:
        print("No notes to edit.")
        return

    display_id = args.id
    total = len(notes)
    idx = total - display_id

    if idx < 0 or idx >= total:
        print(f"Invalid note ID. Use a number between 1 and {total}.")
        return

    n = notes[idx]
    editor_text = format_editor_content(n)
    editor = os.environ.get("EDITOR", "nano")

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", prefix="den_edit_", delete=False
        ) as tmp:
            tmp.write(editor_text)
            tmp_path = tmp.name

        subprocess.run([editor, tmp_path], check=True)

        with open(tmp_path, "r") as f:
            raw = f.read()

    except subprocess.CalledProcessError:
        print("Editor exited with an error.")
        return
    except OSError as e:
        print(f"Unable to open editor: {e}")
        return
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    new_content = parse_editor_content(raw)

    if new_content == n.get("content", ""):
        print(colors.dim("No changes made."))
        return

    updated = note.edit(project_uid, display_id, new_content)

    if updated:
        print(
            f"{colors.green('Updated:')} {new_content[:50]}{'...' if len(new_content) > 50 else ''}"
        )
