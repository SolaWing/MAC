function fish_user_key_bindings
	# M-hjkl = arrow key
    bind \eh backward-char
    bind \el forward-char
    bind \ej history-search-forward
    bind \ek history-search-backward
    bind \c] forward-jump
    fzf_key_bindings
    bind \ee my_edit_line
end
