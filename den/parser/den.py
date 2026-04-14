"""
Interactive TUI for den using curses.
Supports normal and vim keybinding modes.
"""

import os
import sys
import curses
import tempfile
import argparse
import subprocess

from ..parser import note, project
from ..parser.notes_helper import (
    load_notes,
    get_reference,
    read_reference_code,
    _format_timestamp,
    format_editor_content,
    parse_editor_content,
)


# --- Modes ---
MODE_OPERATE = "OPERATE"
MODE_SEARCH = "SEARCH"
MODE_VIEW = "VIEW"


class TUI:
    def __init__(self, project_uid: str):
        self.project_uid = project_uid
        self.mode = MODE_OPERATE
        self.cursor = 0
        self.scroll_offset = 0
        self.search_query = ""
        self.notes: list = []
        self.filtered_indices: list = []
        self.status_msg = ""
        self.ref_scroll_offset = 0
        self._reload_notes()

    def _reload_notes(self):
        raw = load_notes(self.project_uid)
        # Reverse so newest is first
        self.notes = list(reversed(raw))
        self.filtered_indices = list(range(len(self.notes)))
        # Clamp cursor
        if self.cursor >= len(self.filtered_indices):
            self.cursor = max(0, len(self.filtered_indices) - 1)

    def _visible_notes(self) -> list:
        """Returns list of (original_index, note) tuples for current view."""
        return [(i, self.notes[i]) for i in self.filtered_indices]

    def run(self, stdscr):
        curses.set_escdelay(25)
        curses.curs_set(0)
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_GREEN, -1)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

        stdscr.timeout(50)

        while True:
            self._draw(stdscr)
            key = stdscr.getch()
            if key == -1:
                continue
            action = self._handle_input(key)
            if action == "QUIT":
                break

    # ─────────────────────────────────────────
    #  DRAW
    # ─────────────────────────────────────────
    def _draw(self, stdscr):
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        if self.mode == MODE_VIEW:
            self._draw_view(stdscr, h, w)
        else:
            self._draw_list(stdscr, h, w)

        stdscr.refresh()

    def _draw_list(self, stdscr, h, w):
        visible = self._visible_notes()
        total_notes = len(self.notes)

        # --- Header ---
        header = f"  den · {total_notes} note{'s' if total_notes != 1 else ''}"
        mode_label = f"[{self.mode}]"
        header_line = header.ljust(w - len(mode_label) - 1) + mode_label

        try:
            stdscr.addnstr(
                0, 0, header_line, w - 1, curses.A_BOLD | curses.color_pair(1)
            )
            stdscr.addnstr(1, 0, "─" * (w - 1), w - 1, curses.A_DIM)
        except curses.error:
            pass

        # --- Context preview panel ---
        sel = self._get_selected()
        ref = get_reference(sel[2]) if sel else None

        ctx_lines_count = 0
        ctx_display_lines = []
        if ref:
            filepath = ref.get("filepath", "")
            start = ref.get("start_line", "")
            end = ref.get("end_line", "")
            code = read_reference_code(ref)
            ref_label = f"{filepath}:{start}-{end}"
            ctx_display_lines.append((f"  {ref_label}", curses.color_pair(2)))
            if code:
                code_lines = code.splitlines()
                max_ctx = 6
                for cl in code_lines[:max_ctx]:
                    ctx_display_lines.append((f"    {cl}", curses.A_DIM))
                if len(code_lines) > max_ctx:
                    ctx_display_lines.append(
                        (
                            f"    ... {len(code_lines) - max_ctx} more lines",
                            curses.A_DIM,
                        )
                    )
            ctx_lines_count = len(ctx_display_lines) + 1

        list_height = h - 4 - ctx_lines_count
        if list_height < 1:
            list_height = 1

        # Scrolling
        if self.cursor < self.scroll_offset:
            self.scroll_offset = self.cursor
        if self.cursor >= self.scroll_offset + list_height:
            self.scroll_offset = self.cursor - list_height + 1

        if not visible and self.search_query:
            try:
                stdscr.addnstr(2, 0, "  No matches found.", w - 1, curses.A_DIM)
            except curses.error:
                pass
        else:
            for row_idx in range(list_height):
                note_idx = self.scroll_offset + row_idx
                if note_idx >= len(visible):
                    break

                orig_idx, n = visible[note_idx]
                display_id = orig_idx + 1
                content = n.get("content", "") or ""
                if content:
                    content = content.splitlines()[0]
                timestamp = _format_timestamp(n.get("created_at", ""))
                note_ref = get_reference(n)

                ref_tag = ""
                if note_ref:
                    basename = os.path.basename(note_ref.get("filepath", ""))
                    ref_tag = f" 📎 {basename}"

                idx_str = f"[{display_id}]"
                # Emoji 📎 takes 2 columns, len() is 1. Add 1 for extra column.
                ref_visual_len = len(ref_tag) + (1 if ref_tag else 0)
                ts_len = len(timestamp) + ref_visual_len + 4
                content_width = max(5, w - len(idx_str) - ts_len - 6)

                if len(content) > content_width:
                    content = content[: content_width - 2] + ".."

                is_selected = note_idx == self.cursor
                cursor_char = ">" if is_selected else " "

                line = f" {cursor_char} {idx_str}  {content.ljust(content_width)}{ref_tag}  {timestamp}"

                y = row_idx + 2
                try:
                    if is_selected:
                        stdscr.addnstr(
                            y, 0, line.ljust(w - 1), w - 1, curses.color_pair(5)
                        )
                    else:
                        stdscr.addnstr(y, 0, " " * (w - 1), w - 1)
                        x = 0
                        prefix = f" {cursor_char} {idx_str}  "
                        stdscr.addnstr(y, x, prefix, w - 1, curses.A_DIM)
                        x += len(prefix)
                        stdscr.addnstr(y, x, content.ljust(content_width), w - 1 - x)
                        x += content_width
                        if ref_tag:
                            stdscr.addnstr(
                                y, x, ref_tag, w - 1 - x, curses.color_pair(2)
                            )
                            x += ref_visual_len
                        stdscr.addnstr(y, x, f"  {timestamp}", w - 1 - x, curses.A_DIM)
                except curses.error:
                    pass

        # --- Context panel ---
        if ctx_display_lines:
            ctx_start_y = 2 + list_height
            try:
                stdscr.addnstr(ctx_start_y, 0, "─" * (w - 1), w - 1, curses.A_DIM)
                for ci, item in enumerate(ctx_display_lines):
                    line_text, attr = item
                    y = ctx_start_y + 1 + ci
                    if y >= h - 2:
                        break
                    stdscr.addnstr(y, 0, line_text[: w - 1], w - 1, attr)
            except curses.error:
                pass

        # --- Separator + Footer ---
        try:
            stdscr.addnstr(h - 2, 0, "─" * (w - 1), w - 1, curses.A_DIM)
        except curses.error:
            pass

        footer_y = h - 1
        try:
            if self.mode == MODE_SEARCH:
                search_line = f"  /: {self.search_query}█"
                stdscr.addnstr(footer_y, 0, search_line, w - 1, curses.color_pair(1))
            elif self.status_msg:
                stdscr.addnstr(
                    footer_y, 0, f"  {self.status_msg}", w - 1, curses.color_pair(4)
                )
                self.status_msg = ""
            elif self.search_query:
                search_line = f"  /: {self.search_query} "
                stdscr.addnstr(footer_y, 0, search_line, w - 1, curses.color_pair(1))
                hints = " (esc:clear)"
                stdscr.addnstr(
                    footer_y,
                    len(search_line),
                    hints,
                    w - 1 - len(search_line),
                    curses.A_DIM,
                )
            elif self.mode == MODE_VIEW:
                hints = "  j/k:move  q/esc:back"
                stdscr.addnstr(footer_y, 0, hints, w - 1, curses.A_DIM)
            else:
                hints = "  j/k:move  /:search  enter:view  e:edit  d:del  q/esc:quit"
                stdscr.addnstr(footer_y, 0, hints, w - 1, curses.A_DIM)
        except curses.error:
            pass

    def _draw_view(self, stdscr, h, w):
        sel = self._get_selected()
        if not sel:
            self.mode = MODE_OPERATE
            return

        _, display_id, n = sel
        content = n.get("content", "") or ""
        ref = get_reference(n)

        # --- Header ---
        header = f"  den · note [{display_id}]"
        mode_label = "[VIEW]"
        header_line = header.ljust(w - len(mode_label) - 1) + mode_label

        try:
            stdscr.addnstr(
                0, 0, header_line, w - 1, curses.A_BOLD | curses.color_pair(1)
            )
            stdscr.addnstr(1, 0, "─" * (w - 1), w - 1, curses.A_DIM)
        except curses.error:
            pass

        # --- Content (sticky, top) ---
        content_lines = content.splitlines() if content else ["(empty note)"]
        max_content_lines = min(len(content_lines), max(3, h // 3))
        for i, cl in enumerate(content_lines[:max_content_lines]):
            try:
                stdscr.addnstr(2 + i, 0, f"  {cl}"[: w - 1], w - 1)
            except curses.error:
                pass
        if len(content_lines) > max_content_lines:
            try:
                stdscr.addnstr(
                    2 + max_content_lines,
                    0,
                    f"  ... {len(content_lines) - max_content_lines} more lines",
                    w - 1,
                    curses.A_DIM,
                )
                max_content_lines += 1
            except curses.error:
                pass

        # --- Reference separator ---
        ref_start_y = 2 + max_content_lines + 1
        try:
            stdscr.addnstr(ref_start_y - 1, 0, "─" * (w - 1), w - 1, curses.A_DIM)
        except curses.error:
            pass

        if not ref:
            try:
                stdscr.addnstr(ref_start_y, 0, "  No reference.", w - 1, curses.A_DIM)
            except curses.error:
                pass
        else:
            filepath = ref.get("filepath", "")
            start = ref.get("start_line", "")
            end = ref.get("end_line", "")
            code = read_reference_code(ref)

            title = f"{filepath}:{start}-{end}"
            try:
                stdscr.addnstr(ref_start_y, 0, title, w - 1, curses.color_pair(2))
            except curses.error:
                pass

            code_lines = code.splitlines() if code else []
            view_h = h - ref_start_y - 3  # footer(2) + title(1)
            if view_h < 1:
                view_h = 1

            for i in range(view_h):
                ln_idx = self.ref_scroll_offset + i
                if ln_idx >= len(code_lines):
                    break
                try:
                    stdscr.addnstr(
                        ref_start_y + 1 + i,
                        0,
                        f"    {code_lines[ln_idx]}"[: w - 1],
                        w - 1,
                        curses.A_DIM,
                    )
                except curses.error:
                    pass

        # --- Footer ---
        try:
            stdscr.addnstr(h - 2, 0, "─" * (w - 1), w - 1, curses.A_DIM)
        except curses.error:
            pass

        footer_y = h - 1
        try:
            hints = "  j/k:move  q/esc:back"
            stdscr.addnstr(footer_y, 0, hints, w - 1, curses.A_DIM)
        except curses.error:
            pass

    # ─────────────────────────────────────────
    #  INPUT
    # ─────────────────────────────────────────
    def _handle_input(self, key: int) -> str:
        if self.mode == MODE_SEARCH:
            return self._handle_search_input(key)
        if self.mode == MODE_VIEW:
            return self._handle_view_input(key)
        return self._handle_operate_input(key)

    def _handle_operate_input(self, key: int) -> str:
        if key == ord("q"):
            return "QUIT"
        if key == 27:
            if len(self.filtered_indices) != len(self.notes):
                self.filtered_indices = list(range(len(self.notes)))
                self.search_query = ""
                self.cursor = 0
                self.scroll_offset = 0
            else:
                return "QUIT"

        if key in (ord("k"), curses.KEY_UP):
            self._move_up()
        elif key in (ord("j"), curses.KEY_DOWN):
            self._move_down()
        elif key == ord("/"):
            self._enter_search()
        elif key in (curses.KEY_ENTER, 10, 13):
            self._enter_view()
        elif key == ord("e"):
            self._edit_selected()
        elif key == ord("d"):
            self._delete_selected()

        return ""

    def _handle_view_input(self, key: int) -> str:
        if key in (ord("q"), 27):
            self.mode = MODE_OPERATE
            self.ref_scroll_offset = 0
        elif key in (ord("k"), curses.KEY_UP):
            if self.ref_scroll_offset > 0:
                self.ref_scroll_offset -= 1
        elif key in (ord("j"), curses.KEY_DOWN):
            sel = self._get_selected()
            if sel:
                ref = get_reference(sel[2])
                if ref:
                    code = read_reference_code(ref)
                    if self.ref_scroll_offset < len(code.splitlines()) - 1:
                        self.ref_scroll_offset += 1
        return ""

    def _handle_search_input(self, key: int) -> str:
        if key == 27:
            self.mode = MODE_OPERATE
            return ""
        elif key in (curses.KEY_ENTER, 10, 13):
            self.mode = MODE_OPERATE
            return ""
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            self.search_query = self.search_query[:-1]
            self._apply_search()
        elif 32 <= key <= 126:
            self.search_query += chr(key)
            self._apply_search()
        return ""

    # ─────────────────────────────────────────
    #  ACTIONS
    # ─────────────────────────────────────────
    def _enter_search(self):
        self.mode = MODE_SEARCH
        self.search_query = ""
        self.filtered_indices = list(range(len(self.notes)))
        self.cursor = 0
        self.scroll_offset = 0

    def _apply_search(self):
        query = self.search_query.lower()
        if not query:
            self.filtered_indices = list(range(len(self.notes)))
        else:
            self.filtered_indices = [
                i
                for i, n in enumerate(self.notes)
                if query in (n.get("content", "") or "").lower()
            ]
        self.cursor = 0
        self.scroll_offset = 0

    def _enter_view(self):
        sel = self._get_selected()
        if sel:
            self.mode = MODE_VIEW
            self.ref_scroll_offset = 0

    def _move_up(self):
        if self.cursor > 0:
            self.cursor -= 1

    def _move_down(self):
        if self.cursor < len(self.filtered_indices) - 1:
            self.cursor += 1

    def _get_selected(self) -> tuple:
        """Returns (original_list_index, display_id, note) or None."""
        visible = self._visible_notes()
        if not visible or self.cursor >= len(visible):
            return None
        orig_idx, n = visible[self.cursor]
        display_id = orig_idx + 1
        return orig_idx, display_id, n

    def _edit_selected(self):
        sel = self._get_selected()
        if not sel:
            return

        _, display_id, n = sel
        editor = os.environ.get("EDITOR", "nano")

        editor_text = format_editor_content(n)

        curses.endwin()

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", prefix="den_edit_", delete=False
            ) as tmp:
                tmp.write(editor_text)
                tmp_path = tmp.name

            subprocess.run([editor, tmp_path], check=True)

            with open(tmp_path, "r") as f:
                raw = f.read()

        except subprocess.CalledProcessError, OSError:
            self.status_msg = "Editor error."
            return
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        new_content = parse_editor_content(raw)

        if new_content == n.get("content", ""):
            self.status_msg = "No changes."
        else:
            note.edit(self.project_uid, display_id, new_content)
            self.status_msg = "✓ Edited"

        self._reload_notes()
        if self.search_query:
            self._apply_search()

    def _delete_selected(self):
        sel = self._get_selected()
        if not sel:
            return

        _, display_id, n = sel
        removed = note.remove(self.project_uid, display_id)
        if removed:
            content = removed.get("content", "")
            preview = content[:30] + ".." if len(content) > 30 else content
            self.status_msg = f"✗ Deleted: {preview}"

        self._reload_notes()
        if self.search_query:
            self._apply_search()


def _get_project_uid() -> str:
    try:
        proj = project.get()
    except ValueError as e:
        print(e)
        sys.exit(1)
    except OSError as e:
        print(f"Project error: {e}")
        sys.exit(1)

    uid = proj.get("uid")
    if not uid:
        print("Invalid project entry.")
        sys.exit(1)

    return uid


def execute(args: argparse.Namespace) -> None:
    """
    Launch the interactive den TUI.
    """
    project_uid = _get_project_uid()
    tui = TUI(project_uid)
    curses.wrapper(tui.run)
