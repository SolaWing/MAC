#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOME_FILES=(.CFUserTextEncoding .bash_profile .bashrc .clang-format .config .gitconfig .lldbinit lldb_script bin)

function linkFiles () {
    for i in "${HOME_FILES[@]}"; do
        p="$DIR/$i"
        echo link "$p" in ~
        ln -s "$p" ~
    done
}
function unlinkFiles () {
    for i in "${HOME_FILES[@]}"; do
        p="$HOME/$(basename "$i")"
        if [[ -h "$p" ]]; then
            echo rm link "$p";
            rm "$p";
        fi
    done
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
