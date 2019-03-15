function fish_user_key_bindings
	# M-hjkl = arrow key
    if test $fish_bind_mode = "default"
        bind \eh backward-char
        bind \el forward-char
        bind \ej history-search-forward
        bind \ek history-search-backward
        bind \c] forward-jump
        # bind \ee my_edit_line
    else
        for m in default insert visual
            bind -M $m \eh backward-char
            bind -M $m \el forward-char
            bind -M $m \ej history-search-forward
            bind -M $m \ek history-search-backward
            bind -M $m \c] forward-jump
            # bind -M $m \ee my_edit_line
        end
    end
    fzf_key_bindings
end
