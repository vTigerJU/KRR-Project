import clingo
import map_loader

def on_model(m):
    print(m)

def solve():
    ctl = clingo.control.Control(["--stats", "--opt-mode=optN", "-t4"])
    try:
        ctl.load("asp/sokoban.lp")
        map_facts = map_loader.test()
        print(map_facts)
        ctl.add("base", [], map_facts)
        ctl.ground([("base", [])])
        print(ctl.solve(on_model=on_model))
    except Exception as e:
        print(e)

solve()