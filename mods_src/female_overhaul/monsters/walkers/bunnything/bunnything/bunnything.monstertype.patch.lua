-- Restores an obsolete compatibility target after all parent mods load.
function patch(config)
  if type(config["baseParameters"]["scripts"]) == "table" then
    local value = "/monsters/ivrpgmonster.lua"
    local found = false
    for _, entry in ipairs(config["baseParameters"]["scripts"]) do
      if entry == value then found = true; break end
    end
    if not found then table.insert(config["baseParameters"]["scripts"], value) end
  end
  return config
end
