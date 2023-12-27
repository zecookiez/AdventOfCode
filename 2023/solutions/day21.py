
def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day21.txt", "r")
    grid = [i.strip() for i in file.readlines()]

    def part2(seq, qt):
        diff1 = seq[1] - seq[0]
        diff2 = seq[2] - seq[1]
        diff = diff2 - diff1
        tot = seq[2] + diff2 * (qt - 1) + diff * qt * (qt - 1) // 2
        return tot

    N = len(grid)
    TILED = 10
    SZ = N * TILED
    LIM = 26501365
    for i in range(N):
        for j in range(N):
            if grid[i][j] != "S": continue
            queue = 1 << ((i + TILED // 2 * N) * SZ + j + TILED // 2 * N)
            seq = []
            grid = int(
                "".join(row * TILED for row in grid).replace("S", "1").replace(".", "1").replace("#", "0") * TILED, 2)
            for step in range(1, LIM):
                queue = ((queue >> 1) | (queue << 1) | (queue >> SZ) | (queue << SZ)) & grid
                if step == 64:
                    part1 = queue.bit_count()
                if step % N == LIM % N:
                    seq.append(queue.bit_count())
                    if len(seq) >= 3:
                        return part1, part2(seq, (LIM - step) // N + 1)

if __name__ == "__main__":
    print(main())

"""
Review:

will optimize this later, but its unlikely we can do part 2 quickly in the general form unless input is hardcoded
    - nevermind bitmask saves the day :D this is one of the bitmask optimizations of all time

- part 1 is okay, but i was too much of a coward to submit without testing the example
    - that could absolutely be faster..
- part 2 was a disaster, this one was a bit too analytical T_T

its so over 
"""