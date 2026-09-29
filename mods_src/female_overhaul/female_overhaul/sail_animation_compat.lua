-- NonEKI's global animation templates are valid only for its own portrait.
-- FU's selector changes imagePath, so switch templates with that image too.
local originalAnimations
local lastImage
local function syncSailAnimations()
  if not GUI or not GUI.talker then return end
  local image = (customData and customData.aiFrames) or GUI.talker.imagePath
  if not image or image == "" or image == lastImage then return end
  originalAnimations = originalAnimations or GUI.talker.animations
  if image:lower():find("noneki.png", 1, true) then
    GUI.talker.animations = originalAnimations
  else
    GUI.talker.animations = root.assetJson("/female_overhaul/sail_animations.config")
  end
  GUI.talker.frame = 0
  GUI.talker.frameTimer = 0
  lastImage = image
end

local previousLoad = loadFrackinShipSail
function loadFrackinShipSail(race)
  previousLoad(race)
  syncSailAnimations()
end

local previousUpdate = update
function update(dt)
  syncSailAnimations()
  previousUpdate(dt)
end
