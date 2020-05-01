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

function! CloseBuffer()
    python stackexchange.close_buffer()
endfunction

function! SEFavoritesQuery(query)
    python stackexchange.favorites_query(vim.eval('a:query'))
endfunction

command! -nargs=1 PrintHello call PrintHello(<f-args>)
command! -nargs=1 SEFavoritesQuery call SEFavoritesQuery(<f-args>)
command! -nargs=0 CloseBuffer call CloseBuffer()
