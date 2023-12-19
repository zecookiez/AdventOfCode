import re

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day19.txt", "r")
    work, parts = file.read().strip().split("\n\n")

    def get_ints(line):
        return list(map(int, re.findall(r"\d+", line)))

    def get_int(line):
        return get_ints(line)[0]

    RULES = {}
    for line in work.split():
        lab, line = line.strip("}").split("{")
        rules = []
        for rule in line.split(","):
            if ":" in rule:
                cond, res = rule.split(":")
                rules.append((cond, res))
            else:
                rules.append(("True", rule))
        RULES[lab] = rules

    def solve(x, m, a, s):
        cur = "in"
        while cur not in "AR":
            for rule in RULES[cur]:
                cond, res = rule
                if eval(cond):
                    cur = res
                    break
        return cur == "A"

    part1 = 0
    for line in parts.split():
        x, m, a, s = get_ints(line)
        if solve(x, m, a, s):
            part1 += x + m + a + s

    def intersect(a, b):
        return max(a[0], b[0]), min(a[1], b[1])

    def construct(cond, val_range):
        num = get_int(cond)
        if "<" in cond:
            return intersect((num, 4000), val_range), intersect((1, num - 1), val_range)
        return intersect((1, num), val_range), intersect((num + 1, 4000), val_range)

    def split(cond, val_ranges):
        bad_ranges = dict(val_ranges)
        bad_ranges[cond[0]], val_ranges[cond[0]] = construct(cond, val_ranges[cond[0]])
        return bad_ranges, val_ranges

    def solve_part2(node, ranges):
        if node == "A":
            prod = 1
            for L, R in ranges.values():
                prod *= (R - L + 1)
            return prod
        if node == "R" or any(L >= R for L, R in ranges.values()):
            return 0
        tot = 0
        for rule in RULES[node]:
            cond, nx_node = rule
            if cond == "True":
                tot += solve_part2(nx_node, ranges)
                break
            ranges, bad_range = split(cond, ranges)
            tot += solve_part2(nx_node, bad_range)
        return tot

    return part1, solve_part2("in", {ch: (1, 4000) for ch in "xmas"})

if __name__ == "__main__":
    print(main())

"""
Review:
- cute eval trick for part 1 but input parsing was a pain
- had some pretty nasty code for part 2, spent a while to clean it up
"""