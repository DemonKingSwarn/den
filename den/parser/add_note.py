import argparse
from den.parser.project import get as get_project
from den.parser.note import add as add_note


def execute(args: argparse.Namespace) -> None:
    """
    Add a note for the current project.
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
    add_note(project_uid, args)
