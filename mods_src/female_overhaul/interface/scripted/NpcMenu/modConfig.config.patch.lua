local additions = {"crewmemberguardian_nw","crewmembermagicalgirl_nw","crewmemberarctic_nw","crewmemberbiohazard_nw","crewmemberbountyhunter_nw","crewmemberfubees_nw","crewmemberfuhunter_nw","crewmembergas_nw","crewmembergeologist_nw","crewmemberhobo_nw","crewmembermechanic2_nw","crewmembermetalhead_nw","crewmemberradien_nw","crewmemberscience_nw","crewmembersciencedrug_nw","crewmembersciencegas_nw","crewmemberscuba_nw","crewmembershadow_nw","crewmemberstealth_nw","crewmembervolcanologist_nw","crewmemberengineer2_nw"}
function patch(config)
  local list = config.init and config.init.npcTypeList
  if type(list) ~= "table" then return config end
  local present = {}
  for _, name in ipairs(list) do present[name] = true end
  for _, name in ipairs(additions) do
    if not present[name] then table.insert(list, 1, name); present[name] = true end
  end
  return config
end
