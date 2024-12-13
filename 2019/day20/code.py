from collections import defaultdict, deque
import string


def parse_maze(filename):
    with open(filename) as f:
        maze = f.read().splitlines()

    portals = defaultdict(list)
    height, width = len(maze), len(maze[0])

    for y in range(height):
        for x in range(width):
            if maze[y][x].isalpha():
                if x + 1 < width and maze[y][x + 1].isalpha():
                    portal_name = maze[y][x] + maze[y][x + 1]
                    if x - 1 >= 0 and maze[y][x - 1] == '.':
                        portals[portal_name].append((x - 1, y))
                    elif x + 2 < width and maze[y][x + 2] == '.':
                        portals[portal_name].append((x + 2, y))
                if y + 1 < height and maze[y + 1][x].isalpha():
                    portal_name = maze[y][x] + maze[y + 1][x]
                    if y - 1 >= 0 and maze[y - 1][x] == '.':
                        portals[portal_name].append((x, y - 1))
                    elif y + 2 < height and maze[y + 2][x] == '.':
                        portals[portal_name].append((x, y + 2))

    return maze, portals


def build_graph(maze, portals):
    graph = defaultdict(list)

    height, width = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for y in range(height):
        for x in range(width):
            if maze[y][x] == '.':
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '.':
                        graph[(x, y)].append((nx, ny))

    for portal_positions in portals.values():
        if len(portal_positions) == 2:
            graph[portal_positions[0]].append(portal_positions[1])
            graph[portal_positions[1]].append(portal_positions[0])

    return graph


def shortest_path(graph, start, end):
    queue = deque([(start, 0)])
    visited = set()

    while queue:
        current, steps = queue.popleft()

        if current == end:
            return steps

        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, steps + 1))

    return -1


def part_1():
    maze, portals = parse_maze("day20/day20_input.txt")
    print(shortest_path(build_graph(maze, portals),
          portals["AA"][0], portals["ZZ"][0]))


def shortest_path_recursive(graph, portals, start, end):
    """Find the shortest path in a recursive maze."""
    queue = deque([(start, 0, 0)])  # (position, level, steps)
    visited = set()

    # Determine maze boundaries for identifying inner and outer portals
    min_x = min(pos[0] for portal in portals.values() for pos in portal)
    max_x = max(pos[0] for portal in portals.values() for pos in portal)
    min_y = min(pos[1] for portal in portals.values() for pos in portal)
    max_y = max(pos[1] for portal in portals.values() for pos in portal)

    while queue:
        current, level, steps = queue.popleft()

        # Stop if we reach the end at level 0
        if current == end and level == 0:
            return steps

        # Skip visited states
        if (current, level) in visited:
            continue
        visited.add((current, level))

        # Explore neighbors
        for neighbor in graph[current]:
            # Handle portal transitions
            if neighbor in portals:
                for portal_name, positions in portals.items():
                    if neighbor in positions and portal_name not in ("AA", "ZZ"):  # Exclude start and end portals
                        other_end = next(p for p in positions if p != neighbor)
                        if (min_x < neighbor[0] < max_x and min_y < neighbor[1] < max_y):
                            # Inner portal -> Increase level
                            queue.append((other_end, level + 1, steps + 1))
                        elif level > 0:
                            # Outer portal -> Decrease level
                            queue.append((other_end, level - 1, steps + 1))
            else:
                # Regular movement
                queue.append((neighbor, level, steps + 1))

    return -1  # No path found



def part_2():
    maze, portals = parse_maze("day20/day20_input.txt")
    print(shortest_path_recursive(build_graph(maze, portals), portals,
          portals["AA"][0], portals["ZZ"][0]))


if __name__ == "__main__":

    part_1()
    part_2()

        # Parse maze and portals
    maze, portals = parse_maze("day20/day20_input.txt")

    # Part 1
    start = portals["AA"][0]
    end = portals["ZZ"][0]
    graph = build_graph(maze, portals)
    part1_result = shortest_path(graph, start, end)
    print(f"Part 1: Shortest path = {part1_result}")

    # Part 2
    part2_result = shortest_path_recursive(graph, portals, start, end)
    print(f"Part 2: Shortest recursive path = {part2_result}")
