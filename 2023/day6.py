import re
from math import ceil

def get_int(line):
    return list(map(int, re.findall(r"\d+", line)))

file = open("input.txt", "r")
times, dist = [i.strip() for i in file.readlines()]

def solve(times, distances):
    prod = 1
    for t, d in zip(get_int(times), get_int(distances)):
        #good_hold = 0
        #for hold in range(t + 1):
        #    if hold * t - hold * hold > d:
        #        good_hold += 1
        # Solving the number of integer solutions where x*t - x^2 - d > 0
        # x^2 - xt + d < 0
        # range between zeroes is (t +/- sqrt(t^2 - 4d)) / 2

        # Normally I would check if range fits between [0, t] but looking at the puzzle inputs this is fine
        discr = pow(t * t - 4 * d, 0.5)
        x0 = int(ceil((t - discr) * 0.5))
        x1 = int((t + discr) * 0.5)
        prod *= x1 - x0 + 1
    return prod

# Part 1
print(solve(times, dist))

# Part 2
print(solve(times.replace(" ", "")), dist.replace(" ", ""))


"""
Review:
- im too slow :skull:
- tried to cheese by running my slow solution in pypy, but I forgot to put in the input
- ended up wasting my time writing a binary search that didn't work 
    - (it's been a long day I realized after that it wouldn't even work)

too slow for easy problems and too dumb for hard problems
=> conclusion: its so over
"""