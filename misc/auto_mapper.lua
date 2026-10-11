
done = false

WAIT = 40
wait_left = 0

NUM_ROOMS = 256
room = 0

callback = emu.addEventCallback(function()

	if wait_left == 0 then
		if room ~= 0x06 and room ~= 0xFE then
			emu.write(0x041, 0x01, emu.memType.nesInternalRam)
			emu.write(0x048, room, emu.memType.nesInternalRam)
		end
		
		room = room + 1
		
		wait_left = WAIT
	else
		wait_left = wait_left - 1
	end

	if room >= NUM_ROOMS then
		emu.removeEventCallback(callback, emu.eventType.startFrame)
	end
end, emu.eventType.startFrame)