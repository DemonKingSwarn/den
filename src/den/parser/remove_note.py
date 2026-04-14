import argparse

from ..parser import note, project
from .. import colors


def execute(args: argparse.Namespace) -> None:
    """
    Remove a note by its display index.
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

    removed = note.remove(project_uid, args.id)

    if removed:
        content = removed.get("content", "")
        preview = content[:50] + "..." if len(content) > 50 else content
        print(f"{colors.red('Removed:')} {preview}")
