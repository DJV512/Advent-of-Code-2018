# FILENAME = "sample_input.txt"
# FILENAME = "input.txt"

import time
import utils
from functools import lru_cache
import heapq

# TARGET = (10, 10)    
# DEPTH = 510
TARGET = (5, 746)
DEPTH = 4002

def main():
    start_time = time.time()

    parse_time = time.time()

    answer1 = part1()
    part1_time = time.time()
    answer2 = part2()
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


@lru_cache(maxsize=None)
def type(position):

    if position == (0,0) or position == TARGET:
        index = 0
    elif position[0] == 0:
        index = position[1]*48271
    elif position[1] == 0:
        index = position[0]*16807
    else:
        index = type((position[0]-1, position[1])) * type((position[0], position[1]-1))
    
    return (index + DEPTH) % 20183



def part1():

    total_risk = 0
    for x in range(TARGET[0]+1):
        for y in range(TARGET[1]+1):
            erosion = type((x,y))
            risk = erosion % 3
            total_risk += risk
        #     if (x,y) == TARGET:
        #         print("T", end="")
        #     elif risk == 0:
        #         print(".", end="")
        #     elif risk == 1:
        #         print("=", end="")
        #     elif risk == 2:
        #         print("|", end="")
        # print()

    return total_risk


def part2():

    pq = []
    heapq.heappush(pq, (0, (0,0), 1)) # (minutes, position, equipped); for equipped, 0 = neither, 1 = torch, 2 = climbing gear

    visited = set()

    while pq:
        minutes, position, equipped = heapq.heappop(pq)

        if position == TARGET:
            if equipped == 1:
                return minutes
            else:
                return minutes + 7

        terrain = type(position) % 3

        if (position, equipped) in visited:
            continue
        else:
            visited.add((position, equipped))

        for direction in utils.DIRS_4:
            next_position = (position[0] + direction[0], position[1] + direction[1])
            
            if next_position[0] < 0 or next_position[1] < 0:
                continue
            
            next_terrain = type(next_position) % 3

            if next_terrain == 0:
                if equipped in [1, 2]:
                    if (next_position, equipped) not in visited:
                        heapq.heappush(pq, (minutes + 1, next_position, equipped))
                else:
                    if terrain == 1:
                        if (next_position, 2) not in visited:
                            heapq.heappush(pq, (minutes + 8, next_position, 2))
                    elif terrain == 2:
                        if (next_position, 1) not in visited:
                            heapq.heappush(pq, (minutes + 8, next_position, 1))
                    
            elif next_terrain == 1:
                if equipped in [0, 2]:
                    if (next_position, equipped) not in visited:
                        heapq.heappush(pq, (minutes + 1, next_position, equipped))
                else:
                    if terrain == 0:
                        if (next_position, 2) not in visited:
                            heapq.heappush(pq, (minutes + 8, next_position, 2))
                    elif terrain == 2:
                        if (next_position, 0) not in visited:
                            heapq.heappush(pq, (minutes + 8, next_position, 0))
                    
            elif next_terrain == 2:
                if equipped in [0, 1]:
                    if (next_position, equipped) not in visited:
                        heapq.heappush(pq, (minutes + 1, next_position, equipped))
                else:
                    if terrain == 0:
                        if (next_position, 1) not in visited:
                            heapq.heappush(pq, (minutes + 8, next_position, 1))
                    elif terrain == 1:
                        if (next_position, 0) not in visited:
                            heapq.heappush(pq, (minutes + 8, next_position, 0))
                    

if __name__ == "__main__":

    main()