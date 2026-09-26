require "/scripts/util.lua"
require "/scripts/vec2.lua"
require "/scripts/rect.lua"

require "/interface/scripts/main_tab.lua"
require "/interface/scripts/dyes_tab.lua"
require "/interface/scripts/tiles_tab.lua"
require "/interface/scripts/MM_tab.lua"
require "/interface/scripts/monsters_tab.lua"
require "/interface/scripts/guns_tab.lua"
require "/interface/scripts/player_tab.lua"
require "/interface/scripts/credits_tab.lua"

defaultOptions = {} 
playerOptions = {}
defaultIconArray = {}
rainbowColours = { "ff8080", "ff9c74", "ffbc6c", "ffdd6e", "ffff80", "e6ff7a", "c9ff77", "a8ff79", "80ff80", "61ffac", "52ffd0", "5fffed", "80ffff", "00e7ff", "00cbff", "08aaff", "8080ff", "a481ff", "c581ff", "e380ff", "ff80ff", "ff77d9", "ff74b6", "ff7998" }
--status.setStatusProperty("dyeSuite", internalDyeData)

function init()
	self.titleName = " Green's Dye Suite"
	self.title = self.titleName

	loadOptions()

	resetTooltips()

	self.canvas = widget.bindCanvas("scriptCanvas")
	self.messageFadeTimer = 5
	widget.focus("scriptCanvas")

	tabCount = 8
	self.repeats = 0
	self.tooltips = {}
	self.tabTooltips = {}
	self.miscTooltips = {}
	self.miscTooltips2 = {}
	self.miscTooltips3 = {}
	--widget.setSelectedOption("mainTabs", -1)

	safeScriptCheck()
	changeMainTab()
	resetTooltips()
	--pane.setTitle(self.title, "^#b9b5b2; < insert dye pun here >")
	
	--message.setHandler("terminateUI", function(_, _) pane.dismiss() end)
end

function update(dt)

	if player.isAdmin() then

	end

	self.messageFadeTimer = math.max(0, self.messageFadeTimer - dt)

	if self.messageFadeTimer < 2 then
		local color = {255, 245, 235, math.floor(math.min(1, self.messageFadeTimer) * 255)}
		widget.setFontColor("messageOutput", color)
	else
		local color = {
			215 + math.floor(40 * math.sin(os.clock() * 50)),
			215 + math.floor(40 * math.sin(os.clock() * 50)),
			64 + math.floor(math.min(1 - math.max(0, self.messageFadeTimer - 4), 1) * 171),
			255
		}
		widget.setFontColor("messageOutput", color)
	end


	if world.entityExists(player.id()) then
		if widget.getSelectedData("mainTabs") == "tabMain" then
			main.update(dt)

		elseif widget.getSelectedData("mainTabs") == "tabDyes" then
			dyes.update(dt)
		end
	end
end

function uninit()
	dyes.uninit()

	local itemDye = widget.itemSlotItem("dyesPage_layout.paletteImporterLayout.itemSlot")
	if itemDye then player.giveItem(itemDye) end
	local itemTile = widget.itemSlotItem("tilesPage_layout.itemSlot")
	if itemTile then player.giveItem(itemTile) end

	for i = 1, 24, 1 do
		local itm = widget.itemSlotItem("dyesPage_layout.paletteFusionLayout.dyeSlot" .. i)
		if itm then player.giveItem(itm) end
	end
	for i = 1, 2, 1 do
		local itm = widget.itemSlotItem("dyesPage_layout.paletteMergerLayout.dyeSlot" .. i)
		if itm then player.giveItem(itm) end
	end
	for i = 1, 5, 1 do
		local itm = widget.itemSlotItem("dyesPage_layout.MMDyeLayout.dyeSlot" .. i)
		if itm then player.giveItem(itm) end
	end
end


-- Main Functions --
function changeMainTab()
	local mainTab = widget.getSelectedData("mainTabs") or 2
	widget.playSound("/sfx/objects/console_button2.ogg")
	hideTabContent()

	if mainTab == "tabMain" then
		toggleTab(1, true)
		main.init()

	elseif mainTab == "tabDyes" then
		toggleTab(2, true)
		dyes.init()

	elseif mainTab == "tabTiles" then
		toggleTab(3, true)
		tiles.init()

	elseif mainTab == "tabMM" then
		toggleTab(4, true)
		MM.init()

	elseif mainTab == "tabMonsters" then
		toggleTab(5, true)
		monsters.init()

	elseif mainTab == "tabGuns" then
		toggleTab(6, true)
		guns.init()

	elseif mainTab == "tabPlayer" then
		toggleTab(7, true)
		players.init()

	elseif mainTab == "tabCredits" then
		toggleTab(8, true)
		widget.playSound("/sfx/humanoid/human_chatter_male2.ogg")
		credits.init()
	end
