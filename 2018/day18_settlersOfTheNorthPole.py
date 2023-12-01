from time import  time

t0 = time()
puzzle = ["B"*52] + ["B%sB" % line[:-1] for line in open("day18.txt")] + ["B"*52]

# Wrapped the grid with B to ensure that no out-of-bound indexing is happening

# Bruteforce simulation, simulating every minute takes O(nm) time
# This is similar to those cellular automata simulations, so I expected some looping for part 2.
#   Keeping track of every state until I hit a duplicate, then I shift the offset to get the final answer.
#   Part B will then take O(nm * k), k being the number of minutes

def settlers_of_the_north_pole(grid, minutes = 500):

    vis = {}
    total = 1000000000

    for minute in range(minutes):

        grid = simulate(grid)
        state = str(grid)

        if state in vis: # Pattern is looping!
            total = (total - vis[state] - 1) % (minute - vis[state])
            return settlers_of_the_north_pole(grid, total)

        vis[state] = minute

        if minute == 9 and minutes == 500:
            print("Part A: %d" % (state.count("|") * state.count("#")))

    return state.count("|") * state.count("#")

def simulate(grid):

    new_grid = [list(i) for i in grid]
    for x, r in enumerate(grid):
        for y, c in enumerate(r):
            if c == "B":
                continue
                
            adj = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1],
                   [x,     y - 1],             [x,     y + 1],
                   [x + 1, y - 1], [x + 1, y], [x + 1, y + 1]]
            freq = {".": 0, "|": 0, "#": 0, "B": 0}
            for a, b in adj:
                freq[grid[a][b]] += 1

            if c == ".":
                if freq["|"] >= 3:
                    new_grid[x][y] = "|"

            elif c == "|":
                if freq["#"] >= 3:
                    new_grid[x][y] = "#"

            else:
                if freq["#"] < 1 or 1 > freq["|"]:
                    new_grid[x][y] = "."

    return new_grid
    
print("Part B: %d" % settlers_of_the_north_pole(puzzle))
print("Time: %d ms" % (1000*(time() - t0)))
