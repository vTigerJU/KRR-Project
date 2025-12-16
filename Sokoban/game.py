import pygame
import sys
import config as c
from components.button import Button
import map_loader
import controller 

pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Grid Movement Example")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
map_name = "maps/test.txt"
map = map_loader.load_level_from_file(map_name)

crate_img = pygame.image.load("elements/crate.png").convert_alpha()
crate_img = pygame.transform.scale(crate_img, (c.TILE_SIZE, c.TILE_SIZE))

wall_img = pygame.image.load("elements/block.png").convert_alpha()
wall_img = pygame.transform.scale(wall_img, (c.TILE_SIZE, c.TILE_SIZE))

player_img = pygame.image.load("elements/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (c.TILE_SIZE, c.TILE_SIZE))

goal_img = pygame.image.load("elements/goal.png").convert_alpha()
goal_img = pygame.transform.scale(goal_img, (c.TILE_SIZE, c.TILE_SIZE))

floor_img = pygame.image.load("elements/floor.png").convert_alpha()
floor_img = pygame.transform.scale(floor_img, (c.TILE_SIZE, c.TILE_SIZE))

player_x, player_y = 0,0

crates = dict()
walls = set()
goals = set()
hints = []
destroyed_crates = set()
no_solution = False
banner_text = ""

def load_initial_state():
    global crates, walls, goals, no_solution, player_x, player_y, banner_text, destroyed_crates
    map = map_loader.load_level_from_file(map_name)
    no_solution = False
    player_x, player_y = map["player"]
    walls = map["walls"]
    goals = map["goals"]
    banner_text = ""
    c.GRID_WIDTH = map["width"]
    c.GRID_HEIGHT = map["height"]
    crates = dict()
    for crate in map["boxes"]:
        crates[crate] = 0
    destroyed_crates = set()

load_initial_state()

def draw_grid():
    for x in range(c.GRID_WIDTH):
        for y in range(c.GRID_HEIGHT):
            screen.blit(floor_img, (x * c.TILE_SIZE, y * c.TILE_SIZE + c.TOP_BAR_HEIGHT))
            

def draw_player(x, y):
    screen.blit(player_img, (x * c.TILE_SIZE, y * c.TILE_SIZE + c.TOP_BAR_HEIGHT))

def draw_walls(walls):
    for x, y in walls:
        screen.blit(wall_img, (x * c.TILE_SIZE, y * c.TILE_SIZE + c.TOP_BAR_HEIGHT))

def draw_crates(crates):
    for x, y in crates:
        screen.blit(crate_img, (x * c.TILE_SIZE, y * c.TILE_SIZE + c.TOP_BAR_HEIGHT))

def draw_goals(goals):
    for x, y in goals:
        screen.blit(goal_img, (x * c.TILE_SIZE, y * c.TILE_SIZE + c.TOP_BAR_HEIGHT))

def draw_destroyed():
    for x, y in destroyed_crates:
        rect = pygame.Rect(
                x * c.TILE_SIZE,
                y * c.TILE_SIZE+ c.TOP_BAR_HEIGHT,
                c.TILE_SIZE,
                c.TILE_SIZE
            )
        pygame.draw.rect(screen, (255, 0, 0), rect, 1)

def draw_top_bar():
    pygame.draw.rect(
        screen,
        c.TOP_BAR_COLOR,
        pygame.Rect(0, 0, c.SCREEN_WIDTH, c.TOP_BAR_HEIGHT)
    )

    mouse_pos = pygame.mouse.get_pos()
    for b in buttons:
        b.update(mouse_pos)
        b.draw()
    label = font.render(banner_text, True, c.TEXT_COLOR)
    screen.blit(
        label, 
        (
            c.SCREEN_WIDTH - label.get_width() - 10,
            (c.TOP_BAR_HEIGHT - label.get_height()) // 2
        )
    )

def draw_overlay(overlay_text):
    overlay = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    text = font.render(overlay_text, True, (255, 255, 255))
    rect = text.get_rect(center=(c.SCREEN_WIDTH//2, c.SCREEN_HEIGHT//2))
    screen.blit(text, rect)

def draw_hint(hints):
    for x,y in hints:
        center_x = x * c.TILE_SIZE + c.TILE_SIZE // 2
        center_y = y * c.TILE_SIZE + c.TILE_SIZE + c.TOP_BAR_HEIGHT// 2
        pygame.draw.circle(
            screen,
            (255, 105, 180),
            (center_x, center_y),
            c.GOAL_RADIUS
        )

def in_bounds(x, y):
    return 0 <= x < c.GRID_WIDTH and 0 <= y < c.GRID_HEIGHT

def blocked(x, y):
    return (x, y) in walls

def destroy_crate(crate_at):
    global crates, destroyed_crates
    destroyed_crates.add(crate_at)
    crates.pop(crate_at)
    print(crates)

def try_move(dx, dy):
    global player_x, player_y, crates

    target = (player_x + dx, player_y + dy)

    if not in_bounds(*target):
        return

    if target in walls:
        return

    if target in crates:
        beyond = (target[0] + dx, target[1] + dy)

        if not in_bounds(*beyond):
            return
        if beyond in walls or beyond in crates:
            return
        push_counter = crates[target]
        crates.pop(target)
        crates[beyond] = push_counter + 1
        if crates[beyond] == c.MAX_PUSHES:
            destroy_crate(beyond)

    player_x, player_y = target

def is_completed(crates, goals):
    if len(goals) == len(crates):
        return all(crate in goals for crate in crates)
    else:
        return False

def reset_game():
    print("Reset game")
    load_initial_state()


def check():
    global no_solution, banner_text
    map_facts = map_loader.build_asp_facts(map,(player_x,player_y),crates)
    result = controller.solve(map_facts)
    if result is None:
        no_solution = True
        banner_text= "no solution"
    else:
        banner_text = "still solvable"
    
def hint():
    global no_solution
    map_facts = map_loader.build_asp_facts(map,(player_x,player_y),crates)
    print(map_facts)
    try:
        x, y = controller.hint(map_facts)
        print(x,y)
        hints.append((x,y))
    except:
        print("No solution")
        no_solution = True


buttons = []
x = c.BUTTON_PADDING
y = (c.TOP_BAR_HEIGHT - c.BUTTON_HEIGHT) // 2

buttons.append(Button("Reset", x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, reset_game,screen))
x += c.BUTTON_WIDTH + c.BUTTON_PADDING

buttons.append(Button("Hint", x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, hint,screen))
x += c.BUTTON_WIDTH + c.BUTTON_PADDING

buttons.append(Button("Check", x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, check,screen))

#Game Loop
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        for b in buttons:
            b.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                try_move(0, -1)
            elif event.key == pygame.K_DOWN:
                try_move(0, 1)
            elif event.key == pygame.K_LEFT:
                try_move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                try_move(1, 0)
            hints = []
            # Keep player inside grid
            player_x = max(0, min(c.GRID_WIDTH - 1, player_x))
            player_y = max(0, min(c.GRID_HEIGHT - 1, player_y))

    # Drawing
    screen.fill(c.BG_COLOR)
    draw_top_bar()
    draw_grid()
    draw_walls(walls)
    draw_goals(goals)
    draw_crates(crates)
    draw_destroyed()
    draw_hint(hints)
    draw_player(player_x, player_y)
    if is_completed(crates, goals):
        draw_overlay("Level Complete")
    if no_solution:
        draw_overlay("No Solution")
    pygame.display.flip()