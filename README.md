<p align="center">
  <img src="https://github.com/user-attachments/assets/41d23938-ec73-4342-aafc-3caddc7b87f7" width="200" alt="den logo" />
</p>

<p align="center">
  <strong>Braindumping for projects made easy.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12%2B-black" alt="Python 3.12+" />
  <img src="https://img.shields.io/badge/license-MIT-black" alt="MIT License" />
  <img src="https://img.shields.io/badge/status-active-black" alt="Status Active" />
  <img src="https://img.shields.io/badge/cli-tool-black" alt="CLI Tool" />
</p>

## Overview

- **Context-Aware Notes**: Thoughts are meant to be messy. `den` provides a place to put thoughts down and come back to them later. It keeps your notes tied to the specific project you’re working on, so nothing loses context. As you switch directories and projects, your notes move with you organically.
- **Interactive TUI**: The built-in curses-based Terminal User Interface (TUI) provides a fast, keyboard-first way to navigate, search, view, and manage your notes.
- **Reference Tracking**: Anchor your thoughts to specific parts of your codebase by attaching file references directly to your notes.
- **Scriptable CLI**: Core commands (`den add`, `den ls`, `den rm`) are simple and designed to be integrated into broader developer workflows or native editor mappings (like Neovim or shell aliases).

<br>

## Installation

You can install `den` directly from the source:

```bash
git clone https://github.com/RaghavGohil/den.git
cd den
pip install -e .
```

<br>

## Usage

### Interactive Dashboard (TUI)

```bash
den
```

Opens an interactive **curses-based TUI** to quickly navigate and operate on your notes. 
- **Navigation**: `j` / `k` (or arrows)
- **Search**: `/` to start searching, `ESC` to clear
- **View Note Details**: `Enter` to open view mode (shows attached code references)
- **Edit / Delete**: `e` to edit, `d` to delete
- **Quit**: `q` or `ESC`

### List notes

```bash
den ls
```

Displays all saved notes for the current project.

### Add a note

```bash
den add <note text>
```

You can pass multiple words without quotes:
```bash
den add build a realtime terrain engine
```

**Attach a code reference:**
If your thought is linked to a specific implementation, you can track it with the `--ref` flag:
```bash
den add fix this rendering issue --ref src/engine.py:42-50
```

### Edit a note

```bash
den edit [id]
```

Opens the note in your default `$EDITOR`. If no `id` is provided, edits the most recently added note (default: 1).

### Remove a note

```bash
den rm [id]
```

Deletes a note. If no `id` is provided, removes the most recently added note (default: 1).

<br>

## Commands Summary

| Command               | Description                                    |
| --------------------- | ---------------------------------------------- |
| `den`                 | Launch interactive TUI                         |
| `den ls`              | List all notes for the current project         |
| `den add [text]`      | Add a note                                     |
| `den add --ref [path]`| Add a note with an anchored code reference     |
| `den edit [id]`       | Edit a note (defaults to the most recent note) |
| `den rm [id]`         | Remove a note (defaults to the most recent)    |

<br>

## Dependencies

This project uses **no external dependencies** (outside of the Python standard library), ensuring a lightweight and conflict-free tool logic.

<br>

## License

[MIT License](LICENSE)
