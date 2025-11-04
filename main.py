from utils import *
from grid import Grid
from searching_algorithms import *

if __name__ == "__main__":
    # setting up how big will be the display window
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # set a caption for the window
    pygame.display.set_caption("Path Visualizing Algorithm")

    ROWS = 50  # number of rows
    COLS = 50  # number of columns
    grid = Grid(WIN, ROWS, COLS, WIDTH, HEIGHT)

    start = None
    end = None

    # allow selecting the algorithm (1: BFS, 2: DFS, 3: A*)
    selected_algo = "BFS"
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
    # a small font to render the currently selected algorithm on screen
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 18)

    # flags for running the main loop
    run = True
    started = False

    while run:
        grid.draw()  # draw the grid and its spots

        # draw selected algorithm label
        label = font.render(f"Selected: {selected_algo} (1:BFS 2:DFS 3:A*)", True, (0,0,0))
        WIN.blit(label, (10, 10))

        for event in pygame.event.get():
            # verify what events happened
            if event.type == pygame.QUIT:
                run = False

            if started:
                # do not allow any other interaction if the algorithm has started
                continue  # ignore other events if algorithm started

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)

                if row >= ROWS or row < 0 or col >= COLS or col < 0:
                    continue  # ignore clicks outside the grid

                spot = grid.grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                spot = grid.grid[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                # select algorithm keys
                if event.key == pygame.K_1:
                    selected_algo = "BFS"
                    print("Selected BFS")
                elif event.key == pygame.K_2:
                    selected_algo = "DFS"
                    print("Selected DFS")
                elif event.key == pygame.K_3:
                    selected_algo = "ASTAR"
                    print("Selected A*")
                elif event.key == pygame.K_4:
                    selected_algo = "DLS"
                    print("Selected DLS")
                elif event.key == pygame.K_5:
                    selected_algo = "UCS"
                    print("Selected UCS")
                elif event.key == pygame.K_6:
                    selected_algo = "greedy"
                    print("Selected Greedy Search")
                elif event.key == pygame.K_7:
                    selected_algo = "ids"
                    print("Selected ids")   
                elif event.key == pygame.K_8:
                    selected_algo = "ida"
                    print("Selected ida")     
                    

                elif event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_SPACE and not started:
                    # run the algorithm
                    if not start or not end:
                        print("Set start and end points before running the algorithm.")
                    else:
                        for row in grid.grid:
                            for spot in row:
                                spot.update_neighbors(grid.grid)

                        algo_fn = algo_map.get(selected_algo)
                        if algo_fn:
                            started = True
                            algo_fn(lambda: grid.draw(), grid, start, end)
                            started = False
                        else:
                            print(f"No implementation for algorithm: {selected_algo}")

                # clear everything (existing)
                if event.key == pygame.K_c:
                    print("Clearing the grid...")
                    start = None
                    end = None
                    grid.reset()

                # reset using 'r' so you don't have to close/reopen (same as 'c' here)
                if event.key == pygame.K_r:
                    print("Resetting (R) ...")
                    start = None
                    end = None
                    started = False
                    grid.reset()
    pygame.quit()
