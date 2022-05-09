# Vim Plugin for Serenade.ai

A Vim plugin that connects to [Serenade](https://serenade.ai) to let you code
with your voice in Vim.

**Note: this plugin is mostly complete but still being developed.** If you have
any problems, feel free to create an issue.

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Custom Commands](#custom-commands)

## Requirements

- [Serenade](https://serenade.ai/download) (tested with 1.10.3)
- Python 3
- Python `websockets` module (`pip3 install websockets`)
- Vim 8

Developed and tested on MacOS, should work on Linux.

## Installation

Using the built-in package management:

```
git clone https://github.com/charlespascoe/vim-serenade.git ~/.vim/pack/vim-serenade/start/vim-serenade/
```

## Configuration

For Serenade to detect when Vim is focused, it uses a regular expression to
check the name of the foreground process. In `vim-serenade`, this regular
expression is configurable using the `g:serenade_match_re` in your vimrc, which
defaults to `term` (i.e. 'term' must be present somewhere in the process name,
e.g. 'iterm2' or 'terminal'). If you're using another terminal or are using
gvim, you'll need to change it to something that will match the process name:

```
let g:serenade_match_re = 'alacritty'
```

Non-command options are:

| Config Option | Default Value | Description |
|---------------|---------------|-------------|
| `g:serenade_app_name` | `'Vim'` | Sets the application name that is displayed in Serenade. |
| `g:serenade_match_re` | `'term'` | The regular expression that Seranade uses to determine whether the focused application is associated with this plugin. |

### Custom Commands

Most Serenade commands are mapped to simple Vim commands, which can be
overridden globally or on a per-buffer basis (e.g. to have different commands
for different file types). Per-buffer options are preferred over global
options, global options are preferred over the default options.

To set an option globally, use the global scope (`g:`) in your `.vimrc`:

```
let g:serenade_save_command = 'wa'
```

To set an option for a particular file type, use the buffer scope (`b:`) in the
appropriate `ftplugin` file. For example, to set the "go to definition" command
to use the [`vim-go`](https://github.com/fatih/vim-go) plugin for Go files, add
the following line to `~/.vim/ftplugin/go.vim`:

```
let b:serenade_go_to_definition_command = 'GoDef'
```

The following options are available:

| Config Option | Default Value |
|---------------|-----------------|
| `serenade_create_tab_command` | `'tabnew'` |
| `serenade_close_tab_command` | `'tabclose'` |
| `serenade_next_tab_command` | `'normal gt'` |
| `serenade_previous_tab_command` | `'normal gT'` |
| `serenade_undo_command` | `'normal u'` |
| `serenade_redo_command` | `'exec "normal \<C-r>"'` |
| `serenade_save_command` | `'w'` |
| `serenade_back_command` | `'exec "normal \<C-o>"'` |
| `serenade_forward_command` | `'exec "normal \<C-i>"'` |
| `serenade_style_command` | None |
| `serenade_go_to_definition_command` | None |
| `serenade_debugger_toggle_breakpoint_command` | None |
| `serenade_debugger_start_command` | None |
| `serenade_debugger_pause_command` | None |
| `serenade_debugger_stop_command` | None |
| `serenade_debugger_show_hover_command` | None |
| `serenade_debugger_continue_command` | None |
| `serenade_debugger_step_into_command` | None |
| `serenade_debugger_step_out_command` | None |
| `serenade_debugger_step_over_command` | None |
| `serenade_debugger_inline_breakpoint_command` | None |
| `serenade_reload_command` | None |
| `serenade_pause_command` | `''` (No-op) |
