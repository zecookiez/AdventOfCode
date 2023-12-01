t0 = time()
puzzle = 7165

def chronalCharge(serial):

    # Preprocess a table of partial sums, then bruteforce on it. O(N^3) algorithm, where N is the side length
    # Time: 147 ms

    grid = [[0] * 301 for row in range(301)]
    for x in range(1, 301):
        for y in range(1, 301):
            rID = x + 10
            power = rID * y + serial
            level = power * rID // 100 % 10 - 5
            grid[x][y] = level + grid[x - 1][y] + grid[x][y - 1] - grid[x - 1][y - 1]
            #
            # Goal: grid[row][col] notates the sum of all coordinates left and up of (row, col) inclusive
            #
            # Example: For row=3, col=5 (Every value represents its frequency)
            #    2 2 2 2 1
            #    2 2 2 2 1
            #    1 1 1 1 X
            # To get grid[row][col], we combine grid[row - 1][col] and grid[row][col - 1]
            # This creates an overlap at (row - 1, col - 1), so we subtract it by grid[row - 1][col - 1]
            # We use this idea to implement the square size sums later too

    def getHighest(size):
        highest = -1e9, -1, -1, -1
        for x in range(size, 301):
            for y in range(size, 301):
                val = grid[x][y] - grid[x - size][y] - grid[x][y - size] + grid[x - size][y - size]
                # Same concept.
                # Example: For row=3, col=5, size=2 (Every value represents its frequency)
                #    2 2 2 1 1
                #    1 1 1 X X
                #    1 1 1 X X
                # To get the sum, we perform the same similar set of operations to isolate the square
                highest = max((val, x - size + 1, y - size + 1, size), highest)
        return highest

    print("Part A: %d,%d" % getHighest(3)[1:3])
    print("Part B: %d,%d,%d" % max(map(getHighest, range(1, 301)))[1:])

chronalCharge(puzzle)
print("Time: %d ms" % (1000 * (time() - t0))) # ~147ms
