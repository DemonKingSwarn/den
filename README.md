<p align="center">
  <img src="https://github.com/user-attachments/assets/41d23938-ec73-4342-aafc-3caddc7b87f7" width="200" alt="den logo" />
</p>

<p align="center">
  <strong>Context management for projects made easy.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12%2B-black" alt="Python 3.12+" />
  <img src="https://img.shields.io/badge/license-MIT-black" alt="MIT License" />
  <img src="https://img.shields.io/badge/status-active-black" alt="Status Active" />
  <img src="https://img.shields.io/badge/cli-tool-black" alt="CLI Tool" />
</p>

## Overview

### My Problem

When working in a complex codebase, I need a fast way to capture and retrieve context tied to specific parts of the project.

Inline notes like ```TODO``` or ```FIXME``` are intrusive and leak internal intent into the codebase.

External note-taking tools are disconnected from the workflow and introduce unnecessary friction.

AI tools can summarize past work, but they remain bound to session-based context and are not a persistent, structured layer over the project.

### How ```den``` Solves This

```den``` is a tool for capturing and retrieving context scoped per project without breaking your flow.

- **Terminal-first access**: Run ```den recent``` to surface recent context when opening a shell session.
- **Project-scoped storage**: Context is isolated per project, determined by the nearest ```.git``` directory found by traversing upward from the current working directory.
- **Fast capture**: Bind ```den add``` to editor shortcuts (e.g. Neovim). Capture selected code as context without leaving the buffer.
- **Portable storage**: Context is stored locally and can be versioned or synced using standard tooling like ```git```.
- **CLI core**: ```den add```, ```den rm```, ```den ls```, etc. for scriptable, precise operations.
- **TUI interface**: ```den``` launches an interactive session to browse, create, and edit context.

<br>

## Installation

> [!IMPORTANT]
> The PyPI package name is `den-python`, but the installed command is `den`. Requires **Python 3.12+**.

### pip (PyPI)

The recommended way to install `den` is using `pip` (or `pipx` for an isolated environment):

```bash
pip install den-python
```

### Arch Linux (AUR)

If you are using Arch Linux, you can install from the AUR:

```bash
yay -S den
```

### Debian

If you are using a debian based system, you can install from [releases](https://github.com/RaghavGohil/den/releases):

```bash
sudo apt install ./den-version.deb
```

### From Source

You can always clone and install directly from the source:

```bash
git clone https://github.com/RaghavGohil/den.git
cd den
pip install .
```
<br>

## Usage

### Interactive Dashboard (TUI)

```bash
den
```

Opens an interactive **curses-based TUI** to quickly navigate and operate on your notes. 

### Recent Activity

```bash
den recent
```

Fetches the most recent notes globally across all your projects. Hook this to your `.bashrc` or `.zshrc` to get a workflow summary when you open a terminal.

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
| `den recent`          | Fetch globally recent notes across projects    |
| `den ls`              | List all notes for the current project         |
| `den add [text]`      | Add a note                                     |
| `den add --ref [path]`| Add a note with an anchored code reference     |
| `den edit [id]`       | Edit a note (defaults to the most recent note) |
| `den rm [id]`         | Remove a note (defaults to the most recent)    |

<br>

## Dependencies

This project uses **no external dependencies** (outside of the Python standard library), ensuring a lightweight and conflict-free tool logic.

<br>

## Additional notes

If you find this project to be useful, please don't forget to leave a **star**. This keeps me motivated to continue working on the project.

## License

[MIT License](LICENSE)
