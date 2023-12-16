from math import lcm
from collections import defaultdict

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day8.txt", "r")
    input = file.read().strip().split("\n\n")

    inst, nodes = input
    adj = defaultdict(list)
    for line in nodes.split("\n"):
        node, _, L, R = line.split()
        adj[node] = L[1:-1], R[:-1]

    def solve(node, end_cond):
        cur = node
        pt = 0
        while end_cond(cur):
            nxt = inst[pt % len(inst)]
            cur = adj[cur][nxt == "R"]
            pt += 1
        return pt

    # Since it's all simultaneous, solve each part individually
    # Then combine results as lowest common multiple between all integers

    part2 = 1
    for node in adj:
        if node[-1] == "A":
            part2 = lcm(part2, solve(node, lambda node: node[-1] != "Z"))

    return solve("AAA", lambda node: node != "ZZZ"), part2

if __name__ == "__main__":
    print(main())

"""
Review:
- lost some time on input for part 1 (i forgot to do .split("\n") again)
- part 2 wasnt great either (implemented the slow way, only thought of lcm after), but i still somehow found some points
"""