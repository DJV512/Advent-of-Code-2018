# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, guards = part1(data)
    part1_time = time.time()
    answer2 = part2(guards)
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
    
    schedule = []
    for line in data:
        schedule.append(line.strip())
    return schedule


def part1(data):

    schedule = sorted(data)
    inner_dict = lambda: defaultdict(int)
    guards = defaultdict(inner_dict)

    for line in schedule:
        parts = line.split()
        if "begins" in line:
            guard_num = parts[3][1:]
        elif "asleep" in line:
            first_min = parts[1][3:5]
        elif "wakes" in line:
            last_min = parts[1][3:5]
            for x in range(int(first_min), int(last_min)):
                guards[int(guard_num)][x] += 1

    most_sleep = 0
    for guard in guards:
        total_sleep = sum(guards[guard][x]for x in range(0,60))
        if total_sleep > most_sleep:
            most_sleep = total_sleep
            sleepy_guard = guard
            sleepiest_minute = max(guards[guard], key=lambda x: guards[guard][x])

    return sleepy_guard * sleepiest_minute, guards


def part2(guards):
    minute_most_asleep=-1
    for guard in guards:
        minute = max(guards[guard], key=lambda x: guards[guard][x])
        if guards[guard][minute] > minute_most_asleep:
            minute_most_asleep = guards[guard][minute]
            sleepy_minute = minute
            sleepy_guard = guard

    return sleepy_guard * sleepy_minute


if __name__ == "__main__":
    main()