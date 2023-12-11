from math import lcm
import re

file = open("inputs/day9.txt", "r")
input = [i.strip() for i in file.readlines()]

def gi(line):
    return list(map(int, re.findall(r"-?\d+", line)))

part1 = 0
part2 = 0

# Get the difference array
diff = lambda a: [i - j for i, j in zip(a[1:], a)]

def solve(grid, mult):
    grid[-1].append(0)
    for ind in range(len(grid) - 2, -1, -1):
        grid[ind].append(grid[ind][-1] + grid[ind + 1][-1] * mult)
    return grid[0][-1]

for line in input:
    arr = gi(line)
    grid = [arr]
    while any(grid[-1]):
        grid.append(diff(grid[-1]))
    # I guess one small optimization is that you can use the same resulting grid for both parts
    part1 += solve(grid, 1)
    part2 += solve([i[::-1] for i in grid], -1)

print(part1)
print(part2)

"""
Review:
- yippee for some points, this is surprisingly tame i thought they would force some optimization?
- lost some time on part 2 because i dont know how to extrapolate backwards :|
"""