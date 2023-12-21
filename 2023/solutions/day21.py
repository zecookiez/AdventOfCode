
def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day21.txt", "r")
    grid = [i.strip() for i in file.readlines()]

    H, W = len(grid), len(grid[0])

    def part2(seq, qt):
        diff1 = seq[1] - seq[0]
        diff2 = seq[2] - seq[1]
        diff = diff2 - diff1
        tot = seq[2] + diff2 * (qt - 1) + diff * qt * (qt - 1) // 2
        return tot

    def neigh4(x, y):
        for nx, ny in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            yield (nx, ny)

    LIM = 26501365
    for i in range(H):
        for j in range(W):
            if grid[i][j] != "S": continue
            queue = [(i, j)]
            seq = []
            for step in range(1, LIM):
                nq = []
                seen = set()
                for x, y in queue:
                    for nx, ny in neigh4(x, y):
                        if grid[nx % H][ny % W] != "#" and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            nq.append((nx, ny))
                queue = nq[:]
                if step == 64:
                    part1 = len(queue)
                if step % H == LIM % H:
                    seq.append(len(queue))
                    if len(seq) >= 3:
                        return part1, part2(seq, (LIM - step) // H)

if __name__ == "__main__":
    print(main())

"""
Review:

will optimize this later, but its unlikely we can do part 2 quickly in the general form unless input is hardcoded

- part 1 is okay, but i was too much of a coward to submit without testing the example
    - that could absolutely be faster..
- part 2 was a disaster, this one was a bit too analytical T_T

its so over 
"""