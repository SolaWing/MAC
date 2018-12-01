#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os.path, subprocess, sys


def main():
    # finder only accept abspath
    to_remove = [
        os.path.abspath(p) for p in sys.argv[1:] if os.path.lexists(p) # lexists check can also reject flags
    ]
    if len(to_remove) < 1:
        print("nothing to remove.")
        return

    print("will remove:\n" + "\n".join(to_remove))

    # js script has bugs, can't delete multiple file and folder correctly, so use osascript.
    osascript = """
on run argv
    set toDelete to {}
    repeat with p in argv
        set end of toDelete to (POSIX file p)
    end repeat
    tell application "Finder" to delete toDelete
end run
    """

    try:
        from subprocess import DEVNULL  # py3
    except ImportError:
        DEVNULL = open(os.devnull, 'wb')

    p = subprocess.Popen(["osascript", '-'] + to_remove, stdin=subprocess.PIPE, stdout=DEVNULL)
    p.communicate(osascript)

    print("finish!")


if __name__ == "__main__":
    main()
