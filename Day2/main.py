# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import Counter


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(data)
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

    return data


def part1(data):
    twos = 0
    threes = 0
    for line in data:
        counts = Counter(line.strip())
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    return twos*threes


def part2(data):
    entries = len(data)
    length = len(data[0].strip())
    possibles = []
    for a in range(entries-1):
        for b in range(a+1, entries):
            one_wrong = False
            two_wrong = False
            for i in range(length):
                if data[a][i] != data[b][i]:
                   if one_wrong:
                       two_wrong = True
                       break
                   else:
                       one_wrong = True
                       j = i
            if one_wrong and not two_wrong:
                possibles.append((data[a], data[b], j))  

    string = possibles[0][0]
    j = possibles[0][2]    

    return string[0:j] + string[j+1:]


if __name__ == "__main__":
    main()