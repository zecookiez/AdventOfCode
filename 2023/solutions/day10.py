from collections import defaultdict

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day10.txt", "r")
    grid = [i.strip() for i in file.readlines()]

    H = len(grid)
    W = len(grid[0])
    seen = set()
    S_rep = "|" # Manually inspected from input T_T
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch != "S":
                continue
            grid[i] = row.replace("S", S_rep)
            # This is just BFS
            queue = [(i, j)]
            seen.add((i, j))
            dist = defaultdict(int)
            for x, y in queue:
                directions = {
                    "|": [(1, 0), (-1, 0)],
                    "-": [(0, 1), (0, -1)],
                    "L": [(-1, 0), (0, 1)],
                    "J": [(-1, 0), (0, -1)],
                    "F": [(1, 0), (0, 1)],
                    "7": [(1, 0), (0, -1)],
                    "S": [(1, 0), (-1, 0)],
                }[grid[x][y]]
                for dx, dy in directions:
                    nx, ny = dx + x, dy + y
                    if 0 <= nx < H and 0 <= ny < W and (nx, ny) not in seen:
                        dist[nx,ny] = dist[x,y] + 1
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            part1 = max(dist.values())

    part2 = 0
    for x in range(H):
        for y in range(W):
            if (x, y) in seen: continue
            # Point a ray in one direction
            # Main idea is to count crossing with vertical bars
            # But we need to consider corners that cancel each other out:
            #    - LJ for the top horizontal parity (line will stay at the top)
            #    - F7 for the bottom horizontal parity (line will stay at the bottom)
            par_bottom = par_top = 0
            for ny in range(y + 1):
                if (x, ny) in seen and grid[x][ny] in "|JL":
                    par_top ^= 1
                if (x, ny) in seen and grid[x][ny] in "|F7":
                    par_bottom ^= 1
            if par_bottom and par_top:
                part2 += 1

    return part1, part2

if __name__ == "__main__":
    print(main())

"""
Review:
- i thought the input would be one big loop without other noise so i lost a bunch of time there T_T
- went for wacky stuff for part 2 for a long time so thats lost too
"""