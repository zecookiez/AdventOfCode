
# Problem description @ https://adventofcode.com/2018/day/1

puzzle = map(int, open("inputs/day01.txt"))

def partA(s):
    return sum(s)

def partB(s):
    seen = {0}
    a = 0
    while True:
        for i in s:
            a += i
            if a in seen:
                return a
            seen.add(a)

print(partA(puzzle))
print(partB(puzzle))
