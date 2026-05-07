import heapq
from config import DIAGONAL_PATHING
def astar(map, start, goal, additional_obstacles = None):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    if goal in additional_obstacles.keys():
        return []
    
    if DIAGONAL_PATHING:
        path_dirs = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)) # R, L, D, U
    else:
        path_dirs = ((1,0),(-1,0),(0,1),(0,-1))
    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break

        x, y = current

        for dx, dy in path_dirs:
            nx, ny = x + dx, y + dy
            if not map.is_valid_position(nx, ny): continue

            if additional_obstacles is not None:
                if (x,y) in additional_obstacles.keys():
                    continue

            new_cost = cost_so_far[current] + 1
            neighbor = (nx, ny)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + abs(goal[0]-nx) + abs(goal[1]-ny)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # reconstruct path
    path = []
    cur = goal
    while cur and cur != start:
        path.append(cur)
        cur = came_from.get(cur)
    path.reverse()
    return path