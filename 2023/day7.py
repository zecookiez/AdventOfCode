from itertools import combinations_with_replacement
from collections import Counter

file = open("inputs/day7.txt", "r")
input = [i.strip() for i in file.readlines()]

def solve_part1(H):
    hand, bid = H
    def map_to_type(frequency):
        types = {(5, 1)}, {(4, 1)}, {(2, 1), (3, 1)}, {(3, 1)}, {(2, 2)}, {(2, 1)}, {(1, 5)}
        for ind, req in enumerate(types):
            # I learned that <= means subset for python set operations today
            if req <= frequency:
                return -ind # Negative so that sorting prioritizes in the correct order
    # Count the number of each card
    # ...then count the number of counts
    # ......then turn them into (count of cards, count of count of cards)
    # Works great with sets i swear
    return map_to_type(set(Counter(Counter(hand).values()).items())), hand

def solve_part2(H):
    hand, bid = H
    ind_j = [ind for ind, card in enumerate(hand) if card == 0]
    best = solve_part1(H)
    # Too lazy to make a smart guess, we will try all combinations
    # Ordering doesn't matter since we only care about counts
    # Additional optimization is you should only care about cards you already have
    for comb in combinations_with_replacement(list(set(hand)), len(ind_j)):
        tmp = hand[:]
        for val, j_index in zip(comb, ind_j):
            tmp[j_index] = val
        res = solve_part1((tmp, bid))[0], hand
        best = max(best, res)
    return best

for strengths, sort_func in ("AKQJT98765432"[::-1], solve_part1), ("AKQT98765432J"[::-1], solve_part2):
    cards = []
    for line in input:
        hand, bid = line.split()
        cards.append((list(map(strengths.find, hand)), int(bid)))
    total = 0
    for rank, (_, bid) in enumerate(sorted(cards, key = sort_func), 1):
        total += rank * bid
    print(total)


"""
Review:
- i feel like i went slow on part 1 but it turned out okay
- part 2 was okay after figuring out how to reuse my part 1's code, but i had a few issues with the bruteforce guesser
"""