from time import time
import re

t0 = time()
puzzle = [re.findall("(?i)step (\w)", line[:-1]) for line in open("puzzle.txt")]

def performInstructions(puzzle, numberOfWorkers = 1):
    graph = ddict(list)
    freq = ddict(int)

    for src, target in puzzle:
        graph[src].append(target)
        graph[src].sort()
        freq[target] += 1

    queue = []
    order = []
    workers = []
    totalTime = 0

    for node in graph:
        if freq[node] == 0:
            order.append(node)
            workers.append((ord(node) - 4, node))

    while workers or queue:
        label = totalTime, node = min(workers)
        workers.remove(label)
        for destination in graph[node]:
            freq[destination] -= 1
            if freq[destination] == 0:
                queue.append(destination)
        while len(workers) < numberOfWorkers and queue:
            task = min(queue)
            order.append(task)
            queue.remove(task)
            workers.append((totalTime + ord(task) - 4, task))

    return totalTime, "".join(order)

print("Part A: %s" % performInstructions(puzzle)[1])
print("Part B: %d seconds" % performInstructions(puzzle, 5)[0])
print("Time: %d ms" % (1000 * time() - 1000 * t0))
