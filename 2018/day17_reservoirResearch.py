import re
from time import  time

t0 = time()
grid = defaultdict(bool)
for line in open("puzzle.txt"):
    a, b_lower, b_upper = map(int, re.findall("\d+", line))
    is_horizontal = line[0] == "x"
    for p in range(b_lower, b_upper + 1):
        grid[(a, p) if is_horizontal else (p, a)] = True

y_lower = min(grid, key = lambda pos: pos[1])[1]
y_upper = max(grid, key = lambda pos: pos[1])[1]

def reservoir_research(grid):

    # Recursive approach, fill container if we're sure that's an actual container (Deals nested container case very nicely)
    # If level y is safe, then fill both sides as water
    # Complexity: O(nm), n is depth of the ground, m is width of the area

    still_water = set()
    moving_water = set()

    def helper(x, y, direction = "D"):

        # Going either down, left, or right
        moving_water.add((x, y))

        # Haven't touched a surface yet
        if not grid[x, y + 1]:
            if (x, y + 1) not in moving_water and y < y_upper:
                helper(x, y + 1) # Keep going
            if (x, y + 1) not in still_water:
                return False # Found water, stop

        # If the left side is safe
        is_left_filled = grid[x - 1, y] or (x - 1, y) not in moving_water and helper(x - 1, y, "L")

        # If the right side is safe
        is_right_filled = grid[x + 1, y] or (x + 1, y) not in moving_water and helper(x + 1, y, "R")

        if direction == "D" and is_left_filled and is_right_filled:

            # It's safe, mark everything as water \o/
            left = x - 1
            right = x + 1

            still_water.add((x, y))

            while (left, y) in moving_water:
                still_water.add((left, y))
                left -= 1
            while (right, y) in moving_water:
                still_water.add((right, y))
                right += 1

        if direction == "L":
            return is_left_filled or grid[x - 1, y]

        elif direction == "R":
            return is_right_filled or grid[x + 1, y]

        return False

    helper(500, 0)

    print('Part A: %d' % (len(moving_water | still_water) - y_lower))
    return len(still_water)

print("Part B: %d" % reservoir_research(grid))
print("Time: %d ms" % (1000*(time() - t0)))
