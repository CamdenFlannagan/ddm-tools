# --------------------------------------------- #
# CPU Memory Constants
# --------------------------------------------- #
CPU_MEM_OFFSET        = -0x7FF0 # address in cpu memory + CPU_MEM_OFFSET = where in rom file is data

IRON_TEXT             =  0xc240
IRON_TEXT_LEN         =  0x3d

GOLD_TEXT             =  0xc27d
GOLD_TEXT_LEN         =  0x3e

JADE_TEXT             =  0xc2bb
JADE_TEXT_LEN         =  0x3c

OPAL_TEXT             =  0xc2f7
OPAL_TEXT_LEN         =  0x3c

RUBY_TEXT             =  0xc333
RUBY_TEXT_LEN         =  0x3d

OPENING_SCROLL_TEXT   =  0xc611
OPENING_SCROLL_TEXT_LEN \
                      =  0x159

CHEST_ROOM_LOCATION   =  0xcb38

# MAP_CHEST_POSITION is 0xdfbe
MAP_CHEST_TILE        =  0xdfa5
# MAP_CHEST_ORIENTATION_AND_COLOR is 0xdfcb

# MAP_BOMB_POSITION is 0xdfa1
MAP_BOMB_TILE         =  0xdfc2
# MAP_BOMB_ORIENTATION_AND_COLOR is 0xdfa9

# MAP_DOTS_POSITIONS starts 0xf20a, 9 bytes for 9 positions
MAP_DOTS_TILE         =  0xdfe0
# MAP_DOTS_ORIENTATION_AND_COLOR is 0xdfef

ROOM_ADDR_LOWER       =  0xf213
ROOM_ADDR_UPPER       =  0xf313
ROOM_ZONE             =  0xf413

MAP_TILE_DATA         =  0xf513
MAP_TILE_DATA_LEN     =  0x100

MAP_PALLETE_DATA      =  0xf613
MAP_PALLETE_DATA_LEN  =  0x14

# --------------------------------------------- #
# PRG ROM Constants
# --------------------------------------------- #
PRG_ROM_OFFSET  =  0x0010

ROOM_DATA_START =  0x9426
EMPTY_ROOM      =  ROOM_DATA_START