end

function toggleTab(tab, visible)
	if tab == 1 then
		widget.setText("tabsTitle", "Options")
		widget.setVisible("mainPage_layout", visible)
		if not visible then main.uninit() end

	elseif tab == 2 then
		widget.setText("tabsTitle", "Dye Creation")
		widget.setVisible("dyesPage_layout", visible)
		if not visible then dyes.uninit() end

	elseif tab == 3 then
		widget.setText("tabsTitle", "Tile Editor")
		widget.setVisible("tilesPage_layout", visible)
		if not visible then tiles.uninit() end

	elseif tab == 4 then
		widget.setText("tabsTitle", "Matter Manipulator Configuration")

	elseif tab == 5 then
		widget.setText("tabsTitle", "Monster Creation")

	elseif tab == 6 then
		widget.setText("tabsTitle", "Gun Modification")

	elseif tab == 7 then
		widget.setText("tabsTitle", "Character Editor")

	elseif tab == 8 then
		widget.setText("tabsTitle", "Credits")
		widget.setVisible("creditsPage_layout", visible)
		if not visible then credits.uninit() end
	end
end

function safeScriptCheck()
	storageDirectory = status.statusProperty("storageDirectory")
	if storageDirectory ~= nil and io then
		if io.open(storageDirectory .. "/starbound.config", "r") ~= nil then
			self.title = self.titleName .. " - Safe Scripts Off"
			--widget.setOptionVisible("mainTabs", 2, true)
		else
			--widget.setOptionVisible("mainTabs", 2, false)
		end
	end
end

function optionsTab()
	--widget.playSound("/sfx/interface/clickon_error.ogg")
	hideTabContent()
	toggleTab(1, true)
	main.init()
	widget.setSelectedOption("mainTabs", -1)

	--[[
		self.repeats = self.repeats + 1

		if self.repeats == 20 then
			local ents = world.playerQuery(world.entityPosition(player.id()), 50)
			for i = 1", "ents, 1 do
				if ents[i] ~= nil then
					world.sendEntityMessage(ents[i], "setMechItemSet", {}, true)
				end
			end
			showMessage("Mechs cleared.")
		end
	]]
end

function loadOptions()
	defaultOptions = root.assetJson("/defaultOptions.config")
	playerOptions = status.statusProperty("dyeSuiteOptions") or defaultOptions
	defaultIconArray = config.getParameter("iconList", {})
	sb.logError("[Dye Suite] Internal Options are " .. ((status.statusProperty("dyeSuiteOptions") ~= nil) and "existing." or "non-existant."))
	sb.logError("[Dye Suite] Internal Options are loaded as: " .. sb.printJson(playerOptions))

	if playerOptions.enableGeneratedDyes == nil then playerOptions.enableGeneratedDyes = defaultOptions.enableGeneratedDyes end
	if playerOptions.enableUltraPack == nil then playerOptions.enableUltraPack = defaultOptions.enableUltraPack end
	if playerOptions.enableDefaultDyes == nil then playerOptions.enableDefaultDyes = defaultOptions.enableDefaultDyes end
	if playerOptions.enableNumbers == nil then playerOptions.enableNumbers = defaultOptions.enableNumbers end
	if playerOptions.enableTooltips == nil then playerOptions.enableTooltips = defaultOptions.enableTooltips end
	if playerOptions.enableVerboseTooltips == nil then playerOptions.enableVerboseTooltips = defaultOptions.enableVerboseTooltips end

	if playerOptions.categoryBlacklist == nil then playerOptions.categoryBlacklist = defaultOptions.categoryBlacklist end
	if playerOptions.dyeLimit == nil then playerOptions.dyeLimit = defaultOptions.dyeLimit end
	if playerOptions.mainDyeIcon == nil then playerOptions.mainDyeIcon = defaultOptions.mainDyeIcon end
	if playerOptions.generatedDyeIcon == nil then playerOptions.generatedDyeIcon = defaultOptions.generatedDyeIcon end

	--status.setStatusProperty("dyeSuiteOptions", playerOptions)
end

function hideTabContent()
	for tab = 1, tabCount do
		toggleTab(tab, false)
	end
end

function getPlayerProperty(name)
	return status.statusProperty(name)
end

function setPlayerProperty(name, value)
	status.setStatusProperty(name, value)
end

function showMessage(text, time)
	self.messageFadeTimer = time or 5
	widget.setText("messageOutput", text)
end


