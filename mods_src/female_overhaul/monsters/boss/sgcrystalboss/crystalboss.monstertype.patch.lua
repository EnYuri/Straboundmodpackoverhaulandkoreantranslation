-- Restores an obsolete compatibility target after all parent mods load.
function patch(config)
  if type(config["baseParameters"]["scripts"]) == "table" then
    local value = "/monsters/boss/bossMonster_bl3health.lua"
    local found = false
    for _, entry in ipairs(config["baseParameters"]["scripts"]) do
      if entry == value then found = true; break end
    end
    if not found then table.insert(config["baseParameters"]["scripts"], value) end
  end
  config["baseParameters"]["statusSettings"]["stats"]["fireStatusImmunity"]["baseValue"] = 0
  config["baseParameters"]["statusSettings"]["stats"]["iceStatusImmunity"]["baseValue"] = 0
  config["baseParameters"]["statusSettings"]["stats"]["electricStatusImmunity"]["baseValue"] = 0
  config["baseParameters"]["statusSettings"]["stats"]["poisonStatusImmunity"]["baseValue"] = 0
  config["baseParameters"]["statusSettings"]["stats"]["specialStatusImmunity"]["baseValue"] = 0
  config["baseParameters"]["statusSettings"]["stats"]["healingStatusImmunity"]["baseValue"] = 0
  return config
end
