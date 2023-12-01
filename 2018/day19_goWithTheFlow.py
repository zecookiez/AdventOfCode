import re
from time import  time

t0 = time()
puzzle = [[line[:4]] + map(int, re.findall("\d+", line[:-1])) for line in open("day19.txt")]

def go_with_the_flow(inp, part2 = False):

    after = [part2, 0, 0, 0, 0, 0]
    l = inp.pop(0)[-1]
    iterations = 0
    while len(inp) > after[l] > -1:
        line, a, b, c = inp[after[l]]
        if "setr" == line:
            after[c] = after[a]
        elif "seti" == line:
            after[c] = a
        elif "addi" == line:
            after[c] = after[a] + b
        elif "addr" == line:
            after[c] = after[a] + after[b]
        elif "muli" == line:
            after[c] = after[a] * b
        elif "mulr" == line:
            after[c] = after[a] * after[b]
        elif "gtrr" == line:
            after[c] = after[a] > after[b]
        elif "eqrr" == line:
            after[c] = after[a] == after[b]
        after[l] += 1
        iterations += 1
        if iterations >= 30 and part2:
            return sum(d for d in xrange(1, after[3] + 1) if after[3] % d == 0)
    return after[0]

print("Part A: %d" % go_with_the_flow(puzzle[:]))
print("Part B: %d" % go_with_the_flow(puzzle, True))
print("Time: %d ms" % (1000*(time() - t0)))