-- Canvas Events --
--[[
function canvasClickEvent(position, button, isButtonDown)
	local pos = position

	if isButtonDown then -- Mouse Down
		if button == 0 then -- Left MB
			widget.playSound("/sfx/gun/grenadeblast1.ogg")

		elseif button == 1 then -- Middle MB
			widget.playSound("/sfx/gun/grenadeblast1.ogg")

		elseif button == 2 then -- Right MB
			widget.playSound("/sfx/gun/grenadeblast1.ogg")

		else

		end
	end
end

function canvasKeyEvent(key, isKeyDown)
	if isKeyDown then
		if key == 5 or key == 3 then -- space bar or enter

		elseif key == 46 or key == 89 then -- D or right arrow

		elseif key == 43 or key == 90 then -- A or left arrow

		end
	end
end
]]

function itemSlotInteractLeft(slot, disallowInsert, slotMax)
	if player.swapSlotItem() then
		if widget.itemSlotItem(slot) then
			local item = player.swapSlotItem()
			local maxStack = slotMax or item.parameters.maxStack or root.itemConfig(item.name).config.maxStack or root.assetJson("/items/defaultParameters.config:defaultMaxStack")
			local widgetItem = widget.itemSlotItem(slot)
			local maxStackHeld = item.parameters.maxStack or root.itemConfig(item.name).config.maxStack or root.assetJson("/items/defaultParameters.config:defaultMaxStack")

			if root.itemDescriptorsMatch(item, widgetItem, true) then
				if not (item.count + widgetItem.count > maxStack) then
					if disallowInsert then 
						if maxStackHeld < (item.count + widgetItem.count) then
							local take = (item.count + widgetItem.count) - maxStackHeld
							item.count = item.count + take
							widgetItem.count = widgetItem.count - take
							widget.setItemSlotItem(slot, widgetItem)
							player.setSwapSlotItem(item)
						else
							item.count = item.count + widgetItem.count
							widget.setItemSlotItem(slot, nil)
							player.setSwapSlotItem(item)
						end
					else
						widgetItem.count = widgetItem.count + item.count
						widget.setItemSlotItem(slot, widgetItem)
						player.setSwapSlotItem(nil)
					end
				else
					if disallowInsert then 

					else
						if widgetItem.count == maxStack or item.count == maxStackHeld then
							if item.count > maxStack then
								local take = math.min(maxStack - widgetItem.count, item.count)
								if take > 0 then
									player.giveItem(widgetItem)
									widget.setItemSlotItem(slot, { count = take, name = item.name, parameters = item.parameters })
									item.count = item.count - maxStack
									player.setSwapSlotItem(item)
								end
							else
								widget.setItemSlotItem(slot, player.swapSlotItem())
								player.setSwapSlotItem(widgetItem)
							end
						else
							item.count = item.count - (maxStack - widgetItem.count)
							widgetItem.count = maxStack
							widget.setItemSlotItem(slot, widgetItem)
							player.setSwapSlotItem(item)
						end
					end
				end
			else
				if disallowInsert then 

				else
					if item.count > maxStack then
						local take = math.min(maxStack, item.count)
						player.giveItem(widgetItem)
						widget.setItemSlotItem(slot, { count = take, name = item.name, parameters = item.parameters })
						item.count = item.count - maxStack
						player.setSwapSlotItem(item)
					else
						widget.setItemSlotItem(slot, player.swapSlotItem())
						player.setSwapSlotItem(widgetItem)
					end
				end
			end
		else
			if disallowInsert then return end
			local item = player.swapSlotItem()
			local maxStack = slotMax or item.parameters.maxStack or root.itemConfig(item.name).config.maxStack or root.assetJson("/items/defaultParameters.config:defaultMaxStack")
			local take = math.min(maxStack, item.count)
			item.count = item.count - take
			widget.setItemSlotItem(slot, { count = take, name = item.name, parameters = item.parameters })
			player.setSwapSlotItem(item)
		end
	elseif widget.itemSlotItem(slot) then
		if disallowInsert then
			if player.swapSlotItem() then
				player.giveItem(widget.itemSlotItem(slot))
			else
				player.setSwapSlotItem(widget.itemSlotItem(slot))
			end
		else
			player.setSwapSlotItem(widget.itemSlotItem(slot))
			widget.setItemSlotItem(slot, nil)
		end
	end
end

