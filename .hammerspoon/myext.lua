-- Table
function table:print()
    for name,val in pairs(self) do
        print(name, " = ", val)
    end
end

function table:keys()
    local a = {}
    for name,val in pairs(self) do
        table.insert(a, name)
    end
    return a
end

function table:values()
    local a = {}
    for name,val in pairs(self) do
        table.insert(a, val)
    end
    return a
end
