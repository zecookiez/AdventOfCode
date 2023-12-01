from time import time

puzzle = [(81, 157), (209, 355), (111, 78), (179, 211), (224, 268), (93, 268), (237, 120), (345, 203), (72, 189), (298, 265), (190, 67), (319, 233), (328, 40), (323, 292), (125, 187), (343, 186), (46, 331), (106, 350), (247, 332), (349, 145), (217, 329), (48, 177), (105, 170), (257, 166), (225, 113), (44, 98), (358, 92), (251, 209), (206, 215), (115, 283), (206, 195), (144, 157), (246, 302), (306, 157), (185, 353), (117, 344), (251, 155), (160, 48), (119, 131), (343, 349), (223, 291), (256, 89), (133, 96), (240, 271), (322, 73), (324, 56), (149, 272), (161, 107), (172, 171), (301, 291)]

t0 = time()
minX = minY = 1e9
maxX = maxY = -1

# Smallest bounding box
for i, j in puzzle:
    minX = min(minX, i)
    maxX = max(maxX, i)
    minY = min(minY, j)
    maxY = max(maxY, j)

grid = {i: [0,0] for i in puzzle}
region = 0
squareLabel = 0

# Build two squares: one is the bounding box, the other is slightly larger (For the sake of part B I've made that size for completedness)
# If the two areas don't match up, then that point has an infinite area
# Total time complexity: O(n * m * k), n and m being the size of the box respectively, and k being the number of points

for square in [0, 10000 // len(puzzle) + 1]:
    for x in range(minX - square, maxX + square + 1):
        for y in range(minY - square, maxY + square + 1):
            area = float("Inf"), -1
            sumDists = 0
            for xPos, yPos in puzzle:
                dist = abs(x - xPos) + abs(y - yPos)
                if dist < area[0]:
                    area = dist, (xPos, yPos)
                    equal = 0
                elif dist == area[0]:
                    equal = 1
                sumDists += dist
            if equal == 0:
                grid[area[1]][squareLabel] += 1
            if squareLabel == 1 and sumDists < 10000:
                region += 1
    squareLabel = 1

print("Part A: %d" % max(squareA for squareA, squareB in grid.values() if squareA == squareB))
print("Part B: %d" % region)
print("Time taken: %d ms" % (1000 * time() - 1000 * t0))
