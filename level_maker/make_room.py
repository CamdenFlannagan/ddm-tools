'''
# ----- BASICS ----- #
0x00 : air

0x14 : spike up
0x15 : spike down
0x16 : spike right
0x17 : spike left

# which sides of the metal tile are closed
0x18 : metal T /   / L /      
0x19 : metal T /   /   /      
0x1A : metal T /   /   / R
0x1B : metal   /   / L /      
0x1C : metal   /   /   / R
0x1D : metal   / B / L /      
0x1E : metal   / B /   /      
0x1F : metal   / B /   / R
0x20 : metal T / B / L /  
0x21 : metal T / B /   /  
0x22 : metal T / B /   / R
0x23 : metal T /   / L / R
0x24 : metal   /   / L / R
0x25 : metal   / B / L / R
0x26 : metal T / B / L / R

0x27 : rubble inside walls

0x28 : bush interior thick
0x29 : bush interior sparse
0x2A : grow vine up from here until it hits something
0x2B : bush corner up left
0x2C : bush edge up
0x2D : bush corner up right
0x2E : bush edge left
0x2F : bush edge right
0x30 : bush corner down left
0x31 : bush edge down
0x32 : bush corner down right

0x34 : temple skull left
0x35 : temple skull right
0x36 : temple left
0x37 : temple right

0x38 : platform wooden
0x39 : platform metal

# which corner is rounded: top-left, top-right, bottom-left, bottom-right
0x3A : slime __ / __ / __ / __
0x3B : slime TL / TR / __ / __
0x3C : slime __ / __ / BL / BR
0x3D : slime TL / __ / BL / __
0x3E : slime __ / TR / __ / BR
0x3F : slime TL / TR / BL / __
0x40 : slime TL / TR / __ / BR
0x41 : slime TL / __ / BL / BR
0x42 : slime __ / TR / BL / BR
0x43 : slime TL / __ / __ / __
0x44 : slime __ / TR / __ / __
0x45 : slime __ / __ / BL / __
0x46 : slime __ / __ / __ / BR

0x47 : background bricks
0x48 : background bricks
0x49 : background bricks
0x4C : background bricks
0x4D : background bricks
0x4E : background bricks

0x50 : gear
0x51 : rope

0x54 : statue top left
0x55 : statue top right
0x56 : statue bottom left
0x57 : statue bottom right

0x58 : box
0x59 : wood horizontal with hanging lamp
0x5A : wood vertical
0x5B : wood intersection/crossing
0x5C : wood horizontal
0x5D : minecart
0x5E : crystal

0x63 : save statue bottom left
0x64 : save statue bottom right
0x65 : arena tile

0x66 : skeleton head
0x67 : skeleton spine
0x68 : skeleton tail
0x6A : skeleton fin
0x6B : broken bone
0x6C : shell
0x6D : stalagtite top
0x6E : stalagtite bottom
0x6F : stalagtite long part thicker (often used just below/above the top/bottom)
0x70 : stalagtite long part
0x71 : oil lake
0x72 : oil barrel centered

0x73 : maybe background bricks

0x75 : big brick left end
0x76 : big brick right end
0x77 : big brick left end's left half
0x78 : big brick middle

0x7D : dirt T / B / L /  
0x7F : dirt T / B /   / R

0xB0 : oil barrel's left half
0xB1 : oil barrel's right half

0xB6 : grown vine up between this tile and the one to the right, also see vine 0xE1

0xB8 : metal blank interior

0xD5 : dirt (shapes calculated automatically)
0xD6 : grass (shapes calculated automatically)

0xD7 : column top
0xD8 : column middle
0xD9 : column bottom

0xDA : slime TL / TR / BL / BR

0xDB : number statue bottom left
0xDC : number statue bottom right

0xE1 : vine, I think 0xB6 vines need to have E1 where the right half of the vine hits the (dirt?) ceiling

0xE3 : wood vertical into ceiling

0xE4 : slime transition
0xE5 : slime transition in upper half
0xE6 : slime transition in lower half
'''

'''
Loaded in things

0x01 : makes you trip upon entering the screen
0x02 : spike flippy guy
0x03 : mouse
0x04 : save point, invisible until touched
0x05 : iron pick
0x06 : gold pick
0x07 : next pick
0x08 : next pick
0x09 : next pick
0x0A : spike ball
0x0B : heart
0x0C : key
0x0D : bounce shroom
0x0E : 3 locks from chest
0x0F : nothing?
0x10 : d.w.a.r.f.
0x11 : nothing?
0x12 : mole clone
0x13 : bomb
0x14 : nothing?
0x15 : mafia man
0x16 : map
0x17 : sparkles
0x18 : money bag, causes win
0x19 : nothing?
0x1A : white bounce shroom
0x1B : X symbol
0x1C : looks like nothing, golden save flame upon touch, does not save
0x1D : nothing?
0x1E : nothing?
0x1F : CRASH!
0x20 : CRASH!

'''