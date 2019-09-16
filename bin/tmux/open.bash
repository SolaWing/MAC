# exec >/tmp/out

read -r line

EDITOR="${EDITOR:-/usr/local/bin/nvim}"
if [[ -e "$line" ]]; then
    /usr/local/bin/tmux new-window "$EDITOR" "$line"
fi
