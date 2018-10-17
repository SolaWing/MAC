#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOME_FILES=(
    .CFUserTextEncoding
    .bash_profile
    .bashrc
    .clang-format
    .config
    .gitconfig
    .lldbinit
    .tmux.conf
    .style.yapf
    .jshintrc
    .ctags.d
    .vim
    .hammerspoon
    lldb_script
    bin
    )
OTHER_FILES=(
    ipython_startup ~/.ipython/profile_default/startup
)

function linkfile () {
    echo link "$1" to $2
    ln -s "$1" "$2"
}
function copyfile () {
    echo copy "$1" to dir $2
    cp -af "$1" "$2"
}
function unlinkfile () {
    if [[ -h "$1" ]]; then
        echo rm link "$1";
        rm "$1";
    fi
}

function linkFiles () {
    for i in "${HOME_FILES[@]}"; do
        linkfile "$DIR/$i" ~
    done
    function f () {
        while [[ -n $1 ]]; do
            if [[ ! -e "$2" ]]; then
                mkdir -p "$(dirname "$2")"
                linkfile "$DIR/$1" "$2"
            else
                echo $2 already exists
            fi
            shift 2
        done
    }
    f "${OTHER_FILES[@]}"
    # ${#name} return 15, it's not correct
    for i in "$DIR/Services/"*; do
        copyfile "$i" "$HOME/Library/Services"
    done
}
function unlinkFiles () {
    for i in "${HOME_FILES[@]}"; do
        unlinkfile "$HOME/$(basename "$i")"
    done
    # dont remove Services, only overwrite it
    # for i in "$DIR/Services/"*; do
    #     unlinkfile "$HOME/Library/Services/$(basename "$i")"
    # done
}

function showHelp() {
    echo '
pass link to link to home.
pass unlink to unlink'
    exit 0
}

if (($#==0)); then
    showHelp
else
    willUnlink=false
    willLink=false
    for i; do
        case "$i" in
            (l*          ) willLink=true   ;;
            (u*          ) willUnlink=true ;;
            (-h | --help ) showHelp        ;;
        esac
    done
    $willUnlink && unlinkFiles
    $willLink && linkFiles
fi
