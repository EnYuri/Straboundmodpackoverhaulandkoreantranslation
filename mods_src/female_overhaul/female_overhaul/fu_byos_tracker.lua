require "/frackinship/scripts/quest/frackinship.lua"

-- FU completes fu_byos only after "bootship" is completed. If bootship was
-- declined or lost, fu_byos stays active forever and FU's gaterepair treats
-- the player as non-BYOS, overwriting the ship with the vanilla structure.
-- The ship world's "fu_byos" property is the real BYOS marker, so use it too.
local _update = update
function update(dt)
  if player.worldId() == player.ownShipWorldId() and world.getProperty("fu_byos") then
    quest.complete()
    return
  end
  _update(dt)
end
