-- ERM FU Meat Chunk patch incorrectly targets /fu_erm_fix/player.config.
-- Merge its unlock with the existing local blueprint patch, without duplicates.
function patch(config)
  config.defaultBlueprints = config.defaultBlueprints or {}
  config.defaultBlueprints.tier1 = config.defaultBlueprints.tier1 or {}
  for _,blueprint in ipairs(config.defaultBlueprints.tier1) do
    if blueprint.item == "avikanmeatchunk" then return config end
  end
  table.insert(config.defaultBlueprints.tier1, {item="avikanmeatchunk"})
  return config
end
