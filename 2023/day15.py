file = open("inputs/day15.txt", "r")
input = [i.strip() for i in file.readlines()]

part1 = 0
part2 = 0
lens = [[] for _ in range(256)]

def hash(st):
    val = 0
    for ch in st:
        val = (val + ord(ch)) * 17 % 256
    return val

for line in input:
    tok = line.split(",")
    for i in tok:
        part1 += hash(i)
        dash = "-" in i
        if "=" in i:
            i, num = i.split("=")
        else:
            i = i[:-1]
        hashval = hash(i)
        if dash:
            lens[hashval] = [(label, val) for label, val in lens[hashval] if label != i]
        else:
            for ind, (label, val) in enumerate(lens[hashval]):
                if label == i:
                    lens[hashval][ind] = i, int(num)
                    break
            else:
                lens[hashval].append((i, int(num)))

for ind, box in enumerate(lens, 1):
    for ind2, (_, num) in enumerate(box, 1):
        part2 += ind * ind2 * num

print(part1)
print(part2)

"""
Review:
- was videocalling someone while doing today, it was so doomed
- part 1 i thought the = and - meant something (it didnt)
- part 2 sucks its all reading and example guessing
"""