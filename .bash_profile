export EDITOR='nvim'
export LANG='zh_CN.UTF-8'
export CLICOLOR=1
export GREP_OPTIONS='--color=auto --exclude-dir=.cvs --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn'
export GREP_COLOR='1;32'
export PS1="\[\e[0;33m\]\j:\W $\[\e[0m\] "
export HISTCONTROL=ignoreboth:erasedups		# for 'ignoreboth': ignore duplicates and /^\s/
export HISTSIZE=9999

export JAVA_HOME="/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home"
#export JAVA_VERSION=1.6

alias sudo='sudo ' #space end alias will try to expand after alias
alias xargs='xargs ' #space end alias will try to expand after alias
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias l='ls -Ah'
alias ll='ls -lh'
alias la='ls -lAh'
alias g='grep -I'
alias gr='grep -RI'
alias h='history | grep'
alias md='mkdir'
alias mtab='open -b org.vim.MacVim'
alias py='python'
alias py3='python3'
alias vim='mvim'
alias bvim='nvim -b --noplugin'
alias map='xargs -n1'
alias v='nvim'
alias o='open'

alias pngquantDefault='pngquant --quality 65-90 --speed 1 --ext .png --skip-if-larger -f --'
alias tp='/Applications/TexturePacker.app/Contents/MacOS/TexturePacker'
alias em='open -a Emacs $@'
alias pause='kill -s SIGSTOP'
alias resume='kill -s SIGCONT'

# git alias
alias ga='git add'
alias gbr='git branch'
alias gc='git commit'
alias gca='git commit -a'
alias gcm='git commit --amend -C head'
alias gcam='git commit -a --amend -C head'
alias gco='git checkout'
alias gdt='git difftool'
alias gdtm='git difftool --diff-filter=MTU'
alias gd='git diff'
alias gf="git fetch"
alias gp='git pull'
alias gpr='git pull --rebase'
alias gl='git log'
alias gll='git ls-files'
alias glo='git log --graph --oneline'
alias gls='git log --stat'
alias glp=$'git log --graph --pretty=format:\'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset\' --abbrev-commit --date=relative'
alias gldel='git log --diff-filter=D --summary'
alias gm='git merge'
alias gmt='git mergetool'
alias gs='git status'
alias gsub='git submodule'
alias gsubu='git submodule update --init --recursive'
alias greset='git reset'
alias grebase='git rebase'
alias gstash='git stash'


# svn alias
alias ss='svn status'
alias sa='svn add'
alias sae='svn add --depth empty'
alias sue='svn up --depth empty --parents'
alias sr='svn revert --depth infinity'
alias srm='svn rm --force'
alias sc='svn commit'
alias sl='svn log -l 10'
alias sei='svn pe svn:ignore .'
alias ssi='svn ps svn:ignore -F' # ignoreFile(- stdin) path [path]
alias sgi='svn pg svn:ignore ' # path [path]
alias sd='svn diff'

# interactive shell will continue
[[ $- == *i* ]] || return

# up down key will recall cmd with some prefix
bind '"\e[A":history-search-backward'
bind '"\e[B":history-search-forward'
bind 'set completion-ignore-case on'
# M-hjkl = arrow key
bind '"\eh":backward-char'
bind '"\el":forward-char'
bind '"\ej":history-search-forward'
bind '"\ek":history-search-backward'

rm() {
    mv "$@" ~/.Trash
}

alias trm='/bin/rm'

clearTrash() {(
    cd ~/.Trash
    f=(`ls -A`)
    if [[ -z $f ]]; then
        return
    fi
    echo $'the following items will be delete:\n' "${f[@]}"  $'\nAre You sure [Y/N](default Y):'
    read a
    if [[ -z $a || $a == [yY] ]]; then
        /bin/rm -R "$@" "${f[@]}"
        echo done
    fi
)}

# completeSSH() {
#   curWord=${COMP_WORDS[$COMP_CWORD]}
#   if [[ $curWord == *@* ]]; then
#     #if [[ $curWord == *@*:* ]]; then
#     #  COMPREPLY=($(compgen ))
#     #  exit
#     #fi
#     hosts=$(sed -e '{s/ssh-rsa.*//
# s/,/ /
# }' ~/.ssh/known_hosts )

#     suffix=${curWord/*@/}
#     for i in $hosts; do
#       if [[ $i == *${suffix}* ]]; then
#         COMPREPLY+=(@$i)
#       fi
#     done
#   fi
#   #echo $@ #echo $COMP_CWORD #echo $COMP_LINE #echo $COMP_POINT #echo $COMP_WORDBREAK #echo $COMP_WORDS a #echo $COMPREPLY a
# }

#complete -o default -o nospace -F completeSSH ssh scp rsync
if [ -f /usr/local/Cellar/bash-completion/1.3/etc/bash_completion ]; then
    . /usr/local/Cellar/bash-completion/1.3/etc/bash_completion
fi

eval `/usr/libexec/path_helper -s` # will remove duplicates

test -e "${HOME}/.iterm2_shell_integration.bash" && source "${HOME}/.iterm2_shell_integration.bash"
