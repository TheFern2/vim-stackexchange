let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import stackexchange
EOF

function! PrintHello(name)
    python stackexchange.say_hello(vim.eval('a:name'))
endfunction

function! TestHello(...)

    if a:0 == 1
        python stackexchange.say_hello(vim.eval('a:1'))
    else
        python stackexchange.say_hello()
    endif
endfunction

function! CloseBuffer()
    python stackexchange.close_buffer()
endfunction

"function! SEFavoritesQuery(query)
"    python stackexchange.favorites_query(vim.eval('a:query'))
"endfunction

" def favorites_query(query, site=main_site, search_body=False):
function! SEFavoritesQuery(...)

    "echom a:0

    if a:0 == 1
        python stackexchange.favorites_query(vim.eval('a:1'))
    elseif a:0 == 2
        python stackexchange.favorites_query(vim.eval('a:1'), vim.eval('a:2'))
    elseif a:0 == 3
        python stackexchange.favorites_query(vim.eval('a:1'), vim.eval('a:2'), vim.eval('a:3'))
    endif

endfunction

function! SEFetchFavorites(...)

    if a:0 == 1
        python stackexchange.fetch_favorites(vim.eval('a:1'))
    else
        python stackexchange.fetch_favorites()
    endif

endfunction

function! SEOpenQuestion()
    python stackexchange.open_question()
endfunction

command! -nargs=? TestHello call TestHello(<f-args>)
command! -nargs=1 PrintHello call PrintHello(<f-args>)
"command! -nargs=1 SEFavoritesQuery call SEFavoritesQuery(<f-args>)
command! -nargs=+ SEFavoritesQuery call SEFavoritesQuery(<f-args>)
command! -nargs=? SEFetchFavorites call SEFetchFavorites(<f-args>)
command! -nargs=0 CloseBuffer call CloseBuffer()
command! -nargs=0 OpenQuestion call SEOpenQuestion()
