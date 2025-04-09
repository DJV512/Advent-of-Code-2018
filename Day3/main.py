# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, fabric = part1(data)
    part1_time = time.time()
    answer2 = part2(data, fabric)
    part2_time = time.time()

    print("---------------------------------------------------")
    print(f"Part 1 Answer: {answer1}")
    print()
    print(f"Part 2 Answer: {answer2}")
    print()
    print(f"Data Parse Execution Time: {1000*(parse_time - start_time):.2f} ms")
    print(f"Part 1 Execution Time:     {1000*(part1_time - parse_time):.2f} ms")
    print(f"Part 2 Execution Time:     {1000*(part2_time - part1_time):.2f} ms")
    print(f"Total Execution Time:      {1000*(part2_time - start_time):.2f} ms")
    print("---------------------------------------------------")


output = True  # Toggle this flag to enable/disable prints
def debug_print(*args, **kwargs):
    if output:
        print(*args, **kwargs)


def parse_data():
    with open(FILENAME, "r") as f:
        data = f.readlines()

    claims = []
    for line in data:
        parts = line.strip().split()
        claims.append((parts[0][1:], parts[2], parts[3]))

    return claims


def part1(data):

    fabric = defaultdict(int)
    for claim in data:
        x,y = claim[1].split(",")
        xlen, ylen = claim[2].split("x")

        x = int(x)
        y = int(y[:-1])
        xlen = int(xlen)
        ylen = int(ylen)

        for i in range(x, x+xlen):
            for j in range(y, y+ ylen):
                fabric[(i,j)] += 1
        
    return sum(1 for key in fabric if fabric[key] > 1), fabric


def part2(data, fabric):

    for claim in data:
        x,y = claim[1].split(",")
        xlen, ylen = claim[2].split("x")

        x = int(x)
        y = int(y[:-1])
        xlen = int(xlen)
        ylen = int(ylen)

        overlap = False
        for i in range(x, x+xlen):
            for j in range(y, y+ ylen):
                if fabric[(i,j)] > 1:
                    overlap = True
        
        if not overlap:
            return claim[0]
                


if __name__ == "__main__":
    main()