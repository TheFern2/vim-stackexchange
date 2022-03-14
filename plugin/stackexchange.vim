if !has('python3')
  echo 'vim-stackexchange requires python3 support'
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import fab_stackexchange
EOF

" def favorites_query(query, site=main_site, search_body=False):
function! SEFavoritesQuery(...)

    if a:0 == 1
        python3 fab_stackexchange.favorites_query(vim.eval('a:1'))
    elseif a:0 == 2
        python3 fab_stackexchange.favorites_query(vim.eval('a:1'), vim.eval('a:2'))
    elseif a:0 == 3
        python3 fab_stackexchange.favorites_query(vim.eval('a:1'), vim.eval('a:2'), vim.eval('a:3'))
    endif
   
endfunction

" def fetch_favorites(site=main_site):
function! SEFetchFavorites(...)

    if a:0 == 1
        python3 fab_stackexchange.fetch_favorites(vim.eval('a:1'))
    else
        python3 fab_stackexchange.fetch_favorites()
    endif

endfunction

function! SEOpenQuestion()

    python3 fab_stackexchange.open_question()

endfunction

command! -nargs=? TestHello call TestHello(<f-args>)
command! -nargs=1 PrintHello call PrintHello(<f-args>)
command! -nargs=+ SEFavoritesQuery call SEFavoritesQuery(<f-args>)
command! -nargs=? SEFetchFavorites call SEFetchFavorites(<f-args>)
command! -nargs=0 CloseBuffer call CloseBuffer()
command! -nargs=0 OpenQuestion call SEOpenQuestion()