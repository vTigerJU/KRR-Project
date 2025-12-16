import pygame
import sys
import config as c
from button import Button
# --------------------
# Initialization
# --------------------
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Grid Movement Example")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --------------------
# Game State
# --------------------
player_x = 4
player_y = 4
crates = {(5, 5), (2, 3)}
walls = {(3, 3), (3, 4)}
goals = {(1, 1), (7, 4)}

# --------------------
# Helper functions
# --------------------
def draw_grid():
    for x in range(c.GRID_WIDTH):
        for y in range(c.GRID_HEIGHT):
            rect = pygame.Rect(
                x * c.TILE_SIZE,
                y * c.TILE_SIZE+ c.TOP_BAR_HEIGHT,
                c.TILE_SIZE,
                c.TILE_SIZE
            )
            pygame.draw.rect(screen, c.GRID_COLOR, rect, 1)

def draw_player(x, y):
    rect = pygame.Rect(
        x * c.TILE_SIZE,
        y * c.TILE_SIZE + c.TOP_BAR_HEIGHT,
        c.TILE_SIZE,
        c.TILE_SIZE
    )
    pygame.draw.rect(screen, c.PLAYER_COLOR, rect)

def draw_walls(walls):
    for x, y in walls:
        rect = pygame.Rect(
            x * c.TILE_SIZE,
            y * c.TILE_SIZE+ c.TOP_BAR_HEIGHT,
            c.TILE_SIZE,
            c.TILE_SIZE
        )
        pygame.draw.rect(screen, c.WALL_COLOR, rect)

def draw_crates(crates):
    for x, y in crates:
        rect = pygame.Rect(
            x * c.TILE_SIZE,
            y * c.TILE_SIZE+ c.TOP_BAR_HEIGHT,
            c.TILE_SIZE,
            c.TILE_SIZE
        )
        pygame.draw.rect(screen, c.CRATE_COLOR, rect)

def draw_goals(goals):
    for x, y in goals:
        center_x = x * c.TILE_SIZE + c.TILE_SIZE // 2
        center_y = y * c.TILE_SIZE + c.TILE_SIZE + c.TOP_BAR_HEIGHT// 2
        pygame.draw.circle(
            screen,
            c.GOAL_COLOR,
            (center_x, center_y),
            c.GOAL_RADIUS
        )
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

def draw_win_overlay():
    overlay = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    text = font.render("LEVEL COMPLETED!", True, (255, 255, 255))
    rect = text.get_rect(center=(c.SCREEN_WIDTH//2, c.SCREEN_HEIGHT//2))
    screen.blit(text, rect)

def in_bounds(x, y):
    return 0 <= x < c.GRID_WIDTH and 0 <= y < c.GRID_HEIGHT

def blocked(x, y):
    return (x, y) in walls

def try_move(dx, dy):
    global player_x, player_y, crates

    target = (player_x + dx, player_y + dy)

    # Out of bounds
    if not in_bounds(*target):
        return

    # Wall blocks everything
    if target in walls:
        return

    # If there's a crate, try to push it
    if target in crates:
        beyond = (target[0] + dx, target[1] + dy)

        # Can't push if blocked
        if not in_bounds(*beyond):
            return
        if beyond in walls or beyond in crates:
            return

        # Push crate
        crates.remove(target)
        crates.add(beyond)

    # Move player
    player_x, player_y = target

def is_completed(crates, goals):
    return all(crate in goals for crate in crates)

def reset_game():
    print("Reset game")

def undo_move():
    print("Undo move")

def load_level():
    print("Load level")

buttons = []
x = c.BUTTON_PADDING
y = (c.TOP_BAR_HEIGHT - c.BUTTON_HEIGHT) // 2

buttons.append(Button("Reset", x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, reset_game,screen))
x += c.BUTTON_WIDTH + c.BUTTON_PADDING

buttons.append(Button("Undo", x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, undo_move,screen))
x += c.BUTTON_WIDTH + c.BUTTON_PADDING

buttons.append(Button("Load", x, y, c.BUTTON_WIDTH, c.BUTTON_HEIGHT, load_level,screen))

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
    draw_player(player_x, player_y)
    if is_completed(crates, goals):
        draw_win_overlay()
    pygame.display.flip()

