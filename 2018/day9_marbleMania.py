from collections import deque
from time import time

t0 = time()
puzzle = 486, 70833

# My original solution used a linked list solution, but then I remembered that Python's deque is exactly what I needed.

def marbleMania(elfs, finalMarble):
    marbles = deque([0])
    players = [0] * elfs
    for mar in range(1, finalMarble + 1):
        if mar % 23 == 0:
            marbles.rotate(7) # Find the mmarbles 7 positions back
            players[mar % elfs] += mar + marbles.pop() # Take it out
            marbles.rotate(-1) # Shift to current marble
        else:
            marbles.rotate(-1) # Shift to position
            marbles.append(mar) # This is the current marble now
    return max(players)

print(marbleMania(*puzzle), marbleMania(486, 7083300))
print("Time: %d ms" % (1000 * time() - 1000 * t0)) # ~780 ms
