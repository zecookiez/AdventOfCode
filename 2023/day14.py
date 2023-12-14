file = open("inputs/day14.txt", "r")
grid = [list(i.strip()) for i in file.readlines()]

def tilt_north(grid):
    H, W = len(grid), len(grid[0])
    for i in range(1, H):
        for j in range(W):
            if grid[i][j] != "O": continue
            row = i
            while row and grid[row - 1][j] == ".":
                grid[row][j] = "."
                row -= 1
                grid[row][j] = "O"
    return grid

def load(grid):
    return sum((len(grid) - i) * row.count("O") for i, row in enumerate(grid))

def cycle_solve(grid, LIM):
    state = {}
    ind = 0
    while ind < LIM:
        # Rotate four times, each using part 1's tilt method by rotating the grid
        for _ in range(4):
            grid = tilt_north(grid)
            grid = list(map(list, zip(*grid[::-1])))
        label = "".join(map("".join, grid))
        if label in state:
            left = LIM - ind
            LIM = ind + left % (ind - state[label])
        else:
            state[label] = ind
        ind += 1
    return load(grid)

print(load(tilt_north(grid[:])))
print(cycle_solve(grid, 1000000000))

"""
Review:
- part 1 was kinda slow to understand
- part 2 was ok, i still suck at these kind of problem so i should write a template function of this for next year..
"""