function itemSlotInteractRight(slot, disallowInsert, slotMax)
	if widget.itemSlotItem(slot) then
		local item = player.swapSlotItem()
		local widgetItem = widget.itemSlotItem(slot)
		local maxStack = slotMax or widgetItem.parameters.maxStack or root.itemConfig(widgetItem.name).config.maxStack or root.assetJson("/items/defaultParameters.config:defaultMaxStack")
		local maxStackHeld = 1
		if item then maxStackHeld = item.parameters.maxStack or root.itemConfig(item.name).config.maxStack or root.assetJson("/items/defaultParameters.config:defaultMaxStack") end

		if item and root.itemDescriptorsMatch(item, widgetItem, true) then
			if not (item.count >= maxStackHeld) then
				widget.setItemSlotItem(slot, { count = widgetItem.count - 1, name = widgetItem.name, parameters = widgetItem.parameters })
				item.count = item.count + 1
				player.setSwapSlotItem(item)
			end
		elseif not item then
			widget.setItemSlotItem(slot, { count = widgetItem.count - 1, name = widgetItem.name, parameters = widgetItem.parameters })
			player.setSwapSlotItem({ count = 1, name = widgetItem.name, parameters = widgetItem.parameters })
		elseif not root.itemDescriptorsMatch(item, widgetItem, true) then
			player.giveItem(widgetItem)
			widget.setItemSlotItem(slot, nil)
		end
		if widget.itemSlotItem(slot) then
			if widget.itemSlotItem(slot).count < 1 then
				widget.setItemSlotItem(slot, nil)
			end
		end
	else
		if not disallowInsert then
			local item = player.swapSlotItem()
			if item then
				local widgetItem = widget.itemSlotItem(slot)
				local maxStack = slotMax or widgetItem.parameters.maxStack or root.itemConfig(widgetItem.name).config.maxStack or root.assetJson("/items/defaultParameters.config:defaultMaxStack")

				widget.setItemSlotItem(slot, { count = 1, name = item.name, parameters = item.parameters })
				item.count = item.count - 1
				player.setSwapSlotItem(item)
			end
		end
	end
end

function itemSlotCopyIn(w)
	local swapItem = player.swapSlotItem()
	if swapItem ~= nil then
		setItemSlotItem(w, swapItem)
	end
end

function itemSlotCopyOut(w)
	local slotItem = widget.itemSlotItem(w)
	if slotItem ~= nil then
		player.setSwapSlotItem(slotItem)
	end
end

function setItemSlotItem(w, item, params)
	if not w then
		return false
	end

	if not item then 
		widget.setItemSlotItem(w, nil)
		return 
	end

	if type(item) == "string" then
		item = {name = item, parameters = params}
	end

	widget.setItemSlotItem(w, item)
end

function resetTooltips()
	self.tooltips = config.getParameter("tooltipData")["all"] or {}
	self.tooltips = sb.jsonMerge(self.tooltips, self.tabTooltips)
	self.tooltips = sb.jsonMerge(self.tooltips, self.miscTooltips)
	self.tooltips = sb.jsonMerge(self.tooltips, self.miscTooltips2)
	self.tooltips = sb.jsonMerge(self.tooltips, self.miscTooltips3)
end

