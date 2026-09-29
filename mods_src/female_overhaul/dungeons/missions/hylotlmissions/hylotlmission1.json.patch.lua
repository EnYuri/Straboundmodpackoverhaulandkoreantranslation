-- FU moves these stagehands. Find the existing radio trigger by message.
function patch(config)
  for _,layer in ipairs(config.layers or {}) do
    for _,object in ipairs(layer.objects or {}) do
      local properties=object.properties or {}
      local parameterProperty
      for _,p in ipairs(properties) do if p.name=="parameters" then parameterProperty=p end end
      local raw=parameterProperty and parameterProperty.value or properties.parameters
      if type(raw)=="string" then
        local ok,parameters=pcall(sb.parseJson,raw)
        if ok then
          local messages=parameters.radioMessages or (parameters.radioMessage and {parameters.radioMessage})
          local match,present=false,false
          for _,message in ipairs(messages or {}) do
            if message=="hylotlmission01" then match=true end
            if message=="black_hylotlmission01b" then present=true end
          end
          if match and not present then
            table.insert(messages,"black_hylotlmission01b")
            parameters.radioMessage=nil
            parameters.radioMessages=messages
            local updated=sb.printJson(parameters,0)
            if parameterProperty then parameterProperty.value=updated else properties.parameters=updated end
          end
        end
      end
    end
  end
  return config
end
