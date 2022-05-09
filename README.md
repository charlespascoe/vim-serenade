# Vim Plugin for Serenade.ai

Write code with your voice in Vim with [Serenade](https://serenade.ai).

Features:

- Supports multiple instances of Vim running simultaneously, switching focus as
  needed
- Supports integration with third-party plugins for language-specific features
  (e.g. jumping to definitions or debugging)
- Custom Serenade commands to do anything you want inside Vim (e.g. split view,
  buffer management, running arbitrary vimscript)

**Note: this plugin is mostly complete but still being developed.** If you have
any problems, feel free to create an issue.

- [Requirements](#requirements)
- [Installation and Usage](#installation-and-usage)
- [Configuration](#configuration)
    - [Serenade Command Configuration](#serenade-command-configuration)
- [Custom Commands](#custom-commands)
- [Troubleshooting](#troubleshooting)

## Requirements

- [Serenade](https://serenade.ai/download) (tested with 1.10.3)
- Python 3
- Python `websockets` module (`pip3 install websockets`)
- Vim 8
- Possibly
  [vim-tmux-focus-events](https://github.com/tmux-plugins/vim-tmux-focus-events)
  if you're using tmux and you use multiple Vim instances.
    - Still investigating to see if this is really needed.

Developed and tested on MacOS, should work on Linux.

## Installation and Usage

Using the built-in package management:

```
git clone https://github.com/charlespascoe/vim-serenade.git ~/.vim/pack/vim-serenade/start/vim-serenade/
```

To start the plugin and connect to Serenade, use the `SerenadeStart` command.

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
| `g:serenade_app_name` | `'Vim'` | The application name that is displayed in Serenade. |
| `g:serenade_match_re` | `'term'` | The regular expression that Seranade uses to determine whether the focused application is associated with this plugin. |

### Serenade Command Configuration

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

## Custom Commands

Serenade allows you to define custom commands to perform arbitrary actions.
Using the `evaluateInPlugin()` method, you can run arbitrary Vim commands from
custom Serenade voice commands; for example, add the following to
`~/.serenade/scripts/custom.js` to add some simple commands to control things
like splits:

```js
const vim = serenade.app('Vim');

vim.command(
  'split',
  (api) => api.evaluateInPlugin('vsplit'),
);

vim.command(
  'horizontal split',
  (api) => api.evaluateInPlugin('split'),
);

vim.command(
  'close',
  (api) => api.evaluateInPlugin('q'),
  {autoExecute: false},
);
```

You can run anything that is a valid Vim command, including running vimscript
functions (e.g. `call MyFunction()`), which you can use to pass data extracted
from voice commands.

## Troubleshooting

**Serenade doesn't detect when I switch to a different instance of Vim**

Add the following to your `vimrc`, open multiple instances of Vim, then switch
between vim instances to see if it logs a message:

`au FocusGained * echom "Focus Gained"`

This event is used to determine which instance of Vim is currently focused, and
to send a message to Serenade so that control commands are sent to the correct
instance of Vim.

If you are using tmux and nothing is logging when you switch between Vim
instances, then try installing
[vim-tmux-focus-events](https://github.com/tmux-plugins/vim-tmux-focus-events),
and be sure to set any necessary tmux config options.

If you are using some other terminal or terminal multiplexer, then you may wish
to search for "\<name of terminal/multiplexer> vim FocusGained".
