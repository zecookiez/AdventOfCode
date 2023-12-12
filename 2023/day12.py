file = open("inputs/day12.txt", "r")
input = [i.strip() for i in file.readlines()]

def solve(s, nums):
    # Memoized parameters: index of s, index of nums, current <#> count, if we're currently counting <#>s
    memo = {}
    def helper(s_ind, ind, cnt, active):
        # Base case (finished going through the string)
        if s_ind == len(s):
            if active and cnt == nums[ind]:
                ind += 1
            return 1 if ind >= len(nums) else 0
        # Slight optimization by pruning <#>s that are too long
        if active and nums[ind] < cnt:
            return 0
        # Use memoized result
        label = s_ind, ind, cnt, active
        if label in memo:
            return memo[label]
        total = 0
        # <.> or <?> turns into <.>
        if s[s_ind] in ".?":
            # Check if we were counting #s, and see if it matches
            if active and nums[ind] == cnt:
                total += helper(s_ind + 1, ind + 1, 0, False)
            elif not active:
                total += helper(s_ind + 1, ind, 0, False)
        # <#> or <?> turns into <#>
        if s[s_ind] in "#?" and ind < len(nums):
            total += helper(s_ind + 1, ind, cnt + 1, True)
        memo[label] = total
        return total
    return helper(0, 0, 0, False)

part1 = 0
part2 = 0
for line in input:
    springs, nums = line.split()
    nums = list(map(int, nums.split(",")))
    part1 += solve(springs, nums)
    part2 += solve("?".join([springs] * 5), nums * 5)

print(part1)
print(part2)

"""
Review:
- recognizing the problem was going to be about dynamic programming was the fast part, implementing it was a separate story T_T
- i went through multiple ideas before getting the right recurrence down T_T

its so so over
"""