from heapq import heappush, heappop

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day17.txt", "r")
    grid = [list(map(int, row.strip())) for row in file.readlines()]
    H, W = len(grid), len(grid[0])

    def solve(min_turn, max_length):
        queue = [(0, 0, 0, 0, 1, 0), (0, 0, 0, 1, 0, 0)]
        dist = {}

        def add(nd, nx, ny, dx, dy, sz):
            label = nx, ny, dx, dy, sz
            if label in dist and dist[label] <= nd:
                return
            if sz > max_length:
                return
            dist[label] = nd
            heappush(queue, (nd, nx, ny, dx, dy, sz))
            return

        left = lambda dx, dy: (-dy, dx)
        right = lambda dx, dy: (dy, -dx)

        while queue:
            d, x, y, dx, dy, sz = heappop(queue)
            if (x, y, dx, dy, sz) in dist and dist[x, y, dx, dy, sz] < d:
                continue
            moves = [((dx, dy), sz + 1)]
            if sz >= min_turn:
                moves.extend([(left(dx, dy), 1), (right(dx, dy), 1)])
            for (ndx, ndy), nsz in moves:
                nx = ndx + x
                ny = ndy + y
                if 0 <= nx < H and 0 <= ny < W:
                    add(d + grid[nx][ny], nx, ny, ndx, ndy, nsz)

        return min(val for key, val in dist.items()
                   if key[:2] == (H - 1, W - 1) and min_turn <= key[-1] <= max_length)

    return solve(0, 3), solve(4, 10)

if __name__ == "__main__":
    print(main())

"""
Review:
- spent half of my time debugging part 1 T_T
- also spent too much time looking at the flavourtext edge case despite not mattering in the end
  is it bad input design? was it supposed to matter? who knows and its a bit disappointing
- i also need to optimize this code

its so over
"""