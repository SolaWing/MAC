leaderModifier = {"cmd", "shift", "ctrl"}

hs.hotkey.bind(leaderModifier, 'R', "Reload Configuration", function()
    hs.reload()
end)

local showWindows = function ()
    hs.hints.windowHints()  -- window change hints
end
hs.hotkey.bind(leaderModifier, "tab", nil, showWindows)

-- window management
hs.loadSpoon('WinWin')
local WinWin = spoon.WinWin

windowMode = hs.hotkey.modal.new(leaderModifier, "space", "Window Mode")
windowMode:bind({},             "escape", "Exit Window Mode", function () windowMode:exit() end)
windowMode:bind(leaderModifier, "space",  "Exit Window Mode", function () windowMode:exit() end)

windowMode:bind('',      'A',     'Move Leftward',            function() WinWin:stepMove("left") end,        nil, function() WinWin:stepMove("left") end)
windowMode:bind('',      'D',     'Move Rightward',           function() WinWin:stepMove("right") end,       nil, function() WinWin:stepMove("right") end)
windowMode:bind('',      'W',     'Move Upward',              function() WinWin:stepMove("up") end,          nil, function() WinWin:stepMove("up") end)
windowMode:bind('',      'S',     'Move Downward',            function() WinWin:stepMove("down") end,        nil, function() WinWin:stepMove("down") end)
windowMode:bind('',      'H',     'Lefthalf of Screen',       function() WinWin:stash() WinWin:moveAndResize("halfleft") end)
windowMode:bind('',      'L',     'Righthalf of Screen',      function() WinWin:stash() WinWin:moveAndResize("halfright") end)
windowMode:bind('',      'K',     'Uphalf of Screen',         function() WinWin:stash() WinWin:moveAndResize("halfup") end)
windowMode:bind('',      'J',     'Downhalf of Screen',       function() WinWin:stash() WinWin:moveAndResize("halfdown") end)
windowMode:bind('',      'Y',     'NorthWest Corner',         function() WinWin:stash() WinWin:moveAndResize("cornerNW") end)
windowMode:bind('',      'O',     'NorthEast Corner',         function() WinWin:stash() WinWin:moveAndResize("cornerNE") end)
windowMode:bind('',      'U',     'SouthWest Corner',         function() WinWin:stash() WinWin:moveAndResize("cornerSW") end)
windowMode:bind('',      'I',     'SouthEast Corner',         function() WinWin:stash() WinWin:moveAndResize("cornerSE") end)
windowMode:bind('',      'F',     'Fullscreen',               function() WinWin:stash() WinWin:moveAndResize("fullscreen") end)
windowMode:bind('',      'C',     'Center Window',            function() WinWin:stash() WinWin:moveAndResize("center") end)
windowMode:bind('',      '=',     'Stretch Outward',          function() WinWin:moveAndResize("expand") end, nil, function() WinWin:moveAndResize("expand") end)
windowMode:bind('',      '-',     'Shrink Inward',            function() WinWin:moveAndResize("shrink") end, nil, function() WinWin:moveAndResize("shrink") end)
windowMode:bind('shift', 'H',     'Move Leftward',            function() WinWin:stepResize("left") end,      nil, function() WinWin:stepResize("left") end)
windowMode:bind('shift', 'L',     'Move Rightward',           function() WinWin:stepResize("right") end,     nil, function() WinWin:stepResize("right") end)
windowMode:bind('shift', 'K',     'Move Upward',              function() WinWin:stepResize("up") end,        nil, function() WinWin:stepResize("up") end)
windowMode:bind('shift', 'J',     'Move Downward',            function() WinWin:stepResize("down") end,      nil, function() WinWin:stepResize("down") end)
windowMode:bind('',      'left',  'Move to Left Monitor',     function() WinWin:stash() WinWin:moveToScreen("left") end)
windowMode:bind('',      'right', 'Move to Right Monitor',    function() WinWin:stash() WinWin:moveToScreen("right") end)
windowMode:bind('',      'up',    'Move to Above Monitor',    function() WinWin:stash() WinWin:moveToScreen("up") end)
windowMode:bind('',      'down',  'Move to Below Monitor',    function() WinWin:stash() WinWin:moveToScreen("down") end)
windowMode:bind('',      'space', 'Move to Next Monitor',     function() WinWin:stash() WinWin:moveToScreen("next") end)
windowMode:bind('',      '[',     'Undo Window Manipulation', function() WinWin:undo() end)
windowMode:bind('',      ']',     'Redo Window Manipulation', function() WinWin:redo() end)
windowMode:bind('',      '`',     'Center Cursor',            function() WinWin:centerCursor() end)

hs.alert.show("Hammerspoon Config loaded")
