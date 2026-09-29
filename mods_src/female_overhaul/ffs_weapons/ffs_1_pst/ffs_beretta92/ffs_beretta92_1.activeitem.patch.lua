-- RPG Growth and the FFS tag addon both add weapon categories.
-- Keep the first occurrence of each tag, including tags from other mods.
function patch(config)
  if config.itemTags then
    local seen, tags = {}, {}
    for _, tag in ipairs(config.itemTags) do
      if not seen[tag] then
        table.insert(tags, tag)
        seen[tag] = true
      end
    end
    config.itemTags = tags
  end
  return config
end
