-- Applies audited late compatibility repairs while preserving current parent data.
local repairs = assets.json("/female_overhaul/remaining_repairs.config")["/positions/twoactors/missionary/missionary_in_bed.config"]
local function clone(v)
  if type(v) ~= "table" then return v end
  local out = {}; for k,x in pairs(v) do out[k]=clone(x) end; return out
end
local function same(a,b)
  if type(a)~=type(b) then return false end
  if type(a)~="table" then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k,v in pairs(b) do if not same(v,a[k]) then return false end end
  return true
end
local function parts(path)
  local out={}; for s in path:gmatch("[^/]+") do out[#out+1]=s:gsub("~1","/"):gsub("~0","~") end; return out
end
local function key(s) return tonumber(s) and tonumber(s)+1 or s end
local function at(data,path)
  for _,s in ipairs(parts(path)) do if type(data)~="table" then return nil end; data=data[key(s)] end
  return data
end
local function apply(data,ops)
  for _,op in ipairs(ops) do
    if not op.op then
      local trial=clone(data); local result=apply(trial,op); if result then data=result end
    else
      local seg=parts(op.path); local parent=data
      for i=1,#seg-1 do if type(parent)~="table" then return nil end; parent=parent[key(seg[i])] end
      if type(parent)~="table" then return nil end
      local last=seg[#seg]; local k=key(last); local old=parent[k]
      local textField=last=="description" or last=="shortdescription" or last=="text" or last=="completionText" or last:match("Description$")
      local keepTranslation=textField and type(old)=="string" and type(op.value)=="string" and old:match("[\128-\255]") and not op.value:match("[\128-\255]")
      if op.op=="test" then
        local valid=op.value==nil and old~=nil or op.value~=nil and same(old,op.value)
        if op.inverse then valid=not valid end
        if not valid then return nil end
      elseif op.op=="ensure" then
        if old==nil then parent[k]=clone(op.value) elseif type(old)~="table" then return nil end
      elseif op.op=="appendSpecies" then
        if parent[k]==nil then parent[k]={} end
        if type(parent[k])=="table" then
          local found=false; for _,v in ipairs(parent[k]) do if v==op.value then found=true end end
          if not found then table.insert(parent[k],op.value) end
        end
      elseif op.op=="add" and last=="-" then
        local found=false; for _,v in ipairs(parent) do if same(v,op.value) then found=true end end
        if not found then table.insert(parent,clone(op.value)) end
      elseif op.op=="add" then
        if type(k)=="number" then if k<1 or k>#parent+1 then return nil end; table.insert(parent,k,clone(op.value))
        else if not keepTranslation then parent[k]=clone(op.value) end end
      elseif op.op=="replace" then
        if old==nil then return nil end; if not keepTranslation then parent[k]=clone(op.value) end
      elseif op.op=="remove" then
        if old==nil then return nil end
        if type(k)=="number" then table.remove(parent,k) else parent[k]=nil end
      elseif op.op=="copy" then
        local value=at(data,op.from); if value==nil then return nil end; parent[k]=clone(value)
      else return nil end
    end
  end
  return data
end
function patch(config)
  for _,repair in ipairs(repairs) do
    if repair.kind=="encounter" then
      for _,item in ipairs((config.undergroundPlaceables or {}).items or {}) do
        if type(item.microdungeons)=="table" then
          local eligible=false; local found=false
          for _,name in ipairs(item.microdungeons) do
            if name=="undergroundencounterdungeons" then eligible=true end
            if name=="felinundergroundencounter" then found=true end
          end
          if eligible and not found then table.insert(item.microdungeons,"felinundergroundencounter") end
        end
      end
    else
      local trial=clone(config); local result=apply(trial,repair.operations)
      if result then config=result end
    end
  end
  return config
end
