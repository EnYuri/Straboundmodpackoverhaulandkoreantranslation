-- Select the original chest IDs; FU changed Tiled property format and indices.
function patch(config)
  local ids = {[723]=true}
  for _,layer in ipairs(config.layers or {}) do
    for _,object in ipairs(layer.objects or {}) do
      if ids[object.id] then
        local properties = object.properties or {}
        if properties[1] or next(properties) == nil then
          local found = false
          for _,property in ipairs(properties) do
            if property.name == "parameters" then found = true end
          end
          if not found then table.insert(properties, {name="parameters", type="string", value='{"treasurePools":["basicTreasure"]}'}) end
        elseif not properties.parameters then
          properties.parameters = '{"treasurePools":["basicTreasure"]}'
        end
        object.properties = properties
      end
    end
  end
  return config
end
