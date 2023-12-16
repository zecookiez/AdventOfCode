from collections import defaultdict

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day3.txt", "r")
    grid = [i.strip() for i in file.readlines()]

    def neigh8(x, y, H, W):
        for nx, ny in (x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1):
            if 0 <= nx < H and 0 <= ny < W:
                yield (nx, ny)

    part1 = 0
    part2 = 0

    H = len(grid)
    W = len(grid[0])
    seen = set()
    gears = defaultdict(list)
    for r_ind, row in enumerate(grid):
        for c_ind in range(W):
            if not row[c_ind].isdigit():
                continue
            # Expand to find the full number
            R = c_ind
            while R + 1 < W and row[R + 1].isdigit():
                R += 1
            # Do not repeat the same number
            if (r_ind, R) in seen:
                continue
            seen.add((r_ind, R))
            num = int(row[c_ind:R+1])
            is_adj = False
            gear_pos = set()
            for y in range(c_ind, R + 1):
                for nx, ny in neigh8(r_ind, y, H, W):
                    if grid[nx][ny] != "." and not grid[nx][ny].isdigit():
                        is_adj = True
                    if grid[nx][ny] == "*":
                        gear_pos.add((nx, ny))
            if is_adj:
                part1 += num
            # Map numbers to their gears
            for pos in gear_pos:
                gears[pos].append(num)

    part2 = sum(val[0] * val[1] for val in gears.values() if len(val) == 2)

    return part1, part2

if __name__ == "__main__":
    print(main())

"""
Review:
- had a clear idea of what to do from the start
- boilerplate code for grabbing adjacent cells came in handy, getting big value from it

we are so back (for one day)
"""