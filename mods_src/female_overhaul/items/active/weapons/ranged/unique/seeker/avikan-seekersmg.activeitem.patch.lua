-- Restores an obsolete compatibility target after all parent mods load.
function patch(config)
  if type(config["itemTags"]) == "table" then
    local value = "energy"
    local found = false
    for _, entry in ipairs(config["itemTags"]) do
      if entry == value then found = true; break end
    end
    if not found then table.insert(config["itemTags"], value) end
  end
  return config
end
