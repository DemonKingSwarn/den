<p align="center">
  <img src="https://github.com/user-attachments/assets/41d23938-ec73-4342-aafc-3caddc7b87f7" width="200" />
</p>

<p align="center">
  Braindumping for projects made easy.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.14%2B-black" />
  <img src="https://img.shields.io/badge/license-MIT-black" />
  <img src="https://img.shields.io/badge/status-active-black" />
  <img src="https://img.shields.io/badge/cli-tool-black" />
</p>

## Overview

- Thoughts are meant to be messy. `den` provides a place to put thoughts down and come back to them later.

- `den` keeps your notes tied to the project you’re working on, so nothing loses context.
As you switch projects, your notes move with you, keeping ideas organized without extra effort.

- The `den` TUI provides a fast, interactive way to navigate and manage your notes without relying on manual commands or remembering IDs.
  
- Core commands like `den add`, `den ls`, and `den rm <id>` are designed to be scriptable, making it easy to integrate den into workflows with tools like Neovim or shell aliases.

<br>

## Installation

```bash
git clone https://github.com/yourusername/den
cd den
pip install -e .
```

<br>

## Usage

### Default (interactive)

```bash
den
```

Opens an interactive TUI (fzf-based) to quickly navigate and operate on notes.

### List notes

```bash
den ls
```

Displays all saved notes.

### Add a note

```bash
den add this is an idea
```

You can pass multiple words:

```bash
den add build a realtime terrain engine
```

### Edit a note

```bash
den edit <id>
```

### Remove a note

```bash
den rm <id>
```

<br>

## Commands

| Command       | Description                   |
| ------------- | ----------------------------- |
| den           | Interactive TUI               |
| den ls        | List notes                    |
| den add ...   | Add a note                    |
| den edit <id> | Edit a note                   |
| den rm <id>   | Remove a note                 |

<br>

## Example

```bash
den add build meshlet streaming system
den add optimize renderer memory

den

den edit 1
den rm 2
```

<br>

## Dependencies

This project uses no external dependencies.

<br>

## Quick Links

[LICENSE](LICENSE)
