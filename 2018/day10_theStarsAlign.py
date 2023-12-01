from time import time

t0 = time()
puzzle = [map(int, re.findall("\-?\d+", line[:-1])) for line in open("puzzle.txt")]

def starsAlign(points):

    def calc(second):
        # Calculates area of bounding box
        xPos = sorted(x + second * mx for x, y, mx, my in points)
        yPos = sorted(y + second * my for x, y, mx, my in points)
        return (xPos[-1] - xPos[0]) * (yPos[-1] - yPos[0]), xPos[0], xPos[-1], yPos[0], yPos[-1]

    # Time finder, just a binary search to find the bottom of the curve
    # Our heuristic here is to find the time where the area of the stars is minimal
    lower = 0
    upper = 100000
    while upper - lower > 1:
        mid = upper + lower >> 1
        if calc(mid) < calc(mid + 1):
            upper = mid
        else:
            lower = mid

    # Build the specific frame
    _, startX, endX, startY, endY = calc(upper)
    grid = [[" "]*(endX - startX + 1) for r in range(endY - startY + 1)]
    for x, y, mx, my in points:
        grid[y + my * upper - startY][x + mx * upper - startX] = "*"

    for row in grid:
        print("".join(row))

    return "Message at %d seconds" % upper #~32ms



print(starsAlign(puzzle))
print("Time: %d ms" % (1000 * (time() - t0)))
