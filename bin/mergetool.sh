#!/bin/bash

MERGED="$4"
if [[ "$MERGED" == *.png || "$MERGED" == *.jpg ]]; then
    title=(LOCAL BASE REMOTE CURRENT)
    for (( i = 1; i < 5; i++ )); do
        echo "$i open ${title[$((i-1))]}: ${!i}"
    done
    open "$@"
    read -p "choose 1-3: " n
    if [[ $n == [1-3] ]]; then
        cp "${!n}" "$MERGED"
    fi
else
    # nvim -d "$@" -c "winc b | winc J | winc = | diffoff "
    mvim -f -d "$@" -c "winc b | winc J | winc = | diffoff "
fi
