import argparse
import shutil
from ..utils import colors
from ..parser.project import get as get_project
from ..parser.notes_helper import load_notes, format_note_line, format_note_context


def execute(_args: argparse.Namespace) -> None:
    """
    List all notes for the current project.
    """
    try:
        project = get_project()
    except ValueError as e:
        print(e)
        return
    except OSError as e:
        print(f"Project error: {e}")
        return

    project_uid = project.get("uid")

    if not project_uid:
        print("Invalid project entry.")
        return

    notes = load_notes(project_uid)

    if not notes:
        print(colors.dim("  No notes yet."))
        return

    term_width = shutil.get_terminal_size((80, 24)).columns
    len_notes = len(notes)

    print()
    print(
        f"  {colors.bold('den')} {colors.dim(f'· {len_notes} note{"s" if len_notes != 1 else ""}')}"
    )
    print()

    for i, note in enumerate(notes):
        display_id = len_notes - i
        print(format_note_line(display_id, note, width=term_width))
        ctx = format_note_context(note)
        if ctx:
            print(ctx)

    print()
