floor_touches = 0
already_grounded = false

restart = ""
pleaseRestart = false
noRestartSaveYet = true

ram = emu.memType.nesInternalRam

function rram(addr)
	return emu.read(addr, ram, false)
end

down_drill = "none"
death = "not_dying"
death_frames_left = 0

-- this should call just once around the beginning of each run
emu.addMemoryCallback(function()

	floor_touches = 0

end,
emu.callbackType.exec,
0xD46D, 0xD46D,
emu.cpuType.nes,
emu.memType.nesMemory)

emu.addMemoryCallback(function()

	if pleaseCreateSave == true then
		pleaseCreateSave = false
		restart = emu.createSavestate()
	end

	if pleaseRestart == true then
		pleaseRestart = false
		emu.loadSavestate(restart)
	end

end,
emu.callbackType.exec,
0x54dc, 0x54dc + 256,
emu.cpuType.nes,
emu.memType.nesPrgRom)

emu.addEventCallback(function()

	if death == "not_dying" then
		grounded = emu.read(0x580, ram, false) == 0x0E
		grounded = grounded or emu.read(0x580, ram, false) == 0x0F
		grounded = grounded and emu.read(0x570, ram, false) == 0x00
		
		if rram(0x590) == 0x0F then
			down_drill = "wind_up"
		end
		
		-- side-drill has interupted the down drill
		if down_drill == "wind_up" and (rram(0x570) == 0x04 or rram(0x570) == 0x05) then
			down_drill = "none"
		end
		
		if down_drill == "wind_up" and rram(0x590) == 0x00 then
			down_drill = "going_down"
		end
		
		if down_drill == "going_down" and (rram(0x580) == 0x0E or rram(0x580) == 0x0F or rram(0x570) == 0x07) then
			down_drill = "none"
			grounded = true
		end
		
		if grounded then
			if not already_grounded then
				floor_touches = floor_touches + 1
				already_grounded = true
			end
		else
			already_grounded = false
		end
		
		if floor_touches == 1 and noRestartSaveYet == true then
			pleaseCreateSave = true
			noRestartSaveYet = false
		end
		
		if floor_touches > 2 then
			death = "died"
			floor_touches = 1
		end
	end
	
	if death == "died" then
		death_frames_left = 10
		death = "dying"
	end
	
	if death == "dying" then
		death_frames_left = death_frames_left - 1
		if death_frames_left > 2 then
			emu.write(0x570, 0x06, emu.memType.nesInternalRam)
		end
		if death_frames_left <= 0 then
			death = "not_dying"
			pleaseRestart = true
		end
	end
	
	emu.drawString(0, 8, down_drill)
	emu.drawString(0, 0, floor_touches)

end,
emu.eventType.endFrame)