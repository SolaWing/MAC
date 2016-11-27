function my_edit_line
	set f (mktemp -t fish_edit_line)
    command mv $f $f.fish
    set f $f.fish

    commandline -b > $f
    if test -z $EDITOR
        set e vim
    else
        set e $EDITOR
    end
    eval $e $f
    commandline -r (more $f)
    command rm $f
end