function createTooltip(screenPosition)
	if playerOptions.enableTooltips then
		for widgetName, tooltipData in pairs(self.tooltips) do
			if widget.inMember(widgetName, screenPosition) then
				if nestedActiveCheck(widgetName) then
					local tooltip = config.getParameter("tooltipLayout")
					local vertOffset = root.imageSize(tooltip.bg.fileBody)[2]
					if tooltipData.description == nil then tooltipData.description = "" end
					local descCopy = tooltipData.description
					
					if tooltipData.isPalette then
						tooltip.title.value = rainbowifyText(tooltipData.name)
						local vertOffsetText = 0
						if playerOptions.enableVerboseTooltips then
							tooltip.description.value = "" .. tooltipData.description
							tooltip.columnL.value = "" .. tooltipData.columnL
							tooltip.columnM.value = "" .. tooltipData.columnM
							tooltip.columnR.value = "" .. tooltipData.columnR
							vertOffsetText = math.floor(tooltipData.stack * 10.4)
						end
						local rawDesc = clearTextEffects(string.gsub(tooltip.description.value or "", "«", "-"))
						
						--local extraLines = countSubstring(tooltipData.description, "\n") + math.ceil(math.max(rawDesc:len(), 0) / 30)
						--sb.logInfo("Text: " .. rawDesc .. " Stack: " .. tooltipData.stack .. " Len: " .. rawDesc:len())

						tooltip.background.size = { 134, 18 + vertOffsetText }
						local toolTipSize = tooltip.background.size
						tooltip.bg.fileBody = "/interface/images/all/tooltipBacking.png?scale;" .. toolTipSize[1] .. ";" .. toolTipSize[2] .. ";"

						tooltip.title.position = vec2.add(tooltip.title.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.titleBack.position = vec2.add(tooltip.titleBack.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.description.position = vec2.add(tooltip.description.position, {67, vertOffset + vertOffsetText - 11})

						tooltip.columnL.position = vec2.add(tooltip.columnL.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.columnM.position = vec2.add(tooltip.columnM.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.columnR.position = vec2.add(tooltip.columnR.position, {0, vertOffset + vertOffsetText - 11})

						tooltip.description.hAnchor = "mid"
						tooltip.background.position = vec2.add(tooltip.background.position, {0, vertOffset - 1})
						
						tooltip.background.stretchSet.begin = "/interface/images/dye/tooltipStartVertical.png" .. tooltipData.directives
						tooltip.background.stretchSet.inner = "/interface/images/dye/tooltipMidVertical.png" .. tooltipData.directives
						tooltip.background.stretchSet["end"] 	= "/interface/images/dye/tooltipEndVertical.png" .. tooltipData.directives

					else
						tooltip.title.value = rainbowifyText(tooltipData.name)
						if playerOptions.enableVerboseTooltips then
							tooltip.description.value = "^gray;" .. tooltipData.description
						end
						local rawDesc = clearTextEffects(string.gsub(tooltip.description.value or "", "«", "-"))
						local extraLines = countSubstring(descCopy, "\n") + (math.ceil(math.max(rawDesc:len(), 0) / 28))
						local vertOffsetText = math.floor(extraLines * 10.4)
						--local extraLines = countSubstring(tooltipData.description, "\n") + math.ceil(math.max(rawDesc:len(), 0) / 29)
						--sb.logInfo("Text: " .. rawDesc .. " ELines: " .. extraLines .. " Len: " .. rawDesc:len())

						tooltip.background.size = { 134, 18 + vertOffsetText }
						local toolTipSize = tooltip.background.size
						tooltip.bg.fileBody = "/interface/images/all/tooltipBacking.png?scale;" .. toolTipSize[1] .. ";" .. toolTipSize[2] .. ";"

						tooltip.title.position = vec2.add(tooltip.title.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.titleBack.position = vec2.add(tooltip.titleBack.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.description.position = vec2.add(tooltip.description.position, {0, vertOffset + vertOffsetText - 11})
						tooltip.background.position = vec2.add(tooltip.background.position, {0, vertOffset - 1})
					end
					
					return tooltip
				end
			end
		end
	end
end

function nestedActiveCheck(widgetName)
	local lineage = split(widgetName, ".")
	local totalString = ""

	for i = 1, #lineage do
		totalString = totalString .. lineage[i]
		if not widget.active(totalString) then
			--sb.logInfo("[Dye Suite] \"" .. totalString .. "\" is inactive.")
			return false
		end
		totalString = totalString .. "."
	end
	--sb.logInfo("[Dye Suite] \"" .. totalString .. "\" is active.")
	return true
end

function split(inputstr, sep)
	if sep == nil then sep = "%s" end
	local t = {}
	for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do table.insert(t, str) end
	return t
end

function rainbowifyText(text)
	local newtext = ""
	local txt = clearTextEffects(text)
	local i = 0
	for ch in string.gmatch(txt, "[ -Â-ý][-¿]*") do
		i = i + 1
		newtext = newtext .. "^#" .. rainbowColours[(math.floor(os.time() + i - 1) % #rainbowColours) + 1] .. ";" .. ch
	end
	newtext = "^shadow;" .. newtext
	return newtext
end

function gradifyText(text, col, col2)
	local newtext = ""
	local txt = clearTextEffects(text)
	local chars = {}
	for ch in string.gmatch(txt, "[ -Â-ý][-¿]*") do chars[#chars + 1] = ch end
	for i, ch in ipairs(chars) do
		newtext = newtext .. "^#" .. dyes.blendColours(col, col2, i / #chars) .. ";" .. ch
	end
	newtext = "^shadow;" .. newtext
	return newtext
end

function countSubstring(s1, s2)
	return select(2, string.gsub(s1, s2, ""))
end

function clearTextEffects(str)
	return string.gsub(str, "%b^;", "")
end

function round(num) return math.floor(num+.5) end

function table.removeKey(t, k)
	local i = 0
	local keys, values = {},{}
	for k,v in pairs(t) do
		i = i + 1
		keys[i] = k
		values[i] = v
	end
 
	while i>0 do
		if keys[i] == k then
			table.remove(keys, i)
			table.remove(values, i)
			break
		end
		i = i - 1
	end
 
	local a = {}
	for i = 1,#keys do
		a[keys[i]] = values[i]
	end
 
	return a
end