"""
Shared utilities for loading and formatting notes.
"""

import os
import json
from pathlib import Path
from datetime import datetime

from .. import config
from ..utils import colors


def load_notes(project_uid: str) -> list:
    """
    Load notes from the notes file for a project.
    Returns a list of note dicts, or an empty list on failure.
    """
    notes_path = os.path.join(config.DATA_DIR_PATH, project_uid, "notes.json")

    try:
        with open(notes_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []
    except OSError:
        return []


def _format_timestamp(raw: str) -> str:
    """
    Format a raw timestamp into a short, readable format.
    """
    try:
        dt = datetime.fromisoformat(raw)
        return dt.strftime("%d %b, %H:%M")
    except (ValueError, TypeError):
        return raw or ""


def get_reference(note: dict) -> dict | None:
    """
    Get the reference from a note, supporting both new 'reference'
    and legacy 'context' keys.
    """
    return note.get("reference") or note.get("context")


def read_reference_code(ref: dict) -> str:
    """
    Read code from disk for a reference dict.
    Returns the code string or empty string on failure.
    """
    if not ref:
        return ""

    filepath = ref.get("filepath", "")
    start = ref.get("start_line", 1)
    end = ref.get("end_line", start)

    # If legacy note has inline code, use it
    if ref.get("code"):
        return ref["code"]

    try:
        p = Path(filepath).resolve()
        if not p.exists():
            return f"(File not found: {filepath})"
        with open(p, "r") as f:
            lines = f.readlines()
        return "".join(lines[max(0, start - 1) : end])
    except OSError:
        return f"(Unable to read: {filepath})"


def format_note_line(
    display_idx: int, note: dict, width: int = 80, ansi: bool = True
) -> str:
    """
    Format a single note as a compact one-line string.
    """
    content = note.get("content", "") or ""
    # Only show the first line in compact one-line summary
    if content:
        content = content.splitlines()[0]
    timestamp = _format_timestamp(note.get("created_at", ""))
    ref = get_reference(note)

    ref_tag = ""
    ref_visual_len = 0
    if ref:
        filepath = ref.get("filepath", "")
        basename = os.path.basename(filepath)
        ref_tag = f" 📎 {basename}"
        ref_visual_len = len(ref_tag) + 1  # emoji takes 2 columns

    idx_str = f"[{display_idx}]"

    # Calculate available space for content
    # Format: "  [N]  content  ref_tag  timestamp"
    fixed_width = len(idx_str) + ref_visual_len + len(timestamp) + 8  # padding
    content_width = max(10, width - fixed_width)

    # Truncate content if needed
    if len(content) > content_width:
        content = content[: content_width - 2] + ".."

    if ansi:
        line = (
            f"  {colors.dim(idx_str)}  "
            f"{content.ljust(content_width)}"
            f"{colors.yellow(ref_tag) if ref_tag else ''}"
            f"  {colors.dim(timestamp)}"
        )
    else:
        line = f"  {idx_str}  {content.ljust(content_width)}{ref_tag}  {timestamp}"

    return line


def format_note_context(note: dict, ansi: bool = True) -> str:
    """
    Format the context block for a note. Returns empty string if no reference.
    """
    ref = get_reference(note)
    if not ref:
        return ""

    filepath = ref.get("filepath", "")
    start = ref.get("start_line", "")
    end = ref.get("end_line", "")
    code = read_reference_code(ref)

    ref_title = f"[Ref:{filepath}:{start}-{end}]"
    lines = []

    if ansi:
        lines.append(
            f"      {colors.dim('┌─')}{colors.yellow(ref_title)}{colors.dim('─' * max(0, 40 - len(ref_title)))}"
        )
        if code:
            for line in code.splitlines():
                lines.append(f"      {colors.dim('│')} {colors.dim(line)}")
        lines.append(f"      {colors.dim('└' + '─' * 42)}")
    else:
        lines.append(f"      ┌─{ref_title}{'─' * max(0, 40 - len(ref_title))}")
        if code:
            for line in code.splitlines():
                lines.append(f"      │ {line}")
        lines.append(f"      └{'─' * 42}")

    return "\n".join(lines)


def format_editor_content(note: dict) -> str:
    """
    Format a note for editing in $EDITOR.
    Only the content is editable. Reference is read-only.
    """
    return note.get("content", "") or ""


def parse_editor_content(text: str) -> str:
    """
    Parse editor output back into content string.
    """
    return text.strip()
