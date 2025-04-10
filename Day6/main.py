# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import Counter


def main():
    start_time = time.time()

    coords, lowx, lowy, highx, highy = parse_data()
    parse_time = time.time()

    answer1 = part1(coords, lowx, lowy, highx, highy)
    part1_time = time.time()
    answer2 = part2(coords, lowx, lowy, highx, highy)
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

    coords = []
    lowx = 100000000
    lowy = 100000000
    highx = 0
    highy = 0
    for line in data:
        x,y = line.strip().split(", ")
        x = int(x)
        y = int(y)
        coords.append((y,x))
        if x < lowx:
            lowx = x
        if x > highx:
            highx = x
        if y < lowy:
            lowy = y
        if y > highy:
            highy = y
        
    return coords, lowx, lowy, highx, highy


def part1(coords, lowx, lowy, highx, highy):

    infinites = set()
    grid = {}
    for y in range(lowy, highy + 1):
        for x in range(lowx, highx + 1):
            closest_dist = 1000000000
            closest_coord = "."
            for i, coord in enumerate(coords):
                manhattan = abs(y-coord[0]) + abs(x-coord[1])
                if manhattan < closest_dist:
                    closest_dist = manhattan
                    closest_coord = i
                elif manhattan == closest_dist:
                    closest_coord = "."
            if y == lowy or y == highy or x == lowx or x == highx:
                infinites.add(closest_coord)
            grid[(y,x)] = closest_coord

    count = Counter(grid.values())
    biggest = 0
    for key in count:
        if key not in infinites:
            if count[key] > biggest:
                biggest = count[key]

    return biggest


def part2(coords, lowx, lowy, highx, highy):
    size = 0
    for y in range(lowy, highy + 1):
        for x in range(lowx, highx + 1):
            manhattan = 0
            for coord in coords:
                manhattan += abs(y-coord[0]) + abs(x-coord[1])
            if manhattan < 10000:
                size += 1
    
    return size



if __name__ == "__main__":
    main()