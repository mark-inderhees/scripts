if filereadable(expand("$VIM/_vimrc"))
    source $VIM\_vimrc
endif

set nobackup
set noundofile

" Set vim to use bar cursor only in insert mode, else block cursor
if has("unix")
    let &t_ti.="\e[1 q"
    let &t_SI.="\e[5 q"
    let &t_EI.="\e[1 q"
    let &t_te.="\e[0 q"
endif

" Set vim to use 4 space tabs
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab
