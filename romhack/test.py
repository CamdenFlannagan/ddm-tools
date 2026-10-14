from dataclasses import dataclass

@dataclass
class Quad():
    y: int
    x: int

def yx_to_hex(yx: tuple[int, int]) -> int:
    assert yx[0] < 16, yx
    assert yx[1] < 16, yx
    return (yx[0] << 4) + yx[1]

def quad_to_rooms(quad: Quad) -> list[int]:
    return [
        (2*(quad.y - 1), 2*quad.x),
        yx_to_hex((2*(quad.y - 1), 2*quad.x + 1)),
        yx_to_hex((2*(quad.y - 1) + 1, 2*quad.x)),
        yx_to_hex((2*(quad.y - 1) + 1, 2*quad.x + 1)),
    ]

print(quad_to_rooms(Quad(3, 4)))

print(yx_to_hex((4, 8)))