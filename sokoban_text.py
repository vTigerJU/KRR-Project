# final Mini-Project : Group 3
# written By: Axel Lindh - Hannan Khalil - Emil Anderö - Viktor Tiger 

# Sokoban with ASP-Based Hint System

import subprocess
import tempfile
import os
import sys
from collections import Counter



ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_LP_FILE = os.path.join(ROOT, "sokoban_base.lp")
LEVEL_DIR = os.path.join(ROOT, "maps")


MAX_PUSHES_PER_BOX = 5


def list_level_files(level_dir: str):
    if not os.path.isdir(level_dir):
        raise FileNotFoundError(f"Missing levels folder: {level_dir}")
    files = [os.path.join(level_dir, f) for f in os.listdir (level_dir) if f.endswith(".txt")]
    files.sort()

    if not files:
        raise FileNotFoundError(f"No .txt levels found in: {level_dir}")
    return files


LEVEL_FILES = list_level_files(LEVEL_DIR)


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
    Empty lines are ignored.
    """
 
   

    with open(path, "r", encoding= "utf-8") as f:
        raw_lines = [line.rstrip("\n") for line in f]



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
    boxes = []
    player = None

    for y, line in enumerate(lines, start = 1):
        # pad line on the right so all have same width

        padded = line.ljust(width)
        for x, ch in enumerate(padded, start= 1):
            if ch == "#":
                walls.add((x, y))
            elif ch == "$":
                boxes.append((x, y))
            elif ch == ".":
                goals.add((x, y))    
            elif ch == "@":
                player = (x, y)
            elif ch == "*":
                boxes.append((x, y))
                goals.add((x, y))
            elif ch == "+":
                player = (x, y)
                goals.add((x, y))
            

    if player is None:
        raise ValueError(f"No player '@' found in level file {path}")

    return  {

        "name"   : os.path.basename(path),
        "width"  : width,
        "height" : height,
        "walls"  : walls,
        "goals"  : goals,
        "player" : player,
        "boxes"  : boxes,
    }
    

# ------ASP interface-----

def build_asp_facts(level, player_pos, box_positions_by_id, pushes_left_by_id):
    w = level["width"]
    h = level["height"]
   

    lines = []
    lines.append (f"x(1..{w}).")
    lines.append (f"y(1..{h}).")

    for (wx, wy) in sorted(level["walls"]):
        lines.append(f"wall({wx}, {wy}).")

    for (gx, gy) in sorted(level["goals"]):
        lines.append(f"goal({gx}, {gy}).")

    px, py = player_pos
    lines.append(f"player({px}, {py}, 0).")

    for bid in sorted(box_positions_by_id.keys()):
        bx, by = box_positions_by_id[bid]
        lines.append(f"box({bid}, {bx}, {by}, 0).")
        n = pushes_left_by_id.get(bid, MAX_PUSHES_PER_BOX)
        lines.append(f"push_left({bid}, {n}, 0).")

    return "\n".join(lines)

def ask_hint(level, player_pos, box_positions_by_id, pushes_left_by_id):
    """
         return: 
        - direction string ('up', 'down', 'left', 'right') or
        - None if unsatisfiable or error.
    """

    if not os.path.exists(BASE_LP_FILE):
        return None
    
    asp_facts = build_asp_facts(level, player_pos, box_positions_by_id, pushes_left_by_id)
    
    with tempfile.NamedTemporaryFile(mode = "w", suffix = ".lp", delete = False, encoding= "utf-8") as tmp:
        tmp.write(asp_facts)
        tmp_path = tmp.name

    try:
        cmd = ["clingo", BASE_LP_FILE, tmp_path, "--quiet=1", "--opt-mode=optN", "-n", "1"]
        result = subprocess.run(cmd, capture_output = True, text = True, timeout = 60 )
        output = (result.stdout or "") + "\n" + (result.stderr or "")

        if "UNSATISFIABLE" in output:
            return None
        
        tokens = output.split()
        for t in tokens:
            if t.startswith("move(") and t.endswith(")"): 
                inside = t[t.find ("(") + 1 : t.find(")")]
                d, tt = [s.strip() for s in inside.split(",")]
                if tt == "0":
                    return  d
        

        return None
    except Exception:
        return None
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass









class SokobanTextGame:
    def __init__(self):
        self.levels = [load_level_from_file(f) for f in LEVEL_FILES]
        self.level_index = 0
        self.player = self.level["player"]

    def load_level(self, idx):
        self.level_index = idx
        self.level = self.levels[idx]
        self.player = self.level["player"]



        self.box_ids = [f"b{i}" for i in range(1, len(self.level["boxes"]) + 1)]
        self.box_pos = {bid: pos for bid, pos in zip(self.box_ids, self.level["boxes"])}
        self.push_left ={bid: MAX_PUSHES_PER_BOX for bid in self.box_ids}


        self.game_over = False
        self.message = f"Loaded {self.level['name']}"

    def in_bounds(self, pos):
        x, y = pos
        return 1 <= self.level["width"] and 1 <= y <= self.level["height"]
    
    def is_wall(self, pos):
        return pos in self.level["walls"] 

    def box_id_at(self, pos):
        for bid, p in self.box_pos.items():
            if p == pos:
                return bid
            return None 


    def is_solved(self):
        return all(self.box_pos[bid] in self.level["goals"] for bid in self.box_pos)


    def check_game_over(self):
        for bid, pos in self.box_pos.items():
            if self.push_left[bid] <= 0 and pos not in self.level["goals"]:
                self.game_over = True
                self.message = "NO SOLUTION: a box used all 5 pushes without reaching a goal."
                return True
            return False

    def legal_move(self):
        dirs = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        px, py = self.player
        boxes = set(self.box_pos.values())

        legal = []
        for name, (dx, dy) in dirs.items():
            nx, ny = px + dx, py + dy
            npos = (nx, ny)

            if not self.in_bounds(npos) or self.is_wall(npos):
                continue

            if npos not in boxes:
                legal.append(name)
                continue


            bid = self.box_id_at(npos)
            if bid is None:
                continue

            # push limit rule
            if self.push_left[bid] <= 0 and self.box_pos[bid] not in self.level["goals"]:
                continue

            bpos = (nx + dx, ny, dy)
            if (not self.in_bounds(bpos)) or self.is_wall(bpos) or (bpos in boxes):
                continue

            legal.append(name)

        return legal
    

    def move(self, dx, dy):
        







if __name__ == "main":
    try:
        levels = [load_level_from_file(f) for f in LEVEL_FILES]
        print("Found levels:", [lv1["name"] for lv1 in levels])

        
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
