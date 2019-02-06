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

