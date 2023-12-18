
def main(ROOT = ".."):
    file = open(ROOT + "/inputs/day18.txt", "r")
    input = file.readlines()
    directions = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

    def part1_parse(direction, length, _):
        dx, dy = directions[direction]
        length = int(length)
        return dx * length, dy * length

    def part2_parse(old_dir, old_length, rgb):
        length = int(rgb[2:-2], 16)
        direction = "RDLU"[int(rgb[-2])]
        dx, dy = directions[direction]
        return dx * length, dy * length

    def parse(input, parse_func):
        x = y = 0
        points = [(0, 0)]
        for line in input:
            direction, length, rgb = line.split()
            dx, dy = parse_func(direction, length, rgb)
            x += dx
            y += dy
            points.append((x, y))
        return points

    def area(polygon):
        # Area of a simple polygon given its coordinates using shoelace formula
        # But we modelled our grid so that each coord has their own tile
        # => We're really looking for interior points + boundary points
        # Pick's Theorem tells us that (# interior points) = Area - boundary / 2 + 1
        # Real Area = (# interior) + (# boundary)
        #           = (Area - (# boundary) / 2 + 1) + (# boundary)
        #           = Area + (# boundary) / 2 + 1
        area = edge = 0
        for ind, (x1, y1) in enumerate(polygon):
            x2, y2 = polygon[ind - 1]
            area += x1 * y2 - y1 * x2
            edge += abs(x1 - x2) + abs(y1 - y2)
        return int(abs(area) / 2.0 + edge / 2.0 + 1)

    return area(parse(input, part1_parse)), area(parse(input, part2_parse))

if __name__ == "__main__":
    print(main())

"""
Review:
- i did bfs for part 1, nothing eventful
- wrote from scratch for part 2 to use polygon area
    - its honestly a miracle that i remembered about shoelace theorem and pick's theorem
    - and then clowned around for a bit because i couldnt think up how boundary was included to the answer

"""