from utils import *
from collections import deque
from queue import PriorityQueue
from itertools import count
from grid import Grid
from spot import Spot

def _handle_quit():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            return True
    return False
pass

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        if _handle_quit():
            return False

        current = queue.popleft()

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False
pass

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depth-First Search (DFS) Algorithm.
    Args:
        draw (callable): Function to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        if _handle_quit():
            return False

        current = stack.pop()

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False
pass

def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
pass

def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
pass

def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    counter = count()
    open_set = PriorityQueue()
    open_set.put((0, next(counter), start))
    open_set_hash = {start}

    came_from = {}
    g_score = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid.grid for spot in row}
    f_score[start] = h_manhattan_distance((start.row, start.col), (end.row, end.col))

    while not open_set.empty():
        if _handle_quit():
            return False

        current = open_set.get()[2]
        open_set_hash.discard(current)

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue

            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h_manhattan_distance((neighbor.row, neighbor.col), (end.row, end.col))
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], next(counter), neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False
pass
# and the others algorithms...
# ▢ Depth-Limited Search (DLS)
def dls(draw: callable, grid: Grid, start: Spot, end: Spot, limit: int) -> bool:
    """
    Depth-Limited Search (DLS) Algorithm. NEED S FIXES MAYBE
    Args:
        draw (callable): Function to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
        limit (int): The depth limit for the search.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    stack = [(start, 0)]
    visited = {start}
    came_from = {}

    while stack:
        if _handle_quit():
            return False

        current, depth = stack.pop()

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True

        if depth < limit:
            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append((neighbor, depth + 1))
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False
    pass

# ▢ Uninformed Cost Search (UCS)
def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Uninformed Cost Search (UCS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    counter = count()
    open_set = PriorityQueue()
    open_set.put((0, next(counter), start))
    open_set_hash = {start}
    came_from = {}
    g_score = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0
    while not open_set.empty():
        if _handle_quit():
            return False

        current = open_set.get()[2]
        open_set_hash.discard(current)

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue

            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                if neighbor not in open_set_hash:
                    open_set.put((g_score[neighbor], next(counter), neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False

    pass
# ▢ Greedy Search
def greedy_search(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Greedy Best-First Search Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise. ALSO NEEDS FIXES
    """
    counter = count()
    open_set = PriorityQueue()
    open_set.put((0, next(counter), start))
    open_set_hash = {start}
    came_from = {}

    while not open_set.empty():
        if _handle_quit():
            return False

        current = open_set.get()[2]
        open_set_hash.discard(current)

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                if current != start:
                    current.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue

            heuristic = h_manhattan_distance((neighbor.row, neighbor.col), (end.row, end.col))
            if neighbor not in open_set_hash:
                came_from[neighbor] = current
                open_set.put((heuristic, next(counter), neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False
    pass

# ▢ Iterative Deepening Search/Iterative Deepening Depth-First Search (IDS/IDDFS)
def ids(draw: callable, grid: Grid, start: Spot, end: Spot, max_depth: int) -> bool:
    """
    Iterative Deepening Search (IDS) Algorithm.
    Args:
        draw (callable): Function to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
        max_depth (int): The maximum depth limit for the search.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    for depth in range(max_depth + 1):
        stack = [(start, 0)]
        visited = {start}
        came_from = {}

        while stack:
            if _handle_quit():
                return False

            current, curr_depth = stack.pop()

            if current == end:
                # reconstruct path
                while current in came_from:
                    current = came_from[current]
                    if current != start:
                        current.make_path()
                        draw()
                end.make_end()
                start.make_start()
                return True

            if curr_depth < depth:
                for neighbor in current.neighbors:
                    if neighbor not in visited and not neighbor.is_barrier():
                        visited.add(neighbor)
                        came_from[neighbor] = current
                        stack.append((neighbor, curr_depth + 1))
                        neighbor.make_open()

            draw()
            if current != start:
                current.make_closed()

    return False
    pass
# ▢ Iterative Deepening A* (IDA)
def ida(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Iterative Deepening A* (IDA*) Algorithm.
    Args:
        draw (callable): Function to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    threshold = h_manhattan_distance((start.row, start.col), (end.row, end.col))

    def search(path: list[Spot], g: float, threshold: float) -> float | bool:
        current = path[-1]
        f = g + h_manhattan_distance((current.row, current.col), (end.row, end.col))

        if f > threshold:
            return f
        if current == end:
            return True

        min_threshold = float("inf")
        for neighbor in current.neighbors:
            if neighbor not in path and not neighbor.is_barrier():
                path.append(neighbor)
                temp = search(path, g + 1, threshold)
                if temp is True:
                    return True
                if temp < min_threshold:
                    min_threshold = temp
                path.pop()
                neighbor.make_open()
                draw()

        if current != start:
            current.make_closed()
        return min_threshold

    path = [start]
    while True:
        temp = search(path, 0, threshold)
        if temp is True:
            for spot in path:
                if spot != start and spot != end:
                    spot.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True
        if temp == float("inf"):
            return False
        threshold = temp
    pass
# Assume that each edge (graph weight) equalss
