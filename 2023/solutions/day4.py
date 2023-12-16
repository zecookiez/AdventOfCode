import re

def main(ROOT = ".."):
    def get_int(line):
        return list(map(int, re.findall(r"\d+", line)))

    file = open(ROOT + "/inputs/day4.txt", "r")
    input = [i.strip() for i in file.readlines()]

    part1 = 0
    wins = []
    for line in input:
        card, rest = line.split(":")
        win, nums = rest.split("|")
        winning_numbers = set(get_int(win)) & set(get_int(nums))
        if winning_numbers:
            part1 += pow(2, len(winning_numbers) - 1)
        wins.append(len(winning_numbers))

    # Memoize answer for each card
    memo = {}
    def helper(pos):
        if pos in memo:
            return memo[pos]
        tot = wins[pos]
        # Add number of cards won for remaining cards
        for nx_card in range(pos + 1, pos + wins[pos] + 1):
            tot += helper(nx_card)
        memo[pos] = tot
        return tot

    return part1, sum(helper(i) for i in range(len(wins))) + len(wins)

if __name__ == "__main__":
    print(main())

"""
Review:
- lost all my time because i did not properly parse out the card number from the winning numbers T_T
- second half was ok but still a disaster because i cant think properly

we are so NOT back
"""