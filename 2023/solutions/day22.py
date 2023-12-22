from collections import defaultdict

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day22.txt", "r")
    input = [i.strip() for i in file.readlines()]

    def get_int(line):
        x, y, z = list(map(int, line.split(",")))
        return (x, y, z)

    bricks = []
    for line in input:
        (ax, ay, az), (bx, by, bz) = list(map(get_int, line.split("~")))
        ax, bx = sorted([ax, bx])
        ay, by = sorted([ay, by])
        az, bz = sorted([az, bz])
        bricks.append(((ax, ay, az), (bx, by, bz)))

    # Sort bricks from low to high of the z axis
    # Obviously not good enough to simulate falling
    # ...but it is a very good ordering heuristic for the simulation
    bricks.sort(key=lambda i: (i[0][-1], i[1][-1]))

    # If two intervals intersect
    def inter(l1, r1, l2, r2):
        return max(l1, l2) <= min(r1, r2)

    # If both x and y axis overlap
    def align_xy(a, b):
        for ind in range(2):
            L, R = a[0][ind], a[1][ind]
            l, r = b[0][ind], b[1][ind]
            if max(l, L) > min(r, R): return False
        return True

    # Make everything fall
    def fall(bricks):
        N = len(bricks)
        queue = list(range(N))
        in_queue = set(queue)
        for ind in queue:
            in_queue.remove(ind)
            az, bz = bricks[ind]
            moved = False
            while az > 1:
                if any(max(az - 1, bricks[item][0]) <= min(bz - 1, bricks[item][1]) for item in neighbors[ind]):
                    break
                az -= 1
                bz -= 1
                moved = True
            if moved:
                for nx in neighbors[ind]:
                    if nx not in in_queue:
                        in_queue.add(nx)
                        queue.append(nx)
                bricks[ind] = az, bz
        return bricks

    # Preprocess pairs of bricks that share x and y axis
    neighbors = [
        [i2 for i2, b2 in enumerate(bricks) if i1 != i2 and align_xy(b1, b2)] for i1, b1 in enumerate(bricks)
    ]

    # Fall bricks completely
    bricks = fall([(a[2], b[2]) for a, b in bricks])

    # Find which bricks sit next to each other
    connected = [
        [i2 for i2 in neighbors[i1] if inter(az, bz, bricks[i2][0] - 1, bricks[i2][1] - 1)] for i1, (az, bz) in
        enumerate(bricks)
    ]

    # Prepare degree for topological sort from each respective brick
    in_deg = [0] * len(bricks)
    for ind in range(len(bricks)):
        for ind2 in connected[ind]:
            in_deg[ind2] += 1

    part1 = part2 = 0
    for ind in range(len(bricks)):
        # Remove brick, see which bricks it moves
        queue = [ind]
        deg = defaultdict(int)
        moved = {ind}
        for node in queue:
            for nx in connected[node]:
                deg[nx] += 1
                # Only moves if every other brick it depends on has moved
                if deg[nx] == in_deg[nx]:
                    queue.append(nx)
                    moved.add(nx)
        part2 += len(moved) - 1 # Don't include removed brick
        # No brick moved
        if len(moved) == 1:
            part1 += 1

    return part1, part2

if __name__ == "__main__":
    print(main())

"""
Review:
- part 1 was a disaster, i thought i could get away by generating the full bricks
- then made some off-by-one mistakes
- and my code end up taking 10 minutes in pypy to run for both parts T_T
it is now 2am and my code is finally <5 seconds in python
its so over 
"""