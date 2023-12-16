from collections import defaultdict
from bisect import bisect

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day11.txt", "r")
    grid = [i.strip() for i in file.readlines()]

    H, W = len(grid), len(grid[0])

    empty_row = {ind for ind, row in enumerate(grid) if "#" not in row}
    empty_col = {ind for ind in range(W) if all(row[ind] == "." for row in grid)}

    def solve_dijkstra(X, Y, multiplier):
        # Original dijkstra solution because I thought part 2 would introduce obstacles
        def neigh4(x, y, H, W):
            for nx, ny in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
                if 0 <= nx < H and 0 <= ny < W:
                    yield (nx, ny)
        queue = [(0, X, Y)]
        dist = defaultdict(int)
        while queue:
            d, x, y = heappop(queue)
            if dist[x, y] < d:
                continue
            dist[x, y] = d
            for nx, ny in neigh4(x, y, H, W):
                nd = 1 + (multiplier - 1) * (nx in empty_row or ny in empty_col)
                if (nx, ny) not in dist or dist[nx, ny] > d + nd:
                    dist[nx, ny] = d + nd
                    heappush(queue, (d + nd, nx, ny))
        return dist

    def cnt_range(arr, L, R):
        if L > R:
            L, R = R, L
        # Count number of elements in between [L, R]
        return bisect(arr, R) - bisect(arr, L - 1)

    def solve_fast(X, Y, multiplier, pts):
        return sum(x - X + abs(y - Y) + (multiplier - 1) * (cnt_range(erow, X, x) + cnt_range(ecol, Y, y)) for x, y in pts)

    pts = {(x, y) for x, row in enumerate(grid) for y, ch in enumerate(row) if ch == "#"}
    ecol = sorted(empty_col | {-1, W + 1})
    erow = sorted(empty_row | {-1, H + 1})
    part1 = part2 = 0

    # Sorting points just to feel something (no more abs(x - X))
    for x, y in sorted(pts):
        part1 += solve_fast(x, y, 2, pts)
        part2 += solve_fast(x, y, 10**6, pts)
        pts.remove((x, y))

    return part1, part2

if __name__ == "__main__":
    print(main())

"""
Review:
- i went for dijkstra in part 1 because i thought there would be some more complex pathfinding problem for part 2
- part 2 was like a one line change so that was nice
"""