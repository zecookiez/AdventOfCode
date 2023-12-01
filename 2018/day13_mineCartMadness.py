from time import time

t0 = time()
puzzle = [line[:-1] for line in open("puzzle.txt")]

def subterraneanSustainability(grid):
    # Simulation of the entire process
    # O(n^2 * k), n being the number of carts on the map and k being the number of rounds simulated.
    # Time: ~120ms
    def build(track):
        carts = []
        grid = [list(i) for i in track]
        cartID = 0
        for x, row in enumerate(track):
            for y, col in enumerate(row):
                if col in ">v^<":
                    carts.append([x, y, col, str(cartID)])
                    cartID += 1
                    if col in "><":
                        d = "-"
                    elif col in "^v":
                        d = "|"
                    grid[x][y] = d
        return carts, grid

    carts, grid = build(grid)
    directions = {cart[-1]: 0 for cart in carts}
    removed = set()
    firstCollision = True
    DIRECTION = {"^": [-1, 0],
                 "v": [1, 0],
                 "<": [0, -1],
                 ">": [0, 1]}

    while len(carts) > 1:
        newCarts = []
        currentCarts = carts[:]
        cartPosition = 0
        for x, y, d, cartID in carts:
            # Update coordinates
            mx, my = DIRECTION[d]
            x += mx
            y += my
            # Change directions
            if grid[x][y] == "\\":
                d = dict([["v", ">"], ["^", "<"], [">", "v"], ["<", "^"]])[d]
            elif grid[x][y] == "/":
                d = dict([["v", "<"], ["^", ">"], [">", "^"], ["<", "v"]])[d]
            elif grid[x][y] == "+":
                left = dict([["v", ">"], ["^", "<"], [">", "^"], ["<", "v"]])[d]
                right = dict([["v", "<"], ["^", ">"], [">", "v"], ["<", "^"]])[d]
                d = (left + d + right)[directions[cartID] % 3]
                directions[cartID] += 1
            # Check for collisions
            for cartB in currentCarts:
                if cartB[-1] in removed or cartID in removed or cartB[-1] == cartID:
                    continue
                if cartB[:2] == [x, y]:
                    removed |= {cartID, cartB[-1]}
                    if firstCollision:
                        firstCollision = False
                        print("Part A: %d,%d" % (y, x))
            if cartID not in removed:
                newCarts.append([x, y, d, cartID])
            currentCarts[cartPosition] = [x, y, d, cartID]
            cartPosition += 1
        # Update the carts to next round, sort to keep intended processing order
        carts = sorted(newCarts)
    return [[cart[1], cart[0]] for cart in newCarts if cart[-1] not in removed][0]

print("Part B: %d,%d" % tuple(subterraneanSustainability(puzzle)))
print("Time: %d ms" % (1000 * (time() - t0)))
