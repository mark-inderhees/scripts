if filereadable(expand("$VIM/_vimrc"))
    source $VIM\_vimrc
endif

set nobackup
set noundofile

set number
set incsearch
set ignorecase 

" Set vim to use bar cursor only in insert mode, else block cursor
if has("unix")
    let &t_ti.="\e[1 q" " term init, use block
    let &t_SI.="\e[5 q" " start insert, use ibeam
    let &t_EI.="\e[1 q" " end insert, use block
    let &t_te.="\e[5 q" " term exit, use ibeam
endif

" Set vim to use 4 space tabs
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab

" Remap Ctrl-* keys to \*
nnoremap <Leader>w <C-w>

" Use system clipboard instead of vim clipboard
set clipboard=unnamedplus

" Tell vim the term is dark background so colors are readable
set background=dark

" Enable folder specific .vimrc files and make them secure
set exrc
set secure

