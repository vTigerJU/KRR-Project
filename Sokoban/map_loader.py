import os

LEVEL_DIR = "maps"

LEVEL_FILES  = [
    os.path.join(LEVEL_DIR, f)
    for f in os.listdir(LEVEL_DIR)
    if f.endswith(".txt")
]


def load_level_from_file(path):
    """
    load a sokoban level from a text file using classic sokoban symbols:

    supported characters:

    # = wall

    $ = box

    . = goal

    @ = player

    * = box on goal

    + = player on goal

    space = empty floor

    lines starting with 'Title' are ignored.

    """
    with open(path, "r") as f:
        raw_lines = [line.rstrip("\n") for line in f]

    #drop empty lines and "title: " lines

    lines = [ 
        line for line in raw_lines
        if line.strip() != "" and not line.strip().lower().startswith("title:")
    ]

    if not lines:
        raise ValueError(f"Level file {path} is empty or invalid.")

    height = len(lines)
    width = max(len(line) for line in lines)

    walls = set()
    goals = set()
    boxes = set()
    player = None

    for y, line in enumerate(lines, start = 0):
        # pad line on the right so all have same width
        padded = line.ljust(width)
        for x, ch in enumerate(padded, start= 0):
            if ch == "#":
                walls.add((x, y))
            elif ch == "$":
                boxes.add((x, y))
            elif ch == ".":
                goals.add((x, y))    
            elif ch == "@":
                player = (x, y)
            elif ch == "*":
                boxes.add((x, y))
                goals.add((x, y))
            elif ch == "+":
                player = (x, y)
                goals.add((x, y))

    if player is None:
        raise ValueError(f"No player '👑' found in level file {path}")

    level = {
        "name"   : os.path.basename(path),
        "width"  : width,
        "height" : height,
        "walls"  : walls,
        "goals"  : goals,
        "player" : player,
        "boxes"  : boxes,
    }
    return level

def build_asp_facts(level, player_pos, boxes):
    w = level["width"]
    h = level["height"]
    walls = level["walls"]
    goals = level["goals"]
    #boxtemp = level["boxes"]
    #playertemp = level["player"]

    lines = []
    lines.append(f"coordinate(X,Y) :- X=0..{w}, Y=0..{h}.")
    for (wx, wy) in sorted(walls):
        lines.append(f"wall({wx}, {wy}).")

    for (gx, gy) in sorted(goals):
        lines.append(f"isgoal({gx}, {gy}).")

    px, py = player_pos
    lines.append(f"player(p).")
    lines.append(f"on({px}, {py}, p ,0).")

    for i, (bx, by) in enumerate(boxes, start = 1):
        lines.append(f"crate(b{i}).")
        lines.append(f"on({bx}, {by}, b{i}, 0).")

    return "\n".join(lines)