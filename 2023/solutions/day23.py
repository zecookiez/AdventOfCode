from collections import defaultdict

def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day23.txt", "r")
    input = [i.strip() for i in file.readlines()]

    def neigh4(x, y, H, W):
        for nx, ny in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            if 0 <= nx < H and 0 <= ny < W:
                yield (nx, ny)

    directions = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0)
    }

    def solve(grid, part_2):
        H, W = len(grid), len(grid[0])
        # Find all important intersections of the grid
        cross = [(0, 1), (H - 1, W - 2)]
        for x in range(H):
            for y in range(W):
                if grid[x][y] != ".": continue
                cand = [
                    (nx, ny) for nx, ny in neigh4(x, y, H, W) if grid[nx][ny] != "#"
                ]
                if len(cand) > 2:
                    cross.append((x, y))

        adj = defaultdict(list)
        cross_seen = set(cross)
        for ii, jj in cross:
            # For each intersection, calculate its distance to the next intersection without crossing an intersection
            queue = [(ii, jj, 0)]
            seen = {(ii, jj)}
            for x, y, d in queue:
                if (x, y) in cross_seen and (x, y) != (ii, jj):
                    adj[ii, jj].append((x, y, d))
                    continue
                # Process slopes
                ch = grid[x][y]
                if ch in directions:
                    dx, dy = directions[ch]
                    x += dx
                    y += dy
                    if 0 <= x < H and 0 <= y < W and grid[x][y] != "#" and (x, y) not in seen:
                        seen.add((x, y))
                        queue.append((x, y, d + 1))
                else:
                    for nx, ny in neigh4(x, y, H, W):
                        if grid[nx][ny] == "#": continue
                        if (nx, ny) in seen: continue
                        seen.add((nx, ny))
                        queue.append((nx, ny, d + 1))

        # Brute force but we do meet in the middle (one from start, one from end)
        # Theres roughly ~36 nodes, so both sides will do 18 nodes each
        # Also map each node to an integer, then switch to bitmask and adjacency list with integers
        LIM = len(cross)
        first = [[] for _ in range(LIM)]
        encode = {(x, y): ind for ind, (x, y) in enumerate(cross)}
        nadj = [[] for _ in range(LIM)]
        for x, y in adj:
            ind = encode[x, y]
            for nx, ny, d in adj[x, y]:
                nadj[ind].append((encode[nx, ny], d))

        longest = 0

        def first_half(node, seen, cur_dist, seen_cnt):
            # Edge case - you reach the end in the first half
            if node == encode[H - 1, W - 2]:
                nonlocal longest
                longest = max(longest, cur_dist)
            # Store result of first half
            if seen_cnt >= LIM and part_2:
                first[node].append((cur_dist, seen))
                return
            # Try neighbors
            for nx, d in nadj[node]:
                if (seen >> nx) & 1 == 0:
                    first_half(nx, seen | (1 << nx), cur_dist + d, seen_cnt + 2)
            return

        def second_half(node, seen, cur_dist, seen_cnt):
            # Too many nodes in second half
            if seen_cnt > LIM: return 0
            nonlocal longest
            # Exclude current, see if any first half is disjointed and is a longer path
            tmp = seen ^ (1 << node)
            for f_dist, f_seen in first[node]:
                # No more potential longer paths
                if f_dist + cur_dist <= longest: break
                # Disjoint (no repeated vertices)
                if tmp & f_seen == 0:
                    longest = f_dist + cur_dist
            # Try neighbors
            for nx, d in nadj[node]:
                if (seen >> nx) & 1 == 0:
                    second_half(nx, seen | (1 << nx), cur_dist + d, seen_cnt + 2)
            return
        # Start from beginning
        first_half(encode[0, 1], 1 << encode[0, 1], 0, 2)
        if part_2:
            # Sort each in decreasing length so that we can short circuit if no better paths exist
            for ind in range(LIM):
                first[ind].sort(key=lambda val: val[0], reverse=True)
            # Start from end
            second_half(encode[H - 1, W - 2], 1 << encode[H - 1, W - 2], 0, 2)
        return longest

    part1 = solve(input, False)
    clean_grid = input[:]
    for ch in "^v<>":
        clean_grid = [row.replace(ch, ".") for row in clean_grid]
    return part1, solve(clean_grid, True)

if __name__ == "__main__":
    print(main())

"""
Review:
- part 1 was good but pls no more grid (i still chickened out and tested example)
- part 2 was a disaster because i refused to compress the grid T_T
    - tried to cheese by printing longest path every time i got a new one
    - ended up "getting someone else's input" >10 times ._. this is so unfair
    - my original code ended up running an hour before getting the right answer......

cant save myself on the hard problems its so over 
"""