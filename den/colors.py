"""
ANSI color helpers for terminal output.
"""

import re

import sys

_ANSI_PATTERN = re.compile(r"\033\[[0-9;]*m")

# Disable colors if not a TTY (piping to less, etc)
_ENABLED = sys.stdout.isatty()

RESET = "\033[0m" if _ENABLED else ""
BOLD = "\033[1m" if _ENABLED else ""
DIM = "\033[2m" if _ENABLED else ""

RED = "\033[31m" if _ENABLED else ""
GREEN = "\033[32m" if _ENABLED else ""
YELLOW = "\033[33m" if _ENABLED else ""
CYAN = "\033[36m" if _ENABLED else ""


def bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"


def dim(text: str) -> str:
    return f"{DIM}{text}{RESET}"


def red(text: str) -> str:
    return f"{RED}{text}{RESET}"


def green(text: str) -> str:
    return f"{GREEN}{text}{RESET}"


def yellow(text: str) -> str:
    return f"{YELLOW}{text}{RESET}"


def cyan(text: str) -> str:
    return f"{CYAN}{text}{RESET}"


def strip_ansi(text: str) -> str:
    return _ANSI_PATTERN.sub("", text)
