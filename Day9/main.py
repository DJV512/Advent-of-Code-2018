FILENAME = "sample_input.txt"
#FILENAME = "input.txt"

import time
import utils
from collections import defaultdict, deque


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


def part1():

    player_count = 412
    last_marble = 71646

    positions = deque([0, 1])
    current_player = 1
    scores = defaultdict(int)

    for marble in range(2, last_marble + 1):

        current_player = current_player + 1
        if current_player > player_count:
            current_player -= player_count

        if marble % 23 == 0:
            positions.rotate(7)
            new_score = positions.pop()
            scores[current_player] += marble + new_score
            positions.rotate(-1)

        else:
            positions.rotate(-1)
            positions.append(marble)
    
    return max(scores.values())


def part2():

    player_count = 412
    last_marble = 7164600

    positions = deque([0, 1])
    current_player = 1
    scores = defaultdict(int)

    for marble in range(2, last_marble + 1):

        current_player = current_player + 1
        if current_player > player_count:
            current_player -= player_count

        if marble % 23 == 0:
            positions.rotate(7)
            new_score = positions.pop()
            scores[current_player] += marble + new_score
            positions.rotate(-1)

        else:
            positions.rotate(-1)
            positions.append(marble)
    
    return max(scores.values())


if __name__ == "__main__":
    main()