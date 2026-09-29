-- The K'Rakoth FU addon loads before this rifle's base mod in this pack.
function patch(config)
  config.tooltipKind = "gun2"
  config.critChance = 3
  config.critBonus = 9
  config.itemTags = config.itemTags or {}
  local present = {}
  for _, tag in ipairs(config.itemTags) do present[tag] = true end
  for _, tag in ipairs({"energy", "assaultrifle", "upgradeableWeapon"}) do
    if not present[tag] then table.insert(config.itemTags, tag); present[tag] = true end
  end
  return config
end
