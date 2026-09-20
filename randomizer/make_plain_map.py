
map = [ i for i in range(256) ]

out = ""
for i in range(16):
    for j in range(15):
        out += hex(map[i*16 + j]).upper()
        out += ","
    out += hex(map[i*16 + 15]).upper()
    out += "\n"

with open("map.csv", "w") as f:
    f.write(out)
