#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOME_FILES=(.CFUserTextEncoding .bash_profile .bashrc .clang-format .config .gitconfig .lldbinit lldb_script bin)

function linkfile () {
    echo link "$1" in $2
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
            l*) willLink=true ;;
            u*) willUnlink=true ;;
            -h) showHelp ;;
            --help) showHelp ;;
        esac
    done
    $willUnlink && unlinkFiles
    $willLink && linkFiles
fi
