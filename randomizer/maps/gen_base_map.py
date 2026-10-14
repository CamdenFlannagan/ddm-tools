
def hex_str(x):
    return format(x, '#04x').upper()

map = [ i for i in range(256) ]

out = ""
for i in range(16):
    for j in range(15):
        out += hex_str(map[i*16 + j])
        out += ","
    out += hex_str(map[i*16 + 15])
    out += "\n"

with open("./maps/base_map.csv", "w") as f:
    f.write(out)
