" Set vim to use bar cursor only in insert mode, else block cursor
let &t_ti.="\e[1 q"
let &t_SI.="\e[5 q"
let &t_EI.="\e[1 q"
let &t_te.="\e[0 q"

" Set vim to use 4 space tabs
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab

