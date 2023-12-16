from collections import deque

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day16.txt", "r")
    grid = [i.strip() for i in file.readlines()]
    H, W = len(grid), len(grid[0])

    directions = {
        (0, 1, "\\"): (1, 0),
        (0, -1, "\\"): (-1, 0),
        (1, 0, "\\"): (0, 1),
        (-1, 0, "\\"): (0, -1),
        (0, 1, "/"): (-1, 0),
        (0, -1, "/"): (1, 0),
        (1, 0, "/"): (0, -1),
        (-1, 0, "/"): (0, 1)
    }
    def solve(queue):
        seen = set(queue)
        queue = deque(queue)
        while queue:
            x, y, dx, dy = queue.popleft()
            # Move until we hit a special tile (sort of faster)
            while W > y >= 0 <= x < H and grid[x][y] == ".":
                seen.add((x, y, dx, dy))
                x += dx
                y += dy
            if not W > y >= 0 <= x < H:
                continue
            ch = grid[x][y]
            seen.add((x, y, dx, dy))
            if (dy and ch == "|") or (dx and ch == "-"):
                for ndx, ndy in ([(0, 1), (0, -1)] if dx else [(1, 0), (-1, 0)]):
                    nx = x + ndx
                    ny = y + ndy
                    if W > ny >= 0 <= nx < H and (nx, ny, ndx, ndy) not in seen:
                        seen.add((nx, ny, ndx, ndy))
                        queue.append((nx, ny, ndx, ndy))
            else:
                if (dx, dy, ch) in directions:
                    dx, dy = directions[dx, dy, ch]
                x += dx
                y += dy
                if W > y >= 0 <= x < H and (x, y, dx, dy) not in seen:
                    seen.add((x, y, dx, dy))
                    queue.append((x, y, dx, dy))
        return len({(x, y) for x, y, a, b in seen})

    part2 = 0
    for col in range(W):
        part2 = max(part2, solve([(0, col, 1, 0)]), solve([(H - 1, col, -1, 0)]))
    for row in range(H):
        part2 = max(part2, solve([(row, 0, 0, 1)]), solve([(row, W - 1, 0, -1)]))

    return solve([(0, 0, 0, 1)]), part2

if __name__ == "__main__":
    print(main())

"""
Review:
- part 1 was super mid, i was just slowly implementing it through everything and had a bug with my mirror code
- part 2 was ok considering i gained points despite not getting points in part 1
- i also need to optimize this code

its so over
"""