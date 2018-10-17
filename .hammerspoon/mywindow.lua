local win = {}
-- local function win:dock(direction)
--     self = self or hs.window.focusedWindow()
--     if direction == "left"
-- end

-- @dockmode: 0 change the right-bottom size. 1 change the left-top size. nil to guess
function win:stepSize(width, height)
    local cwin = self == win and hs.window.focusedWindow() or self
    if not cwin then
        hs.alert.show("No focused window!")
    end

    local cscreen = cwin:screen()
    local cres = cscreen:fullFrame()
    local wf = cwin:frame()

    print(wf, cres)
    if width then
        local changeLeft = (wf.x - cres.x) > (cres.x2 - wf.x2)
        if -1 < width and width < 1 then
            width = cres.w * width
        end
        wf.w = wf.w + width
        if changeLeft then
            wf.x = wf.x - width
        end
    end
    if height then
        local changeTop = (wf.y - cres.y) > (cres.y2 - wf.y2)
        if -1 < height and height < 1 then
            height = cres.w * height
        end
        wf.h = wf.h + height
        if changeTop then
            wf.y = wf.y - height
        end
    end
    cwin:setFrame(wf)
end

return win
