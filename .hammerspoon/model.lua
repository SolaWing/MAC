hsupervisor_keys = {{}, "F12"}
hshelp_keys = {{}, "F1"}
hs.loadSpoon("ModalMgr")  -- Modal wrapper

local M = spoon.ModalMgr
-- fix deactivateAll, inner use ipairs. active_list is {name: obj} pairs
function M:deactivateAll()
    self:deactivate(table.keys(self.active_list))
end
M.supervisor:bind({}, "escape", "Reset Modal Environment", function() M.supervisor:exit() end)

local function exitAll()
    M:deactivateAll()
    M.supervisor:exit()
end

local function exitAfter(f)
    return function (...)
        f(...)
        exitAll()
    end
end

-- showWindows
local showWindows = exitAfter(function ()
    hs.hints.windowHints()  -- window change hints
end)
hs.hotkey.bind(leaderModifier, "tab", nil, showWindows)
M.supervisor:bind({}, "tab", "show windows", showWindows)


-- appM modal environment
M:new("appM")
M.supervisor:bind({}, "A", "Enter AppM Environment", function()
    M:deactivateAll()
    -- Show the keybindings cheatsheet once appM is activated
    M:activate({"appM"}, "#FFBD2E", true)
end)
local cmodal = M.modal_list["appM"]

cmodal:bind('', 'escape', 'Deactivate appM',   function() M:deactivate({"appM"}) end)
cmodal:bind('', 'F1',     'Toggle Cheatsheet', function() M:toggleCheatsheet() end)

local hsapp_list = {
    {key = 'f', name = 'Finder'},
    {key = 's', name = 'Safari'},
    {key = 't', name = 'iTerm'},
    {key = 'v', name = 'MacVim'},
    {key = 'm', id = 'com.apple.ActivityMonitor'},
    {key = 'y', id = 'com.apple.systempreferences'},
}
for _, v in ipairs(hsapp_list) do
    if v.id then
        local located_name = hs.application.nameForBundleID(v.id)
        if located_name then
            cmodal:bind('', v.key, located_name, exitAfter(function()
                hs.application.launchOrFocusByBundleID(v.id)
            end))
        end
    elseif v.name then
        cmodal:bind('', v.key, v.name, exitAfter(function()
            hs.application.launchOrFocus(v.name)
        end))
    end
end
