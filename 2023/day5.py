import re
from collections import defaultdict

def get_int(line):
    return list(map(int, re.findall(r"\d+", line)))

file = open("inputs/day5.txt", "r")
input = file.read().strip().split("\n\n")

part1 = float("inf")
part2 = float("inf")
seeds = input.pop(0)
mappings = defaultdict(list)
pairs = defaultdict(list)
for map1 in input:
    name, *map1 = map1.split("\n")
    tagA, _, tagB = name.split()[0].split("-")
    pairs[tagA].append(tagB)
    for line in map1:
        a, b, sz = get_int(line)
        mappings[tagA, tagB].append((b, sz, a - b))

def intersect(L1, R1, L2, R2):
    return max(L1, L2), min(R1, R2)

# Solve for a given range instead of a single element
# We don't need to memoize since there's only a few layers of mapping (< 20)
def helper_range(t, L, R):
    if t == "location":
        # Directly return the lowest one in our range
        return L
    best = 10**18
    for nxt_t in pairs[t]:
        ranges_left = [(-1, L - 1), (R + 1, float("inf"))]
        for start, sz, delta in mappings[t, nxt_t]:
            # if (start, start + sz - 1) intersects (L, R)
            new_L, new_R = intersect(L, R, start, start + sz - 1)
            if new_L <= new_R:
                best = min(best, helper_range(nxt_t, new_L + delta, new_R + delta))
                ranges_left.append((new_L, new_R))
        ranges_left.sort()
        # Get all ranges in between the ones already covered
        for ind in range(1, len(ranges_left)):
            (L1, R1), (L2, R2) = ranges_left[ind - 1], ranges_left[ind]
            # Grab the range in between R1 and L2
            if L2 - R1 >= 2:
                best = min(best, helper_range(nxt_t, R1 + 1, L2 - 1))
    return best

seed_arr = get_int(seeds)
for seed in seed_arr:
    part1 = min(part1, helper_range("seed", seed, seed))

for ind in range(0, len(seed_arr), 2):
    L, sz = seed_arr[ind:ind+2]
    part2 = min(part2, helper_range("seed", L, L + sz - 1))

print(part1)
print(part2)

"""
Review:
- had a bad time understanding how the mapping ranges worked for part 1
- ...and also found a bug in my input parser during testing 
- part 2 was okay given that i went up 900 spots so i can't even be mad about it :(

it's so over
"""