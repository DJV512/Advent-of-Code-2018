# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import Counter, defaultdict
import networkx as nx
import matplotlib.pyplot as plt


def main():
    start_time = time.time()

    key_first, key_second = parse_data()
    parse_time = time.time()

    answer1 = part1(key_first)
    part1_time = time.time()
    answer2 = part2(key_second)
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

    key_first = defaultdict(list)
    key_second = defaultdict(list)
    for line in data:
        parts = line.strip().split()
        key_first[parts[1]].append(parts[7])
        key_second[parts[7]].append(parts[1])

    return key_first, key_second


def part1(key_first):
    G = nx.DiGraph()
    for key in key_first:
        for node in key_first[key]:
            G.add_edge(key, node)

    order = "".join(list(nx.lexicographical_topological_sort(G)))

    return order


def part2(key_second):

    # I tried to do this manually with the Excel sheet at first. I got the worng answer,
    # so decided to code it after all. Once I got the code working, I went back and fixed the
    # Excel sheet. Turns out I had made two of the jobs too short. It would have been right
    # otherwise!

    time = 0
    complete_jobs = set()
    available_jobs = set()
    current_jobs = [None] * 5
    current_jobs[0] = (["F", 60 + ord("F")-ord("A")+1])
    current_jobs[1] = (["S", 60 + ord("S")-ord("A")+1])

    while len(complete_jobs) < 26:

        for z in range(len(current_jobs)):
            if current_jobs[z] is not None:
                if current_jobs[z][1] > 1:
                    current_jobs[z][1] -= 1
                else:
                    complete_jobs.add(current_jobs[z][0])
                    current_jobs[z] = None

        for key in key_second.copy():
            can_do = True
            for prereq in key_second[key]:
                if prereq not in complete_jobs:
                    can_do = False
                    break
            if can_do:
                available_jobs.add(key)
                key_second.pop(key)  
        
        if available_jobs and None in current_jobs:
            for available_job in sorted(available_jobs):
                for worker in range(5):
                    if current_jobs[worker] == None:
                        current_jobs[worker] = ([available_job, 60 + ord(available_job)-ord("A")+1])
                        available_jobs.remove(available_job)
                        break

        time += 1

    return time


if __name__ == "__main__":
    main()