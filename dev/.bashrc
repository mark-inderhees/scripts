..()
{
    cd ..
}

...()
{
    cd ..
    cd ..
}

....()
{
    cd ..
    cd ..
    cd ..
}

.....()
{
    cd ..
    cd ..
    cd ..
    cd ..
}

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alFh'
alias la='ls -Ah'
alias l='ls -CFh'

if [ -e ~/.bash_prompt ]; then
    source ~/.bash_prompt
fi

