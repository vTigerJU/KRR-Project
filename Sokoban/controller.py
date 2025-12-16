import clingo
import map_loader

def on_model(m):
    print(m)

def solve(map_facts):
    ctl = clingo.control.Control(["--stats", "--opt-mode=optN", "-t4"])
    try:
        ctl.load("sokoban.lp")
        print(map_facts)
        ctl.add("base", [], map_facts)
        ctl.ground([("base", [])])
        print(ctl.solve(on_model=on_model))
    except Exception as e:
        print(e)

