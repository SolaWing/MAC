#!/bin/bash
# update for iterm2 3.0+
osascript -e \
'on run argv
    tell application "System Events"
        set old_frontmost to item 1 of (get name of processes whose frontmost is true)
    end tell
    tell application "iTerm"
        set myterm to (create window with profile "FZF")
        tell current session of first window
            write text "cd " & quoted form of (item 2 of argv)
            write text "export FZF_DEFAULT_OPTS=" & quoted form of (system attribute "FZF_DEFAULT_OPTS")
            write text (item 1 of argv) & "&& exit 0"
        end tell
        repeat while (exists myterm)
            delay 0.1
        end repeat
    end tell
    tell application old_frontmost
        activate
    end tell
end run' "$1" "$PWD"
