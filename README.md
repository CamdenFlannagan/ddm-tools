# Diggy Diggy Mole Randomizer!

You'll need the latest version of the Mesen emulator to play the randomizer.

In Mesen, run Diggy Diggy Mole, open and run the script ddm_randomizer.lua, and restart the game. Now your world should be scrambled.

How to make your own map:
Sort of like Minecraft, you can give the randomizer a seed. Run the python script with the seed of your choosing using command line arguments to regenerate the map and update the ddm_randomizer.lua script. Run the script like this. You can pick the seed and which room on the random map you want to start on:

py randomizer.py --seed 16 --start 0x23

The seed and start will default to 16 and 0x88 if you don't provide them yourself.

You can also go into ddm_randomizer.lua and create your own custom, intentional arrangement of Diggy Diggy Mole's screens by altering the scramble table yourself

# The Floor is Lava!

Run this script and restart the game. Now the game will behave just like Super Mario Maker 2's "Once you leave the ground you may not touch the ground again."

This will force you to do a lot of ceiling movement, which is pretty cool. 

I don't think the game is beatable like this, unfortunately, but you can make your own challenges using the randomizer script and a custom arrangement of screens.
