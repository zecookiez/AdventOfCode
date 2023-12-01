import re
from time import time

t0 = time()

# Parse the input (Just copy and paste it into a txt file)

parsed = open("puzzle.txt")
arr = []
first_half = 0
index = 0

for line in parsed:
    if len(line) > 2:
        index += 1
        if "After" in line:
            first_half = index
        arr.append(list(map(int, re.findall("\d+", line[:-1]))))
puzzleA, puzzleB = arr[:first_half], arr[first_half:]

def chronal_classification(inputA, inputB):

    # Part A is just bruteforce, O(n), n being the number of samples
    # Part B's logical deductions take a bit more time, O(n^3) but runs much better on average. I based it off of the "relax-an-edge" approach in the Bellman-ford algorithm.
    #  n in this case is the number of operations [bounded by 16 so technically it is O(n) :p]
    # Time: ~100ms
    
    # Used eval() to maky my code much cooler and shorter, don't use this with professional code, you never know what could be hiding in the inputs :)
    
    ambiguous = 0
    operations = {"register_a+b", "register_a+register_b", "register_a*b", "register_a*register_b", "register_a&b", "register_a&register_b", "register_a|b", "register_a|register_b", "register_a", "a", "a>register_b", "register_a>b", "register_a>register_b", "a==register_b", "register_a==register_b", "register_a==b"}
    freq = [set() for i in range(16)]
    
    for instructions in range(0, len(input), 3):
    
        before = input[instructions]
        op_id, a, b, c = input[instructions + 1]
        after = input[instructions + 2]

        # Set variables for the eval
        register_a = before[a]
        register_b = before[b]

        potential = set()
        for op in operations:
            if eval(op) == after[c]:
                potential.add(op)
                
        freq[op_id] |= potential
        ambiguous += len(potential) >= 3

    print("Part A: %d" % ambiguous)

    # Working out the mapping of each opcode
    while operations:
        for potential_ops in freq:
            if len(potential_ops) == 1 and operations & potential_ops:
                operations -= potential_ops
                freq = [ops - potential_ops or ops for ops in freq]

    return partB([min(op) for op in freq], inputB)

def partB(mapping, input):

    after = [0, 0, 0, 0]
    for op, a, b, c in input:
        # Set variables for eval
        register_a = after[a]
        register_b = after[b]
        after[c] = eval(mapping[op])
        
    return after[0]

print("Part B: %d" % chronal_classification(puzzleA, puzzleB))
print("Time: %d ms" % (1000 * (time() - t0)))
