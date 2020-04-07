-- http://www.hammerspoon.org/docs/index.html
hs.hotkey.alertDuration = 0.4
leaderModifier = {"ctrl", "alt"}
require "myext"
-- require "model"
-- win = require "mywindow"

-- manual reload
-- hs.hotkey.bind(leaderModifier, 'R', "Reload Configuration", function()
--     hs.reload()
-- end)


-- fix: cross screen focus correct window
function hs.window:focus()
  local app=self:application()
  self:becomeMain()
  app:_bringtofront()
  -- if app:bundleID()=='com.apple.finder' then --workaround for the desktop taking over
    -- it may look like this should ideally go inside :becomeMain(), but the problem is actually
    -- triggered by :_bringtofront(), so the workaround belongs here
    if desktopFocusWorkaroundTimer then desktopFocusWorkaroundTimer:stop() end
    desktopFocusWorkaroundTimer=hs.timer.doAfter(0.05,function()
      -- 0.3s comes from https://github.com/Hammerspoon/hammerspoon/issues/581
      -- it'd be slightly less ugly to use a "space change completed" callback (as per issue above) rather than
      -- a crude timer, althought that route is a lot more complicated
      self:becomeMain()
      desktopFocusWorkaroundTimer=nil --cleanup the timer
    end)
    self:becomeMain()
  -- end
  return self
end

local showWindows = function ()
    hs.hints.windowHints()  -- window change hints
end
hs.hotkey.bind(leaderModifier, "tab", nil, showWindows)

-- window management
hs.loadSpoon('WinWin')
local WinWin = spoon.WinWin

windowMode = hs.hotkey.modal.new(leaderModifier, "space", "Window Mode")
windowMode:bind(leaderModifier, "space",  "Exit Window Mode", function () windowMode:exit() end)
windowMode:bind({},             "escape", "Exit Window Mode", function () windowMode:exit() end)
windowMode:bind({},             "return", "Exit Window Mode", function () windowMode:exit() end)

windowMode:bind({},             "tab",    nil,                showWindows)

windowMode:bind('',      'H', 'Move Leftward',    function() WinWin:stepMove("left") end,                             nil, function() WinWin:stepMove("left") end)
windowMode:bind('',      'L', 'Move Rightward',   function() WinWin:stepMove("right") end,                            nil, function() WinWin:stepMove("right") end)
windowMode:bind('',      'K', 'Move Upward',      function() WinWin:stepMove("up") end,                               nil, function() WinWin:stepMove("up") end)
windowMode:bind('',      'J', 'Move Downward',    function() WinWin:stepMove("down") end,                             nil, function() WinWin:stepMove("down") end)
windowMode:bind('alt', 'H', 'Minus Width',      function() WinWin:stepResize("left") end,                           nil, function() WinWin:stepResize("left") end)
windowMode:bind('alt', 'L', 'Plus Width',       function() WinWin:stepResize("right") end,                          nil, function() WinWin:stepResize("right") end)
windowMode:bind('alt', 'K', 'Minus Height',     function() WinWin:stepResize("up") end,                             nil, function() WinWin:stepResize("up") end)
windowMode:bind('alt', 'J', 'Plus Height',      function() WinWin:stepResize("down") end,                           nil, function() WinWin:stepResize("down") end)
windowMode:bind('shift',  'H', 'Plus Left Width',  function() WinWin:stepResize("right"); WinWin:stepMove("left") end, nil, function() WinWin:stepResize("right"); WinWin:stepMove("left") end)
windowMode:bind('shift',  'L', 'Minus Left Width', function() WinWin:stepResize("left"); WinWin:stepMove("right") end, nil, function() WinWin:stepResize("left"); WinWin:stepMove("right") end)
windowMode:bind('shift',  'K', 'Plus Top Height',  function() WinWin:stepResize("down"); WinWin:stepMove("up") end,    nil, function() WinWin:stepResize("down"); WinWin:stepMove("up") end)
windowMode:bind('shift',  'J', 'Minus Top Height', function() WinWin:stepResize("up"); WinWin:stepMove("down") end,    nil, function() WinWin:stepResize("up"); WinWin:stepMove("down") end)
windowMode:bind('',      'A',     'Lefthalf of Screen',       function() hs.window.focusedWindow():moveToUnit({0,   0,   0.5, 1})   end)
windowMode:bind('',      'D',     'Righthalf of Screen',      function() hs.window.focusedWindow():moveToUnit({0.5, 0,   0.5, 1})   end)
windowMode:bind('',      'W',     'Uphalf of Screen',         function() hs.window.focusedWindow():moveToUnit({0,   0,   1,   0.5}) end)
windowMode:bind('',      'X',     'Downhalf of Screen',       function() hs.window.focusedWindow():moveToUnit({0,   0.5, 1,   0.5}) end)
windowMode:bind('',      'Q',     'NorthWest Corner',         function() hs.window.focusedWindow():moveToUnit({0,   0,   0.5, 0.5}) end)
windowMode:bind('',      'E',     'NorthEast Corner',         function() hs.window.focusedWindow():moveToUnit({0.5, 0,   0.5, 0.5}) end)
windowMode:bind('',      'Z',     'SouthWest Corner',         function() hs.window.focusedWindow():moveToUnit({0,   0.5, 0.5, 0.5}) end)
windowMode:bind('',      'C',     'SouthEast Corner',         function() hs.window.focusedWindow():moveToUnit({0.5, 0.5, 0.5, 0.5}) end)
windowMode:bind('',      'F',     'Fullscreen',               function() hs.window.focusedWindow():moveToUnit({0,   0,   1,   1})   end)

