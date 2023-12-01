from time import time

t0 = time()
puzzle = "####..##.##..##..#..###..#....#.######..###########.#...#.##..####.###.#.###.###..#.####..#.#..##..#"
puzzle1 = {line[:5] for line in list(open("puzzle.txt"))[2:] if line[-2] == "#"}

def subterraneanSustainability(serial, pattern, certainty = 300):

    def countPots(state):
        return sum(index - negative for index, pot in enumerate(state) if pot == "#")

    def nextState(pattern):
        paddedPattern = "..%s.." % pattern
        backExtend = frontExtend = ""
        if ("..." + pattern[:2]) in serial:
            frontExtend = "#"
            global negative
            negative += 1
        if (pattern[-2:] + "...") in serial:
            backExtend = "#"
        pattern = frontExtend + "".join(
            ".#"[paddedPattern[n:n + 5] in serial] for n in range(len(pattern))) + backExtend
        return pattern
        
    # At some point they're going to start repeating over and over again, so I took the average of the last 100 states and extrapolated the data :)
    # This is about O(n * k), where n is the length of the pattern and k is the number of generations
    
    global negative
    negative = 0
    previous = countPots(pattern)
    difference = []
    left = 50000000000 - certainty
    for generation in range(certainty):
        pattern = nextState(pattern)
        pots = countPots(pattern)
        difference.append(pots - previous)
        if len(difference) > 100:
            difference.pop(0)
        elif len(difference) == 20:
            print("Part A: %d" % pots)
        previous = pots
    return pots + sum(difference) // len(difference) * left

print("Part B: %d" % subterraneanSustainability(puzzle1, puzzle))
print("Time: %d ms" % (1000 * (time() - t0))) # ~45 ms
