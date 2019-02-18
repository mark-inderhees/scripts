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

# Configure prompt
if [ $ANDROID_DATA ]; then
    # Android, keep the prompt to just a $
    PS1='\[\033[01;32m\]\$\[\033[00m\] '
elif [ -f /usr/bin/lsb_release ] && [[ `lsb_release -d` == *"Ubuntu"* ]]; then
    # An advanced prompt for Ubuntu
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[01;36m\]$(__git_ps1) \[\033[01;34m\]\w\[\033[00m\]\$ '
else
    # A simple prompt for other distros
    PS1='\[\033[01;32m\]\u \[\033[01;34m\]\W\[\033[00m\]\$ '
fi

# Set terminal tab title based on machine name
echo -en "\033]0;`hostname`\a"

# Stops CTRL-S from being used as XOFF flow control
stty -ixon

# To fix issues where long lines are wrapping on the same line
which resize > /dev/null 2>&1
if [ $? -eq 0 ]; then
    shopt -s checkwinsize
    eval `resize`
fi

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
if [ ! -f ~/.vimrc ]; then
    # Set vim to use bar cursor only in insert mode, else block cursor
    echo 'let &t_ti.="\e[1 q"' > ~/.vimrc
    echo 'let &t_SI.="\e[5 q"' >> ~/.vimrc
    echo 'let &t_EI.="\e[1 q"' >> ~/.vimrc
    echo 'let &t_te.="\e[0 q"' >> ~/.vimrc

    # Set vim to use 4 space tabs
    echo 'filetype plugin indent on' >> ~/.vimrc
    echo 'set tabstop=4' >> ~/.vimrc
    echo 'set shiftwidth=4' >> ~/.vimrc
    echo 'set expandtab' >> ~/.vimrc
fi

# If a .Xmodmap file does not exist, create it
# Disable middle mouse wheel button to prevent accidental pastes
if [ ! -f ~/.Xmodmap ]; then
    echo 'pointer = 1 25 3 4 5 6 7 8 9' > ~/.Xmodmap
fi

