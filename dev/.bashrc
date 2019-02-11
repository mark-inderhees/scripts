rescan()
{
    echo "Reloading $BASH_SOURCE"
    source $BASH_SOURCE
}

p()
{
    popd > /dev/null 2>&1
}

..()
{
    pushd .. > /dev/null 2>&1
}

...()
{
    pushd ../.. > /dev/null 2>&1
}

....()
{
    pushd ../../.. > /dev/null 2>&1
}

.....()
{
    pushd ../../../.. > /dev/null 2>&1
}

scpit()
{
    if [ -z "$SCP_TARGET" ]; then
        echo "Please set \$SCP_TARGET"
        return
    fi
    scp $1 root@$SCP_TARGET:~
}

f()
{
    find . -iname "$1"
}

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alFh'
alias la='ls -Ah'
alias l='ls -CFh'

DIRNAMETMP=$(dirname $BASH_SOURCE)
source $DIRNAMETMP/.bash_prompt
unset DIRNAMETMP

# Set terminal tab title based on machine name
echo -en "\033]0;`hostname`\a"

# Stops CTRL-S from being used as XOFF flow control
stty -ixon

# To fix issues where long lines are wrapping on the same line
shopt -s checkwinsize
eval `resize`

# If an .inputrc file does not exist, create it
# Set case insensitive tab completion and shift tab menu completion
# The shell will need to be restarted, this is a onetime setup
if [ ! -f ~/.inputrc ]; then
    echo '$include /etc/inputrc' > ~/.inputrc
    echo 'set completion-ignore-case On' >> ~/.inputrc
    echo 'Tab: complete' >> ~/.inputrc
    echo '"\e[Z": menu-complete' >> ~/.inputrc
fi

if [ "$XRDP_SESSION" = "1" ]; then
    gsettings set org.gnome.desktop.interface enable-animations false
fi

# If a .vimrc file does not exist, create it
# Set vim to use bar cursor only in insert mode, else block cursor
if [ ! -f ~/.vimrc ]; then
    echo 'let &t_ti.="\e[1 q"' > ~/.vimrc
    echo 'let &t_SI.="\e[5 q"' >> ~/.vimrc
    echo 'let &t_EI.="\e[1 q"' >> ~/.vimrc
    echo 'let &t_te.="\e[0 q"' >> ~/.vimrc
fi
