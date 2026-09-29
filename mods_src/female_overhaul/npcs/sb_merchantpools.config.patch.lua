-- Irisil's Betabound integration uses an obsolete array index.
function patch(config)
  for _,tier in ipairs(config.sb_cupidmerchant or {}) do
    for _,entry in ipairs(tier[2] or {}) do
      if entry.item and entry.item.name == "climbingrope" then
        entry.item.name = "lofty_irisil_redclimbingrope"
      end
    end
  end
  return config
end
