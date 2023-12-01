
# Problem description @ https://adventofcode.com/2018/day/2

puzzle = [line[:-1] for line in open("day02.txt")]

def partA(strings):
    twoChars = 0
    threeChars = 0
    for line in strings:
        mapping = [0] * 130
        for value in map(ord, line):
            d[value] += 1
        twoChars += 2 in mapping
        threeChars += 3 in mapping
    return twoChars * threeChars


def partB(strings):
    # O(nk), where k is the length of each string
    # This is better than the standard O(n^2 * k) bruteforce but isn't required for this problem.
    seen = set()
    for line in strings:
        for pos in range(len(line)):
            if pos == 0 or line[pos] != line[pos - 1]: # Prevents returning a false positive where two neighboring characters are identical
                newLine = line[:pos] + line[pos + 1:]
                if newLine in seen:
                    return newLine
                seen.add(newLine)

print(partA(puzzle))
print(partB(puzzle))
