
file = open("input.txt", "r")
input = [i.strip() for i in file.readlines()]

# Starting off strong with the ugliest code for a day 1

part1 = 0
part2 = 0
num = "_ one two three four five six seven eight nine".split()
for line in input:
    # Find indices of digits and words, sort, then grab the first + last one
    indices = [(ind, int(ch)) for ind, ch in enumerate(line) if ch.isdigit()]
    part1 += indices[0][1] * 10 + indices[-1][1]
    # Find all positions of that word (spent 10 minutes debugging a case where one .find was not enough :sob:)
    for val, word in enumerate(num):
        for start in range(len(line) - len(word) + 1):
            if line.find(word, start) == start:
                indices.append((start, val))
    indices.sort()
    part2 += indices[0][1] * 10 + indices[-1][1]

print(part1)
print(part2)

"""
Review:
- Almost had part 1 instantly, died because first could be last as well and scratched my head against my first line of input :/
- Threw part 2 as well by attempting multiple strategies before settling on the .find strategy
- Threw even more time in part 2 by attempting to call .find once even if there are multiple occurrences :/
:// it's so over
"""