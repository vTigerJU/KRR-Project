import clingo
import re

final_model = None


def on_model(model):
    global final_model
    final_model = model.symbols(shown=True)

def solve(map_facts):
    ctl = clingo.control.Control(["--stats", "--opt-mode=opt", "-t4"])
    try:
        ctl.load("sokoban.lp")
        ctl.add("base", [], map_facts)
        ctl.ground([("base", [])])
        result = ctl.solve(on_model=on_model)

        if result.satisfiable and final_model is not None:
           
            return final_model
        else:
            return None
    except Exception as e:
        print(e)

def getDirection(dir,x,y):
    match dir:
        case "moveUp":
            y-=1
        case "moveDown":
            y+=1
        case "moveLeft":
            x-=1
        case "moveRight":
            x+=1
        case "pushUp":
            y-=1
        case "pushDown":
            y+=1
        case "pushLeft":
            x-=1
        case "pushRight":
            x+=1
    return x,y

def hint(map_facts):
    results = solve(map_facts)
    try:
        move = str(results[0])
        dirMatch = re.split(r'\(',move)
        dir = dirMatch[1]
        match = re.findall(r'\d+', move)
        if len(match) >= 2:
            first_two_digits = "".join(match[:2])
            x = int(first_two_digits[0])
            y = int(first_two_digits[1])

        x,y = getDirection(dir,x,y)

        return x, y
    
    except:
        return None
    
