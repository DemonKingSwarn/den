"""
Commands:
    den
    den ls
    den add ...
    den edit <id>
    den rm <id>
"""

import argparse

from den.parser import den
from den.parser import list_notes
from den.parser import add_note
from den.parser import edit_note
from den.parser import add_note

_parser = argparse.ArgumentParser(
    prog="den",
    description="Braindumping for projects made easy.",
)
_parser.set_defaults(func=den)

_subparsers = _parser.add_subparsers()

_parser_ls = _subparsers.add_parser(name="ls")
_parser_ls.set_defaults(func=list_notes.list_notes)
_parser_add = _subparsers.add_parser(name="add")
_parser_add.set_defaults(func=add_note.add_note)
_parser_add.add_argument("note", nargs="*")
_parser_edit = _subparsers.add_parser(name="edit")
_parser_edit.add_argument("id", type=int)
_parser_rm = _subparsers.add_parser(name="rm")
_parser_rm.add_argument("id", type=int)


def execute() -> None:
    args: argparse.Namespace = _parser.parse_args()
    args.func(args)
