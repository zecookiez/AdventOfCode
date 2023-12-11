import re
from collections import defaultdict

def GI(line):
    return int(re.findall(r"\d+", line)[0])

file = open("inputs/day2.txt", "r")
input = [i.strip() for i in file.readlines()]

part1 = 0
part2 = 0
R, G, B = "red green blue".split()
for line in input:
    _, line = line.split(":")
    # Maximum amount of balls per colour across all draws
    cnts = defaultdict(int)
    is_possible = True
    for draws in line.split(";"):
        # Parse one draw into their colour->quantity mapping
        cur_cnt = defaultdict(int)
        for draw in draws.split(", "):
            quantity, colour = draw.split()
            cur_cnt[colour] = int(quantity)
        is_possible &= cur_cnt[R] <= 12 and cur_cnt[G] <= 13 and cur_cnt[B] <= 14
        # Keep track of maximum amount per colour
        for colour, quantity in cur_cnt.items():
            cnts[colour] = max(cnts[colour], quantity)
    if is_possible:
        part1 += GI(_) # get index
    part2 += cnts[R] * cnts[G] * cnts[B]

print(part1)
print(part2)

"""
Review:
- Wild input parsing work, was not clean at all 
- part 2 was okay but did not save me from the part 1 input parsing disaster

:///// it's so so over
"""