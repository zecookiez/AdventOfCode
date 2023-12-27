from collections import defaultdict
from random import randint

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day25.txt", "r")
    input = [i.strip() for i in file.readlines()]

    adj = defaultdict(list)
    nodes = set()
    for line in input:
        node, neighbors = line.split(":")
        nodes.add(node)
        for nx in neighbors.split():
            adj[node].append(nx)
            nodes.add(nx)
    rencode = list(nodes)
    encode = {node: ind for ind, node in enumerate(rencode)}
    N = len(nodes)
    nadj = [[] for i in range(N)]
    for node, id in encode.items():
        for nx in adj[node]:
            nx = encode[nx]
            nadj[id].append(nx)

    # Dinic Implementation from PyRival
    INF = float("inf")

    class Dinic:
        def __init__(self, n):
            self.lvl = [0] * n
            self.ptr = [0] * n
            self.q = [0] * n
            self.adj = [[] for _ in range(n)]

        def add_edge(self, a, b, c, rcap=0):
            self.adj[a].append([b, len(self.adj[b]), c, 0])
            self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])

        def dfs(self, v, t, f):
            if v == t or not f:
                return f
            for i in range(self.ptr[v], len(self.adj[v])):
                e = self.adj[v][i]
                if self.lvl[e[0]] == self.lvl[v] + 1:
                    p = self.dfs(e[0], t, min(f, e[2] - e[3]))
                    if p:
                        self.adj[v][i][3] += p
                        self.adj[e[0]][e[1]][3] -= p
                        return p
                self.ptr[v] += 1
            return 0

        def calc(self, s, t):
            flow, self.q[0] = 0, s
            for l in range(30, 31):  # l = 30 maybe faster for random data
                while True:
                    self.lvl, self.ptr = [0] * len(self.q), [0] * len(self.q)
                    qi, qe, self.lvl[s] = 0, 1, 1
                    while qi < qe and not self.lvl[t]:
                        v = self.q[qi]
                        qi += 1
                        for e in self.adj[v]:
                            if not self.lvl[e[0]] and (e[2] - e[3]) >> (30 - l):
                                self.q[qe] = e[0]
                                qe += 1
                                self.lvl[e[0]] = self.lvl[v] + 1
                    p = self.dfs(s, t, INF)
                    while p:
                        flow += p
                        p = self.dfs(s, t, INF)
                    if not self.lvl[t]:
                        break
            return flow

    while True:
        src = randint(0, N - 1)
        tgt = randint(0, N - 1)
        d = Dinic(len(nadj))
        for i in range(N):
            for j in nadj[i]:
                d.add_edge(i, j, 1, 1)
        flow = d.calc(src, tgt)
        if flow == 3:
            queue = [src]
            seen = {src}
            for node in queue:
                for nx in d.adj[node]:
                    if nx[2] - nx[3] > 0 and nx[0] not in seen:
                        seen.add(nx[0])
                        queue.append(nx[0])
            return len(seen) * (N - len(seen)), "FILLER"

if __name__ == "__main__":
    print(main())

"""
Review:
- pretty disasterous, i only thought of max flow until it was too late
- also completely forgot networkx exists X_X you get a flow with dinic solution + randomization instead
    -> just flow with a randomly-picked source and target and capacity 1 for edges
    -> max flow / min cut will indicate # of edges required to cut between source and target
    -> every saturated edge will be taken out instead of just 3, so we can count the component size of the source
    
idk this one was pretty bad considering that a lot of people just threw networkx + some graph visualization tool at it
:/ 
"""