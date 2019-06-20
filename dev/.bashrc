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

    if [ -z "$1" ]; then
        echo "Please specify a file to scp"
        echo "scpit file [user] [destination]"
        return
    fi

    if [ "$1" = "?" ]; then
        echo "scpit file [user] [destination]"
        return
    fi

    local scpuser="root"
    if [ -n "$2" ]; then
        scpuser=$2
    fi

    local dest="~"
    if [ -n "$3" ]; then
        dest=$3
    fi

    echo "executing scp $1 $scpuser@$SCP_TARGET:$dest"
    scp $1 $scpuser@$SCP_TARGET:$dest
}

f()
{
    find . -iname "$1"
}

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ccat='pygmentize -g'
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
    PS1='\[\033[01;32m\]\u \[\033[01;34m\]\w\[\033[00m\]\$ '
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

# Update .inputrc if it does not exist or is different
DIRNAMETMP=$(dirname $BASH_SOURCE)
cmp $DIRNAMETMP/.inputrc ~/.inputrc --silent
if [ $? -ne 0 ]; then
    cp $DIRNAMETMP/.inputrc ~/.inputrc
fi

if [ "$XRDP_SESSION" = "1" ]; then
    gsettings set org.gnome.desktop.interface enable-animations false
fi

# If .gitconfig does not include the shared settings, add it
grep -q .gitconfig ~/.gitconfig
if [ $? -ne 0 ]; then
    echo "[include]" >> ~/.gitconfig
    echo "    path = \"$DIRNAMETMP/.gitconfig\"" >> ~/.gitconfig
    echo "    path = \"$DIRNAMETMP/.gitconfiglinux\"" >> ~/.gitconfig
fi

# Update .vimrc if it does not exist or is different
cmp $DIRNAMETMP/.vimrc ~/.vimrc --silent
if [ $? -ne 0 ]; then
    cp $DIRNAMETMP/.vimrc ~/.vimrc
fi

# Update VS Code settings.json if it does not exist or is different
cmp $DIRNAMETMP/codesettings.json ~/.config/Code/User/settings.json --silent
if [ $? -ne 0 ]; then
    cp $DIRNAMETMP/codesettings.json ~/.config/Code/User/settings.json
fi

# Update VS Code keybindings.json if it does not exist or is different
cmp $DIRNAMETMP/codekeybindings.json ~/.config/Code/User/keybindings.json --silent
if [ $? -ne 0 ]; then
    cp $DIRNAMETMP/codekeybindings.json ~/.config/Code/User/keybindings.json
fi

# If a .Xmodmap file does not exist, create it
# Disable middle mouse wheel button to prevent accidental pastes
if [ ! -f ~/.Xmodmap ]; then
    echo 'pointer = 1 25 3 4 5 6 7 8 9' > ~/.Xmodmap
fi

# Run private script if it exists
if [ -f ~/.bashrc_private ]; then
    source ~/.bashrc_private
fi

unset DIRNAMETMP