windowMode:bind('shift',      'A',     'Left 2/3 of Screen',       function() hs.window.focusedWindow():moveToUnit({0,   0,   2/3, 1})   end)
windowMode:bind('shift',      'D',     'Right 2/3 of Screen',      function() hs.window.focusedWindow():moveToUnit({1/3, 0,   2/3, 1})   end)
windowMode:bind('shift',      'W',     'Up 2/3 of Screen',         function() hs.window.focusedWindow():moveToUnit({0,   0,   1,   2/3}) end)
windowMode:bind('shift',      'X',     'Down 2/3 of Screen',       function() hs.window.focusedWindow():moveToUnit({0,   1/3, 1,   2/3}) end)
windowMode:bind('shift',      'Q',     'NorthWest Corner',         function() hs.window.focusedWindow():moveToUnit({0,   0,   2/3, 2/3}) end)
windowMode:bind('shift',      'E',     'NorthEast Corner',         function() hs.window.focusedWindow():moveToUnit({1/3, 0,   2/3, 2/3}) end)
windowMode:bind('shift',      'Z',     'SouthWest Corner',         function() hs.window.focusedWindow():moveToUnit({0,   1/3, 2/3, 2/3}) end)
windowMode:bind('shift',      'C',     'SouthEast Corner',         function() hs.window.focusedWindow():moveToUnit({1/3, 1/3, 2/3, 2/3}) end)
windowMode:bind({'shift', 'alt'},      'A',     'Left 1/3 of Screen',       function() hs.window.focusedWindow():moveToUnit({0,   0,   1/3, 1})   end)
windowMode:bind({'shift', 'alt'},      'D',     'Right 1/3 of Screen',      function() hs.window.focusedWindow():moveToUnit({2/3, 0,   1/3, 1})   end)
windowMode:bind({'shift', 'alt'},      'W',     'Up 1/3 of Screen',         function() hs.window.focusedWindow():moveToUnit({0,   0,   1,   1/3}) end)
windowMode:bind({'shift', 'alt'},      'X',     'Down 1/3 of Screen',       function() hs.window.focusedWindow():moveToUnit({0,   2/3, 1,   1/3}) end)
windowMode:bind({'shift', 'alt'},      'Q',     'NorthWest Corner',         function() hs.window.focusedWindow():moveToUnit({0,   0,   1/3, 1/3}) end)
windowMode:bind({'shift', 'alt'},      'E',     'NorthEast Corner',         function() hs.window.focusedWindow():moveToUnit({2/3, 0,   1/3, 1/3}) end)
windowMode:bind({'shift', 'alt'},      'Z',     'SouthWest Corner',         function() hs.window.focusedWindow():moveToUnit({0,   2/3, 1/3, 1/3}) end)
windowMode:bind({'shift', 'alt'},      'C',     'SouthEast Corner',         function() hs.window.focusedWindow():moveToUnit({2/3, 2/3, 1/3, 1/3}) end)

windowMode:bind('',      'S',     'Center Window',            function() hs.window.focusedWindow():centerOnScreen()   end)
windowMode:bind('',      '=',     'Stretch Outward',          function() WinWin:moveAndResize("expand") end, nil, function() WinWin:moveAndResize("expand") end)
windowMode:bind('',      '-',     'Shrink Inward',            function() WinWin:moveAndResize("shrink") end, nil, function() WinWin:moveAndResize("shrink") end)

windowMode:bind('',      'left',  'Move to Left Monitor',     function() WinWin:moveToScreen("left") end)
windowMode:bind('',      'right', 'Move to Right Monitor',    function() WinWin:moveToScreen("right") end)
windowMode:bind('',      'up',    'Move to Above Monitor',    function() WinWin:moveToScreen("up") end)
windowMode:bind('',      'down',  'Move to Below Monitor',    function() WinWin:moveToScreen("down") end)
windowMode:bind('',      'space', 'Move to Next Monitor',     function() WinWin:moveToScreen("next") end)
-- windowMode:bind('',      '[',     'Undo Window Manipulation', function() WinWin:undo() end)
-- windowMode:bind('',      ']',     'Redo Window Manipulation', function() WinWin:redo() end)
windowMode:bind('',      '`',     'Center Cursor',            function() WinWin:centerCursor() end)

hs.alert.show("Hammerspoon Config loaded")
