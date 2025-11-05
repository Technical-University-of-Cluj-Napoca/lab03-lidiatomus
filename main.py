import pygame
import random
from utils import *
from grid import Grid
from searching_algorithms import *


WHITE = (255, 255, 255)
LIGHT_GREY = (245, 245, 245)
DARK_GREY = (50, 50, 50)
BLACK = (20, 20, 20)
BG_COLOR = (255, 220, 230)  

BUTTON_COLORS = {
    "BFS": (173, 216, 230),
    "DFS": (255, 182, 193),
    "ASTAR": (255, 255, 153),
    "DLS": (204, 204, 255),
    "UCS": (200, 255, 200),
    "greedy": (255, 200, 150),
    "ids": (210, 210, 255),
    "ida": (255, 220, 180)
}

SIDE_PANEL_WIDTH = 160
BOTTOM_BAR_HEIGHT = 90

def draw_legend(win, font, selected_algo):
    """Draws legend instructions at the bottom."""
    legend_rect = pygame.Rect(0, HEIGHT - BOTTOM_BAR_HEIGHT, WIDTH, BOTTOM_BAR_HEIGHT)
    pygame.draw.rect(win, LIGHT_GREY, legend_rect)

    lines = [
        f"Selected: {selected_algo}",
        "1:BFS  2:DFS  3:A*  4:DLS  5:UCS  6:Greedy  7:IDS  8:IDA",
        "SPACE: Run  |  C: Clear  |  R: Reset  |  ESC: Quit"
    ]
    for i, text in enumerate(lines):
        label = font.render(text, True, BLACK)
        win.blit(label, (10, HEIGHT - BOTTOM_BAR_HEIGHT + 10 + i * 25))


def draw_buttons(win, font, buttons, selected_algo):
    """Draws the clickable buttons for each algorithm."""
    for rect, name in buttons:
        color = BUTTON_COLORS[name] if name != selected_algo else WHITE
        pygame.draw.rect(win, color, rect, border_radius=6)
        pygame.draw.rect(win, DARK_GREY, rect, width=2, border_radius=6)
        text = font.render(name, True, BLACK)
        win.blit(text, (rect.x + 15, rect.y + 7))


if __name__ == "__main__":
    pygame.init()

    WIDTH = 900
    HEIGHT = 750
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visual Pathfinding Algorithms")

    ROWS, COLS = 50, 50
    grid_width = WIDTH - SIDE_PANEL_WIDTH
    grid_height = HEIGHT - BOTTOM_BAR_HEIGHT

    grid = Grid(WIN, ROWS, COLS, grid_width, grid_height)

    start = None
    end = None
    selected_algo = "BFS"
    started = False
    run = True

    algo_map = {
        "BFS": bfs,
        "DFS": dfs,
        "ASTAR": astar,
        "DLS": lambda draw, grid, start, end: dls(draw, grid, start, end, limit=10),
        "UCS": ucs,
        "greedy": greedy_search,
        "ids": lambda draw, grid, start, end: ids(draw, grid, start, end, max_depth=15),
        "ida": ida
    }

    pygame.font.init()
    font = pygame.font.SysFont("Arial", 18)

    clock = pygame.time.Clock()  

    # algorithm buttons 
    algo_names = ["BFS", "DFS", "ASTAR", "DLS", "UCS", "greedy", "ids", "ida"]
    buttons = []
    for i, name in enumerate(algo_names):
        rect = pygame.Rect(grid_width + 20, 50 + i * 45, 120, 35)
        buttons.append((rect, name))

    mouse_down_left = False
    mouse_down_right = False

    def point_on_buttons(pos):
        for rect, _ in buttons:
            if rect.collidepoint(pos):
                return True
        return False

    while run:
        WIN.fill(BG_COLOR)
        grid.draw()
        draw_buttons(WIN, font, buttons, selected_algo)
        draw_legend(WIN, font, selected_algo)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if event.button == 1: 
                    if point_on_buttons(pos):
                        for rect, name in buttons:
                            if rect.collidepoint(pos):
                                selected_algo = name
                                print(f"Selected {name}")
                                break
                    else:
                        if pos[0] < grid_width and pos[1] < grid_height:
                            row, col = grid.get_clicked_pos(pos)
                            if 0 <= row < ROWS and 0 <= col < COLS:
                                spot = grid.grid[row][col]
                                if not start and spot != end:
                                    start = spot
                                    start.make_start()
                                elif not end and spot != start:
                                    end = spot
                                    end.make_end()
                                elif spot != start and spot != end:
                                    spot.make_barrier()
                    mouse_down_left = True

                elif event.button == 3: 
                    if pos[0] < grid_width and pos[1] < grid_height:
                        row, col = grid.get_clicked_pos(pos)
                        if 0 <= row < ROWS and 0 <= col < COLS:
                            spot = grid.grid[row][col]
                            spot.reset()
                            if spot == start:
                                start = None
                            elif spot == end:
                                end = None
                    mouse_down_right = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down_left = False
                elif event.button == 3:
                    mouse_down_right = False

            elif event.type == pygame.MOUSEMOTION:
                pos = event.pos
                if point_on_buttons(pos):
                    continue
                if pos[0] < grid_width and pos[1] < grid_height:
                    row, col = grid.get_clicked_pos(pos)
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        spot = grid.grid[row][col]
                        if mouse_down_left:
                            if spot != start and spot != end:
                                spot.make_barrier()
                        elif mouse_down_right:
                            spot.reset()
                            if spot == start:
                                start = None
                            elif spot == end:
                                end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_1:
                    selected_algo = "BFS"
                elif event.key == pygame.K_2:
                    selected_algo = "DFS"
                elif event.key == pygame.K_3:
                    selected_algo = "ASTAR"
                elif event.key == pygame.K_4:
                    selected_algo = "DLS"
                elif event.key == pygame.K_5:
                    selected_algo = "UCS"
                elif event.key == pygame.K_6:
                    selected_algo = "greedy"
                elif event.key == pygame.K_7:
                    selected_algo = "ids"
                elif event.key == pygame.K_8:
                    selected_algo = "ida"

                elif event.key == pygame.K_SPACE and not started:
                    if not start or not end:
                        print("Set start and end points first.")
                    else:
                        for row in grid.grid:
                            for spot in row:
                                spot.update_neighbors(grid.grid)
                        algo_fn = algo_map.get(selected_algo)
                        if algo_fn:
                            mouse_down_left = False
                            mouse_down_right = False

                            def draw_all():
                                WIN.fill(BG_COLOR)
                                grid.draw()
                                draw_buttons(WIN, font, buttons, selected_algo)
                                draw_legend(WIN, font, selected_algo)
                                pygame.display.flip()       
                                clock.tick(60)              

                            started = True
                            result = algo_fn(draw_all, grid, start, end)
                            started = False

                            mouse_down_left = False
                            mouse_down_right = False

                            if result is False:
                                run = False
                                break

                elif event.key == pygame.K_c:
                    start, end = None, None
                    grid.reset()
                elif event.key == pygame.K_r:
                    start, end = None, None
                    started = False
                    grid.reset()

    pygame.quit()
