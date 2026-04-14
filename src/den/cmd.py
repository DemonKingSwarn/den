"""
Commands:
    den             - Open an interactive session.
    den ls          - List all notes.
    den add <note>  - Add a new note (No need to add quotes).
    den edit [id]   - Edit a note (default: most recent).
    den rm [id]     - Remove a note (default: most recent).
"""

import argparse

from .parser import den, list_notes, add_note, edit_note, remove_note

_parser = argparse.ArgumentParser(
    prog="den",
    description="Braindumping for projects made easy.",
)

_parser.set_defaults(func=den.execute)

_subparsers = _parser.add_subparsers()

_parser_ls = _subparsers.add_parser(name="ls")
_parser_ls.set_defaults(func=list_notes.execute)
_parser_add = _subparsers.add_parser(name="add")
_parser_add.add_argument("--ref", type=str)
_parser_add.set_defaults(func=add_note.execute)
_parser_add.add_argument("note", nargs="*")
_parser_edit = _subparsers.add_parser(name="edit")
_parser_edit.set_defaults(func=edit_note.execute)
_parser_edit.add_argument("id", type=int, nargs="?", default=1)
_parser_rm = _subparsers.add_parser(name="rm")
_parser_rm.set_defaults(func=remove_note.execute)
_parser_rm.add_argument("id", type=int, nargs="?", default=1)


def execute() -> None:
    args: argparse.Namespace = _parser.parse_args()
    args.func(args)
