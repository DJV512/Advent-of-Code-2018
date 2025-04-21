FILENAME = "sample_input.txt"
#FILENAME = "input.txt"

import time
import utils

def main():
    start_time = time.time()

    parse_time = time.time()

    answer1, grid = part1()
    part1_time = time.time()
    answer2, max_size = part2(grid)
    part2_time = time.time()

    print("---------------------------------------------------")
    print(f"Part 1 Answer: {answer1}")
    print()
    print(f"Part 2 Answer: {answer2, max_size}")
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


def power_level(x, y):
    serial = 7139
    # serial = 18

    rackID = x + 10
    power = rackID * y
    power += serial
    power *= rackID
    power %= 1000
    power = int((power - power%100)/100)
    power -= 5 

    return power


def part1():
    
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x,y)] = power_level(x, y)

    max_power = 0
    for x in range(1, 299):
        for y in range(1, 299):
            power = 0
            for i in [0, 1, 2]:
                for j in [0, 1, 2]:
                    power += grid[(x+i, y+j)]
            if power > max_power:
                max_power = power
                max_coord = (x,y)

    return max_coord, grid


def make_sat(grid):
    sat_grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            power = grid[(x, y)] + sat_grid.get((x - 1, y), 0) + sat_grid.get((x, y-1), 0) - sat_grid.get((x - 1, y - 1), 0)
            sat_grid[(x, y)] = power
    
    return sat_grid


def part2(grid):

    sat_grid = make_sat(grid)

    max_power = 0
    for x in range(1, 301):
        for y in range(1, 301):
            for q in range(300):
                if x + q < 301 and y + q < 301:
                    power = sat_grid[(x + q, y + q)] - sat_grid.get((x - 1, y + q), 0) - sat_grid.get((x + q, y - 1), 0) + sat_grid.get((x - 1, y - 1), 0)
                    if power > max_power:
                        max_power = power
                        max_coord = (x, y)
                        max_size = q

    return max_coord, max_size
                    

if __name__ == "__main__":
    main()