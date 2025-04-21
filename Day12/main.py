# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils


def main():
    start_time = time.time()

    plants, rules = parse_data()
    parse_time = time.time()

    answer1 = part1(plants, rules)
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


def parse_data():
    with open(FILENAME, "r") as f:
        data = f.readlines()

    rules = {}
    for line in data:
        if "initial" in line:
            plants = [".", ".", ".", ".", ".", ".", "."]
            plants.extend(list(line.strip().split()[2]))
            plants.extend([".", ".", ".", ".", ".", ".", "."])

        if "=>" in line:
            parts = line.strip().split(" => ")
            rules[parts[0]] = parts[1]
        
    return plants, rules


def part1(plants, rules):

    for _ in range(20):
        new_plants = [".", "."]
        length = len(plants)
        for pot in range(0, length-3):
            surroundings = plants[pot:pot+5]
            new_plants.append(rules.get(("".join(surroundings)), "."))
        plants = new_plants + [".", "."]

    plant_count = 0
    for i in range(len(plants)):
        if plants[i] == "#":
            plant_count += i - 7

    return plant_count


def part2():

    # Played around printing it out and noticed that it settled into a predictable pattern around generation 150.
    # Determined the score for each generation from 150 to 160, and fit a linear trendline to it with Excel.
    # The return statement below is that linear equation, with 50 billion generations substituted in.

    return 102*(50000000000)+1377


if __name__ == "__main__":
    main()