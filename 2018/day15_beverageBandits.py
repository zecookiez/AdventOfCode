t0 = time()
puzzle = [list(line[:-1]) for line in open("puzzle.txt")]

# Simulating the battle takes roughly O(n * m * k):
#   n being the area of the grid (Breadth-first search visits all the squares once in the worst case)
#   m being number of units (Iterate through every unit's turn)
#   k being the number of turns (Play until one side loses)
# Overall this took about ~550 ms with both parts together

def beverage_bandits(input):
    
    # Part A will take the full O(n * m * k) because we play until the end
    print("Part A: %d" % simulate_battle(input))

    # Part B however will add an extra log2(dmg) to find the minimum with binary search.
    # This will then take O(n * m * k * log(d)), d being the maximum damage.
    # However we don't need to run until the end for most cases and can short-circuit early (See line 126) so it takes about the same amount of time
    lower = 4
    upper = 200
    while upper - lower > 1:
        power = upper + lower >> 1
        if simulate_battle(input, power):
            upper = power
        else:
            lower = power
    return simulate_battle(input, upper)
    
def simulate_battle(grid, power = 3):

    class Unit:
        def __init__(self, x, y, type, id, power):
            self.x = x
            self.y = y
            self.type = type
            self.hp = 200
            self.dmg = power if type == "E" else 3
            self.id = id

        def target(self, unit, grid, units):

            enemy = "EG"[unit.type == "E"]

            queue = deque([[unit.x, unit.y, []]])
            visited = set()
            valid_targets = []

            while queue:
                new_queue = deque()

                for x_pos, y_pos, moves in queue:

                    if grid[x_pos][y_pos] == enemy:
                        valid_targets.append([moves, x_pos, y_pos])
                    else:
                        adjacent = [x_pos - 1, y_pos], [x_pos, y_pos - 1], [x_pos, y_pos + 1], [x_pos + 1, y_pos]
                        for new_x, new_y in adjacent:

                            if grid[new_x][new_y] == "#":
                                continue
                            elif grid[new_x][new_y] == unit.type:
                                continue
                            elif (new_x, new_y) in visited:
                                continue

                            visited.add((new_x, new_y))
                            new_queue.append([new_x, new_y, moves + [[new_x, new_y]]])
                if valid_targets:
                    break
                queue = new_queue

            if not valid_targets:
                return [[], unit.x, unit.y]
            return min(valid_targets, key = lambda candidate: (len(candidate[0]), candidate[0][-1]))

        def find(self, x, y, units):
            for index, unit in enumerate(units):
                if unit.x == x and unit.y == y:
                    if unit.hp > 0:
                        return index, unit
            return None

    def find_players(grid):
        units = []
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if col in "EG":
                    units.append(Unit(x, y, col, len(units), power))
        return units

    units = find_players(grid)
    grid = [list(row) for row in grid]
    rounds = 0

    while True:
        for index, unit in enumerate(units):

            grid[unit.x][unit.y] = "."
            if unit.hp <= 0:
                continue

            moves, enemy_x, enemy_y = unit.target(unit, grid, units)

            if len(moves) > 1:
                unit.x, unit.y = moves[0]
                units[index] = unit
            elif all(enemy_unit.type == unit.type for enemy_unit in units):
                return (rounds - 1) * sum(max(0, remaining_unit.hp) for remaining_unit in units)

            adjacent = [unit.x - 1, unit.y], [unit.x, unit.y - 1], [unit.x, unit.y + 1], [unit.x + 1, unit.y]
            enemy_health = 201
            enemy = 1e9, 1e9, []
            for new_x, new_y in adjacent:
                if grid[new_x][new_y] not in ("#." + unit.type):
                    health = unit.find(new_x, new_y, units)

                    if health and health[1].hp < enemy_health:
                        enemy_health = health[1].hp
                        enemy = new_x, new_y, health

            if enemy_health < 201:
                position, finished = enemy[2]
                finished.hp -= unit.dmg
                if finished.hp > 0:
                    units[position] = finished
                else:
                    grid[finished.x][finished.y] = "."
                    if power > 3 and finished.type == "E": # Short-circuiting for part B
                        return False

            grid[unit.x][unit.y] = unit.type

        units = sorted((unit for unit in units if unit.hp > 0), key = lambda candidate: [candidate.x, candidate.y])
        rounds += 1

print("Part B: %d" % beverage_bandits(puzzle))
print("Time: %d ms" % (1000 * (time() - t0)))
