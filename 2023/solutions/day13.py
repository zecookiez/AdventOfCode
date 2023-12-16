
def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day13.txt", "r")
    input = file.read().strip().split("\n\n")

    def solve(grid, target):

        def count_diff(split, limit, cnt_func):
            diff_cnt = 0
            # i am out of good names for the reflected index so i reversed the name of the original index
            for ind in range(split):
                dni = (split - ind) + split - 1
                if dni < limit:
                    diff_cnt += cnt_func(ind, dni)
            return diff_cnt

        H, W = len(grid), len(grid[0])
        reflect_ver = lambda ind: count_diff(ind, W, lambda ind1, ind2: sum(row[ind1] != row[ind2] for row in grid))
        reflect_hor = lambda ind: count_diff(ind, H, lambda ind1, ind2: sum(i != j for i, j in zip(grid[ind1], grid[ind2])))

        for ind in range(1, H):
            if reflect_hor(ind) == target:
                return 100 * ind
        for ind in range(1, W):
            if reflect_ver(ind) == target:
                return ind

    part1 = 0
    part2 = 0
    for case in input:
        grid = case.split("\n")
        part1 += solve(grid, 0)
        part2 += solve(grid, 1)

    return part1, part2

if __name__ == "__main__":
    print(main())

"""
Review:
- both parts were ok, slightly trolled a bit with part 1 as i tried to make the code for reflection
"""