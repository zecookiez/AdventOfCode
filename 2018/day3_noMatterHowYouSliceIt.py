inputString = ["#1 @ 1,2: 3x4"] # Puzzle input here

puzzle = [map(int, re.findall("\d+", line)) for line in inputString]

def partA(A):
    # No need to actually make a grid, just check if we've already marked that place before
    
    marked = set()
    overlap = set()
    for _, x, y, length, width in A:
        for xPos in range(x, x + length):
            for yPos in range(y, y + width):
                label = xPos * 1000 + yPos
                if label in marked:
                    overlap.add(label)
                else:
                    marked.add(label)
    return overlap


def partB(A, overlaps):
    for request, x, y, length, width in A:
        xCor = [xPos * 1000 for xPos in range(x, x + length)]
        yCor = range(y, y + width)
        if all(xPos + yPos not in overlaps for xPos in xCor for yPos in yCor):
            return request


print(len(partA(puzzle)))
print(partB(puzzle, partA(puzzle)))
