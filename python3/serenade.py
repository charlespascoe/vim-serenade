import json
import vim

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

    # TODO: use diff to preserve marks
    vim.current.buffer[:] = lines

    # This creates a new undo block so that undo/redo works correctly
    vim.command('let &ul=&ul')

    cursor = index_to_cursor(lines, index)
    vim.current.window.cursor = cursor

    if cursor[1] == 0:
        vim.command('normal ^')


def handle_message(message):
    if len(message) == 0 or message[0] != '{':
        print('[Serenade]', message)
        return ''

    data = json.loads(message)["data"]

    result = {"message": "completed"}

    for command in data["response"]["execute"]["commandsList"]:
        ct = command["type"]
        if ct == "COMMAND_TYPE_GET_EDITOR_STATE":
            result = {
                "message": "editorState",
                "data": get_editor_state(command.get("limited", False)),
            }
        elif ct == "COMMAND_TYPE_DIFF":
            set_editor_state(command["source"], command["cursor"])
        elif ct == "COMMAND_TYPE_NEXT_TAB":
            vim.command('normal gt')
        elif ct == "COMMAND_TYPE_PREVIOUS_TAB":
            vim.command('normal gT')
        elif ct == "COMMAND_TYPE_UNDO":
            vim.command('normal u')
        elif ct == "COMMAND_TYPE_REDO":
            vim.command(r'exec "normal \<C-r>"')
        elif ct == "COMMAND_TYPE_SAVE":
            vim.command('wa') # TODO: make configurable
        elif ct == "COMMAND_TYPE_BACK":
            vim.command(r'exec "normal \<C-o>"') # TODO: make configurable
        elif ct == "COMMAND_TYPE_FORWARD":
            vim.command(r'exec "normal \<C-i>"') # TODO: make configurable
        elif ct == "COMMAND_TYPE_OPEN_FILE_LIST":
            if 'path' in command:
                # TODO: escape
                vim.command(f'e {command["path"]}')
        elif ct == 'COMMAND_TYPE_PRESS':
            handle_press(command)
        else:
            print('Unknown:', command)


    resp = json.dumps({"message": "callback", "data": {"callback": data["callback"], "data": result}})

    return resp + '\n'

keymap = {
    'up': r'\<Up>',
    'down': r'\<Down>',
}

def handle_press(command):
    print(command)
    key = keymap.get(command['text'])

    if key is None:
        print('Unknown key:', command['text'])
        return

    count = command.get('index', 1)

    vim.command(f'exec "normal {key * count}"')
