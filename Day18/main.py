# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from copy import deepcopy


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    datapart1 = deepcopy(data)
    datapart2 = deepcopy(data)

    answer1 = part1(datapart1)
    part1_time = time.time()
    answer2 = part2(datapart2)
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

    return utils.grid_parse_list(data)


def count_surroundings(spot, data, height, width):
    trees = 0
    lumberyard = 0
    for direction in [(-1, -1), (-1, 0), (-1, 1), (0,-1), (0, 1), (1, -1), (1, 0), (1,1)]:
        new_spot = (spot[0]+direction[0],spot[1]+direction[1])
        if new_spot[0] >= 0 and new_spot[0] < height and new_spot[1] >= 0 and new_spot[1] < width:
            if data[new_spot[0]][new_spot[1]] == "|":
                trees += 1
            elif data[new_spot[0]][new_spot[1]] == "#":
                lumberyard += 1
    return trees, lumberyard



def part1(data):

    height = len(data)
    width = len(data[0])

    for i in range(10):
        new_grid = [["."]*width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                spot = (y,x)
                current = data[spot[0]][spot[1]]
                
                trees, lumberyard = count_surroundings(spot, data, height, width)
                
                if current == ".":
                    if trees >= 3:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "|":
                    if lumberyard >= 3:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "#":
                    if lumberyard >= 1 and trees >= 1:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "."
                
        data = new_grid

    final_trees = 0
    final_lumberyard = 0
    for y in range(height):
        for x in range(width):
            if data[y][x] == "#":
                final_lumberyard += 1
            if data[y][x] == "|":
                final_trees += 1

    return final_trees * final_lumberyard


def part2(data):

    data1 = deepcopy(data)
    data2 = deepcopy(data)
    data3 = deepcopy(data)

    height = len(data)
    width = len(data[0])
    seen = set()
    i = 0

    while True:
        i += 1
        new_grid = [["."]*width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                spot = (y,x)
                current = data1[spot[0]][spot[1]]
                
                trees, lumberyard = count_surroundings(spot, data1, height, width)
                
                if current == ".":
                    if trees >= 3:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "|":
                    if lumberyard >= 3:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "#":
                    if lumberyard >= 1 and trees >= 1:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "."
                
        state = bytes(ord(cell) for row in new_grid for cell in row)
        if state in seen:
            cycle_state = state
            break
        else:
            seen.add(state)
        data1 = new_grid
        

    j=0
    while True:
        j += 1
        new_grid = [["."]*width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                spot = (y,x)
                current = data2[spot[0]][spot[1]]
                
                trees, lumberyard = count_surroundings(spot, data2, height, width)
                
                if current == ".":
                    if trees >= 3:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "|":
                    if lumberyard >= 3:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "#":
                    if lumberyard >= 1 and trees >= 1:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "."
                
        state = bytes(ord(cell) for row in new_grid for cell in row)
        if state == cycle_state:
            break
        data2 = new_grid
        
    
    cycle_length = i-j
    minute_number = j+(1000000000-j)%cycle_length 


    k=0
    while True:
        k += 1
        new_grid = [["."]*width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                spot = (y,x)
                current = data3[spot[0]][spot[1]]
                
                trees, lumberyard = count_surroundings(spot, data3, height, width)
                
                if current == ".":
                    if trees >= 3:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "|":
                    if lumberyard >= 3:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "|"
                elif current == "#":
                    if lumberyard >= 1 and trees >= 1:
                        new_grid[spot[0]][spot[1]] = "#"
                    else:
                        new_grid[spot[0]][spot[1]] = "."
        
        if k == minute_number:
            break
        data3 = new_grid
        

    final_trees = 0
    final_lumberyard = 0
    for y in range(height):
        for x in range(width):
            if new_grid[y][x] == "#":
                final_lumberyard += 1
            elif new_grid[y][x] == "|":
                final_trees += 1

    return final_trees * final_lumberyard


if __name__ == "__main__":
    main()