function ws
    if count $argv > /dev/null
        cd (realpath ~/ln/$argv[1])
    else
        ls ~/ln
    end
end
