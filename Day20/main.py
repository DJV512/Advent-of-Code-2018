# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import deque, defaultdict


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, answer2 = part1(data)
    part1_time = time.time()
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
        data = f.read()

    return data.strip()


def period():
    return "."


def path_to_all_rooms(map):
    room_directory = {}

    queue = deque()
    queue.append(((0,0), 0))
    visited = set()
    visited.add((0,0))

    while queue:
        position, steps = queue.popleft()

        if map[position] == ".":
            room_directory[position] = steps
        
        for direction in [(-1,0), (1,0), (0,1), (0,-1)]:
            wall_or_not = (position[0]+direction[0], position[1]+direction[1])
            if map[wall_or_not] != "#":
                next_room = (position[0]+2*direction[0], position[1]+2*direction[1])
                if next_room not in visited:
                    visited.add(next_room)
                    queue.append((next_room, steps+1))
    
    return room_directory


def part1(data):

    position = (0,0)
    map = defaultdict(period)
    map[position] = "X"
    map[(-1, -1)] = "#"
    map[(-1, 1)] = "#"
    map[(1, -1)] = "#"
    map[(1, 1)] = "#"
    map[(0, 1)] = "?"
    map[(0, -1)] = "?"
    map[(1, 0)] = "?"
    map[(-1, 0)] = "?"

    i = 1

    stack = deque()

    while i < len(data)-1:

        map[(position[0]-1, position[1]-1)] = "#"
        map[(position[0]-1, position[1]+1)] = "#"
        map[(position[0]+1, position[1]-1)] = "#"
        map[(position[0]+1, position[1]+1)] = "#"

        direction = data[i]
        if direction in "NSEW":
            match direction:
                case "N":
                    map[(position[0]-1, position[1])] = "-"

                    if (position[0], position[1]+1) not in map:
                        map[(position[0], position[1]+1)] = "?"
                    if (position[0], position[1]-1) not in map:
                        map[(position[0], position[1]-1)] = "?"
                    if (position[0]+1, position[1]) not in map:
                        map[(position[0]+1, position[1])] = "?"
                        
                    position = (position[0]-2, position[1])

                case "S":
                    map[(position[0]+1, position[1])] = "-"

                    if (position[0], position[1]+1) not in map:
                        map[(position[0], position[1]+1)] = "?"
                    if (position[0], position[1]-1) not in map:
                        map[(position[0], position[1]-1)] = "?"
                    if (position[0]-1, position[1]) not in map:
                        map[(position[0]-1, position[1])] = "?"

                    position = (position[0]+2, position[1])

                case "E":
                    map[(position[0], position[1]+1)] = "|"

                    if (position[0], position[1]-1) not in map:
                        map[(position[0], position[1]-1)] = "?"
                    if (position[0]+1, position[1]) not in map:
                        map[(position[0]+1, position[1])] = "?"
                    if (position[0]-1, position[1]) not in map:
                        map[(position[0]-1, position[1])] = "?"

                    position = (position[0], position[1]+2)

                case "W":
                    map[(position[0], position[1]-1)] = "|"

                    if (position[0]+1, position[1]) not in map:
                        map[(position[0]+1, position[1])] = "?"
                    if (position[0]-1, position[1]) not in map:
                        map[(position[0]-1, position[1])] = "?"
                    if (position[0], position[1]+1) not in map:
                        map[(position[0], position[1]+1)] = "?"

                    position = (position[0], position[1]-2)

        elif direction == "(":
            stack.append(position)

        elif direction == "|":
            
            if (position[0]+1, position[1]) not in map:
                map[(position[0]+1, position[1])] = "?"
            if (position[0]-1, position[1]) not in map:
                map[(position[0]-1, position[1])] = "?"
            if (position[0], position[1]+1) not in map:
                map[(position[0], position[1]+1)] = "?"
            if (position[0], position[1]-1) not in map:
                map[(position[0], position[1]-1)] = "?"

            position = stack[-1]

        elif direction == ")":
            
            if (position[0]+1, position[1]) not in map:
                map[(position[0]+1, position[1])] = "?"
            if (position[0]-1, position[1]) not in map:
                map[(position[0]-1, position[1])] = "?"
            if (position[0], position[1]+1) not in map:
                map[(position[0], position[1]+1)] = "?"
            if (position[0], position[1]-1) not in map:
                map[(position[0], position[1]-1)] = "?"

            position = stack.pop()

        i += 1
    
    map[(position[0]-1, position[1]-1)] = "#"
    map[(position[0]-1, position[1]+1)] = "#"
    map[(position[0]+1, position[1]-1)] = "#"
    map[(position[0]+1, position[1]+1)] = "#"
    if (position[0]+1, position[1]) not in map:
        map[(position[0]+1, position[1])] = "#"
    if (position[0]-1, position[1]) not in map:
        map[(position[0]-1, position[1])] = "#"
    if (position[0], position[1]+1) not in map:
        map[(position[0], position[1]+1)] = "#"
    if (position[0], position[1]-1) not in map:
        map[(position[0], position[1]-1)] = "#"
        
    for key in map:
        if map[key] == "?":
            map[key] = "#"

    room_directory = path_to_all_rooms(map)

    answer1 = max(room_directory.values())
    answer2 = sum(1 for v in room_directory.values() if v >=1000)

    return answer1, answer2


if __name__ == "__main__":
    main()