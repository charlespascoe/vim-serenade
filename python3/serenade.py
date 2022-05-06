import json
import vim
import difflib

diff = difflib.Differ()

def cursor_to_index(lines, cursor):
    row, col = cursor

    count = sum(len(line) + 1 for line in lines[:row-1])
    count += col

    return count

def index_to_cursor(lines, index):
    x = index
    l = 0

    while x >= len(lines[l]) + 1:
        x -= len(lines[l]) + 1
        l += 1

    return (l + 1, x)

def print_current_file():
    lines = vim.current.buffer[:]
    print(len(lines))
    cursor = vim.current.window.cursor
    src = '\n'.join(lines)
    print(len(src.split('\n')))
    index = cursor_to_index(lines, cursor)
    print(src[:index] + '|' + src[index:])

    print(cursor, index_to_cursor(src, index))

def get_editor_state(limited):
    filename = vim.current.buffer.name

    if limited:
        return {"filename": filename}

    lines = vim.current.buffer[:]
    src = '\n'.join(lines)
    cursor = vim.current.window.cursor
    return {
        "source": src,
        "cursor": cursor_to_index(lines, cursor),
        "filename": filename,
    }

def set_editor_state(src, index):
    lines = src.split('\n')

    i = 0
    j = 0

    for line in diff.compare(vim.current.buffer[:], lines):
        if line.startswith('  '):
            i += 1
            j += 1
        elif line.startswith('- '):
            del vim.current.buffer[i]
        elif line.startswith('+ '):
            vim.current.buffer.append(lines[j], i)
            i += 1
            j += 1

    # This creates a new undo block so that undo/redo works correctly
    vim.command('let &ul=&ul')

    cursor = index_to_cursor(lines, index)
    vim.current.window.cursor = cursor

    if cursor[1] == 0:
        vim.command('normal ^')


def get_config(key, default=None):
    cmd = vim.eval(f'get(b:, "serenade_{key}", "")')

    if cmd != '':
        return cmd

    cmd = vim.eval(f'get(g:, "serenade_{key}", "")')

    if cmd != '':
        return cmd

    return default


simple_commands = {
    'COMMAND_TYPE_CREATE_TAB':
        'tabnew',
    'COMMAND_TYPE_CLOSE_TAB':
        'tabclose',
    'COMMAND_TYPE_NEXT_TAB':
        'normal gt',
    'COMMAND_TYPE_PREVIOUS_TAB':
        'normal gT',

    'COMMAND_TYPE_UNDO':
        'normal u',
    'COMMAND_TYPE_REDO':
        r'exec "normal \<C-r>"',

    'COMMAND_TYPE_SAVE':
        'w',

    'COMMAND_TYPE_BACK':
        r'exec "normal \<C-o>"',
    'COMMAND_TYPE_FORWARD':
        r'exec "normal \<C-i>"',

    'COMMAND_TYPE_STYLE':
        None,
    'COMMAND_TYPE_GO_TO_DEFINITION':
        None,

    'COMMAND_TYPE_DEBUGGER_TOGGLE_BREAKPOINT':
        None,
    'COMMAND_TYPE_DEBUGGER_START':
        None,
    'COMMAND_TYPE_DEBUGGER_PAUSE':
        None,
    'COMMAND_TYPE_DEBUGGER_STOP':
        None,
    'COMMAND_TYPE_DEBUGGER_SHOW_HOVER':
        None,
    'COMMAND_TYPE_DEBUGGER_CONTINUE':
        None,
    'COMMAND_TYPE_DEBUGGER_STEP_INTO':
        None,
    'COMMAND_TYPE_DEBUGGER_STEP_OUT':
        None,
    'COMMAND_TYPE_DEBUGGER_STEP_OVER':
        None,
    'COMMAND_TYPE_DEBUGGER_INLINE_BREAKPOINT':
        None,

    'COMMAND_TYPE_RELOAD':
        None,

    'COMMAND_TYPE_PAUSE':
        '', # no-op

    # TODO
    #'COMMAND_TYPE_OPEN_FILE_LIST': None,
    #'COMMAND_TYPE_OPEN_FILE': None,
    #'COMMAND_TYPE_SCROLL': None,
    #'COMMAND_TYPE_SELECT': None,
    #'COMMAND_TYPE_CLICK': None,
}

def command_to_config_key(command_type):
    return command_type[len('COMMAND_TYPE_'):].lower() + '_command'

def handle_message(message):
    if len(message) == 0 or message[0] != '{':
        print('[Serenade]', message)
        return ''

    data = json.loads(message)["data"]

    result = {"message": "completed"}

    for command in data["response"]["execute"]["commandsList"]:
        ct = command["type"]
        # TODO: Proper logging
        # print('Command: ' + ct)

        if ct in simple_commands:
            config_key = command_to_config_key(ct)
            vim_cmd = get_config(config_key, simple_commands[ct])

            if vim_cmd is None:
                print(f'You need to set either b:serenade_{config_key} or g:serenade_{config_key} to use this operation')
            elif vim_cmd != '':
                vim.command(vim_cmd)
        elif ct == "COMMAND_TYPE_GET_EDITOR_STATE":
            result = {
                "message": "editorState",
                "data": get_editor_state(command.get("limited", False)),
            }
        elif ct == "COMMAND_TYPE_DIFF":
            set_editor_state(command["source"], command["cursor"])
        elif ct == "COMMAND_TYPE_OPEN_FILE_LIST":
            if 'path' in command:
                # TODO: escape
                vim.command(f'e {command["path"]}')
        elif ct == 'COMMAND_TYPE_SWITCH_TAB':
            index = command.get('index')

            if index is not None:
                vim.command(f'normal {index}gt')
        elif ct == 'COMMAND_TYPE_PRESS':
            handle_press(command)
        else:
            print('Unknown:', command)

    resp = json.dumps({"message": "callback", "data": {"callback": data["callback"], "data": result}})

    return resp + '\n'

keymap = {
    'up': r'\<Up>',
    'down': r'\<Down>',
    'left': r'\<Left>',
    'right': r'\<Right>',
    'pagedown': r'\<Pagedown>',
    'pageup': r'\<Pageup>',
}

def handle_press(command):
    print(command)
    key = keymap.get(command['text'])

    if key is None:
        print(command)
        print('Unknown key:', command['text'])
        return

    count = max(command.get('index', 1), 1)

    vim.command(f'exec "normal {key * count}"')
