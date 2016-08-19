function fish_user_key_bindings
	# M-hjkl = arrow key
    bind \eh backward-char
    bind \el forward-char
    bind \ej history-search-forward
    bind \ek history-search-backward
    fzf_key_bindings
end
