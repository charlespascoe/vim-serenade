let s:client_path = expand('<sfile>:p:h:h').'/serenade_client.py'
let s:serenade_running = 0

let g:serenade_app_name = get(g:, 'serenade_app_name', 'Vim')
let g:serenade_match_re = get(g:, 'serenade_match_re', 'term')

let s:ws_addr = get(g:, 'serenade_websocket_address', 'ws://localhost:17373')
let s:should_log = get(g:, 'serenade_enable_logging', 0)

func serenade#Init()
    if s:serenade_running
        return
    end

    let s:serenade_running = 1

    let s:job = job_start(['python3', s:client_path, g:serenade_app_name, g:serenade_match_re, s:ws_addr, s:should_log], {
    \    'out_io': 'pipe',
    \    'err_io': 'pipe',
    \    'in_io': 'pipe',
    \    'mode': 'nl',
    \    'callback': 'serenade#OnOutput',
    \    'err_cb': 'serenade#OnError',
    \    'exit_cb': 'serenade#OnExit',
    \    'stoponexit': 'term'
    \})

    py3 import serenade

    " Needed to allow the cursor to go past the last character (which Serenade
    " expects)
    set ve+=onemore

    au FocusGained * call serenade#Active()

	" The following is required because Serenade both sends a command to press
	" the arrow keys, along with sending the actual key presses. It essentially
	" temporarily disables the keys after handling the command.

	noremap <expr> <Up> py3eval('serenade.should_allow_key("up")') ? "\<Up>" : ""
	noremap <expr> <Down> py3eval('serenade.should_allow_key("down")') ? "\<Down>" : ""
	noremap <expr> <Left> py3eval('serenade.should_allow_key("left")') ? "\<Left>" : ""
	noremap <expr> <Right> py3eval('serenade.should_allow_key("right")') ? "\<Right>" : ""

	inoremap <expr> <Up> py3eval('serenade.should_allow_key("up")') ? "\<Up>" : ""
	inoremap <expr> <Down> py3eval('serenade.should_allow_key("down")') ? "\<Down>" : ""
	inoremap <expr> <Left> py3eval('serenade.should_allow_key("left")') ? "\<Left>" : ""
	inoremap <expr> <Right> py3eval('serenade.should_allow_key("right")') ? "\<Right>" : ""
endfun

func serenade#InitBufferConfig(key, default)
    let fullkey = 'b:serenade_'.a:key
    let b:[key] = get(b:, fullkey, a:default)
endfun

func serenade#OnOutput(job, msg)
    let g:__serenade_message = a:msg
    let res = py3eval('serenade.handle_message(vim.eval("g:__serenade_message"))')

    if res == ""
        return
    end

    let ch = job_getchannel(s:job)

    call ch_sendraw(ch, res)
endfun

func serenade#Active()
    if exists('s:job')
        let ch = job_getchannel(s:job)

        call ch_sendraw(ch, "active\n")
    end
endfun

func serenade#OnError(job, msg)
    echom "Msg: ".a:msg
endfun

func serenade#OnExit(job, code)
    echom "Code: ".a:code
endfun

func serenade#RegisterUndo()
    let &ul=&ul
endfun
