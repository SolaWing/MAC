isBinaryType() {
    [[ $(file -I $1) == *=binary ]]
    return
}

if isBinaryType $MERGED; then
    if [[ $LOCAL = "/dev/null" ]]; then
        echo add $'\e[32m'$MERGED$'\e[0m'
    elif [[ $REMOTE = "/dev/null" ]]; then
        echo delete $'\e[32m'$MERGED$'\e[0m'
    else
        echo modify $'\e[32m'$MERGED$'\e[0m'
    fi
else
    if [[ $MERGED = $LOCAL || $MERGED = $REMOTE ]]; then
        echo diff $'\e[32m'$LOCAL$'\e[0m' '<==>' $'\e[32m'$REMOTE$'\e[0m'
        mvim -d -f $LOCAL $REMOTE
    else
        echo diff $'\e[32m'$LOCAL$'\e[0m' '<==' $'\e[1;30;42m'$MERGED$'\e[0m' '==>' $'\e[32m'$REMOTE$'\e[0m'
        mvim -d -f $LOCAL $REMOTE $MERGED -c "winc b | winc J | winc ="
    fi
fi
