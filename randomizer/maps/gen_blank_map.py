
out = ""
for i in range(16):
    for j in range(15):
        out += "____,"
    out += "____"
    out += "\n"

with open("./maps/blank_map.csv", "w") as f:
    f.write(out)
