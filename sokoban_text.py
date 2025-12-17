# final Mini-Project : Group 3
# written By: Axel Lindh - Hannan Khalil - Emil Anderö - Viktor Tiger 

# Sokoban with ASP-Based Hint System

import subprocess
import tempfile
import os
import sys
import re 


def extract_first_move(output):
    for line in output.splitlines():
        m = re.search(r"move\((\w+),0\)", line)
        if m:
            return m.group(1)
    return None


ROOT = os.path.dirname(os.path.abspath(__file__))


BASE_LP_FILE = os.path.join(ROOT, "sokoban_base.lp")
LEVEL_DIR = os.path.join(ROOT, "maps")

LEVEL_FILES  = sorted(

    os.path.join(LEVEL_DIR, f)
    for f in os.listdir(LEVEL_DIR)
    if f.endswith(".txt")
)

def list_level_files(level_dir: str):
    if not os.path.isdir(level_dir):
        raise FileNotFoundError(f"Missing levels folder: {level_dir}")
    files = []
    for f in os.listdir(level_dir):
        if f.endswith(".txt"):
            files.append(os.path.join(level_dir, f))
    files.sort()
    if not files:
        raise FileNotFoundError(f"No .txt levels found in: {level_dir}")
    return files




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
            else:
                pass

    if player is None:
        raise ValueError(f"No player '@' found in level file {path}")

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

# ------ASP interface-----

def build_asp_facts(level, player_pos, boxes):
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

    for i, (bx, by) in enumerate(boxes, start = 1):
        lines.append(f"box(b{i}, {bx}, {by}, 0).")

    return "\n".join(lines)


def ask_hint(level, player_pos, boxes):
    """
    call clingo with  current state and return: 
        - direction string ('up', 'down', 'left', 'right') or
        - None if unsatisfiable or error.
    """

    if not os.path.exists(BASE_LP_FILE):
        print("Error: sokoban_base.lp not found.")
        return None
    
    asp_facts = build_asp_facts(level, player_pos, boxes)

    with tempfile.NamedTemporaryFile(mode = "w", suffix = ".lp", delete = False) as tmp:
        tmp.write(asp_facts)
        tmp_path = tmp.name

    try:
        cmd = ["clingo", BASE_LP_FILE, tmp_path, "--quiet=1", "--opt-mode=optN", "-n", "1"]
        result = subprocess.run(cmd, capture_output = True, text = True, timeout = 60 )
        output = (result.stdout or "") + "\n" + (result.stderr or "")

        if "UNSATISFIABLE" in output:
            return None
        
        tokens = output.split()
        moves = [t for t in tokens if t.startswith("move(")]
        first_move = None 
        for m in moves:
            inside = m[m.find ("(") + 1 : m.find(")")]
            direction, t = inside.split(",")
            if t == "0":
                return  direction
        

        return None
    except Exception as e:
        print ("Error running clingo: ", e)
        return None 
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass




# ----- Game Logic (text) --------

class SokobanTextGame:
    def __init__(self):
        self.levels = [load_level_from_file(f) for f in LEVEL_FILES]
        self.level_index = 0
        self.load_level(self.level_index)
        self.message = ""

    def load_level(self, idx):
        lvl = self.levels[idx]
        self.level = lvl
        self.player = lvl["player"]
        self.boxes = list(lvl["boxes"])
        self.message = f"Loaded {lvl['name']}"

    def in_bounds(self, pos):
        x, y = pos
        return 1 <= x <= self.level["width"] and 1 <= y <= self.level["height"]

    def is_wall(self, pos):
        return pos in self.level["walls"]

    def is_box(self, pos):
        return pos in self.boxes

    def is_solved(self):
        return all(b in self.level["goals"] for b in self.boxes)

    def try_move(self, dx, dy):
        px, py = self.player
        target = (px + dx, py + dy)

        if not self.in_bounds(target):
            self.message = "Blocked: outside grid"
            return
        if self.is_wall(target):
            self.message = "Blocked: wall"
            return
        if self.is_box(target):
            bx, by = target
            beyond = (bx + dx, by + dy)
            if (not self.in_bounds(beyond)
                or self.is_wall(beyond)
                or self.is_box(beyond)):
                self.message = "Blocked: can't push box"
                return
            # push box
            self.boxes.remove(target)
            self.boxes.append(beyond)
            self.player = target
            self.message = "Pushed box"
        else:
            self.player = target
            self.message = "Moved"

        if self.is_solved():
            self.message = "Level solved! Press n for next level."

    def print_grid(self):
        w = self.level["width"]
        h = self.level["height"]
        walls = self.level["walls"]
        goals = self.level["goals"]

        print("\n" + "=" * (w + 8))
        print(f"Level: {self.level['name']} ({self.level_index+1}/{len(self.levels)})")
        for y in range(1, h + 1):
            row = []
            for x in range(1, w + 1):
                pos = (x, y)
                ch = " "
                if pos in walls:
                    ch = "#"
                if pos in goals:
                    ch = "."
                if pos in self.boxes:
                    ch = "$"
                if pos in goals and pos in self.boxes:
                    ch = "*"
                if pos == self.player:
                    ch = "@"
                    if pos in goals:
                        ch = "+"
                row.append(ch)
            print("".join(row))
        print("=" * (w + 8))
        if self.message:
            print("Message:", self.message)

    def run(self):
        print("Sokoban + ASP (text version, classic symbols)")
        print("Controls:")
        print("  w/a/s/d: move")
        print("  h      : ask ASP hint")
        print("  r      : reset level")
        print("  n      : next level")
        print("  q      : quit")

        while True:
            self.print_grid()
            if self.is_solved():
                cmd = input("[Solved] Command (n/r/q): ").strip().lower()
            else:
                cmd = input("Command (w/a/s/d/h/r/n/q): ").strip().lower()

            if cmd == "q":
                print("Good Bye!")
                break
            elif cmd == "r":
                self.load_level(self.level_index)
            elif cmd == "n":
                self.level_index = (self.level_index + 1) % len(self.levels)
                self.load_level(self.level_index)
            elif cmd in ("w", "a", "s", "d"):
                dx, dy = 0, 0
                if cmd == "w":
                    dy = -1
                elif cmd == "s":
                    dy = 1
                elif cmd == "a":
                    dx = -1
                elif cmd == "d":
                    dx = 1
                self.try_move(dx, dy)
            elif cmd == "h":
                if self.is_solved():
                    self.message = "Already solved."
                else:
                    hint = ask_hint(self.level, self.player, self.boxes)
                    if hint is None:
                        self.message = "ASP: UNSOLVABLE from this state (or no solution within maxT)."
                    else:
                        self.message = f"ASP Hint: move {hint}"
            else:
                self.message = "Unknown command."
                

if __name__ == "__main__":
    try:
        game = SokobanTextGame()
        game.run()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
