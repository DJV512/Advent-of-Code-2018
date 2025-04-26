# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
import re
from collections import defaultdict


def main():
    start_time = time.time()

    data, program = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(data, program)
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

    before_and_after = []
    parts = data.strip().split("\n\n")
    pattern = r"\d{1,2}"
    for i, part in enumerate(parts):
        matches = re.findall(pattern, part)
        if not matches:
            break
        before_and_after.append(matches+[i])


    program = []
    for x in range(i+1, len(parts)):
        matches = re.findall(pattern, parts[x])
        program.append(matches)

    return before_and_after, program


def operation(a, b, c, func, b0=None, b1=None, b2=None, b3=None, debug=True, registers=None):
    if debug:
        registers = {
            0: b0,
            1: b1,
            2: b2,
            3: b3
        }

    if func == "addr":
        registers[c] = registers[a] + registers[b]
    elif func == "addi":
        registers[c] = registers[a] + b
    elif func == "mulr":
        registers[c] = registers[a] * registers[b]
    elif func == "muli":
        registers[c] = registers[a] * b
    elif func == "banr":
        registers[c] = registers[a] & registers[b]
    elif func == "bani":
        registers[c] = registers[a] & b
    elif func == "borr":
        registers[c] = registers[a] | registers[b]
    elif func == "bori":
        registers[c] = registers[a] | b
    elif func == "setr":
        registers[c] = registers[a]
    elif func == "seti":
        registers[c] = a
    elif func == "gtir":
        if a > registers[b]:
            registers[c] = 1
        else:
            registers[c] = 0
    elif func == "gtri":
        if registers[a] > b:
            registers[c] = 1
        else:
            registers[c] = 0
    elif func == "gtrr":
        if registers[a] > registers[b]:
            registers[c] = 1
        else:
            registers[c] = 0
    elif func == "eqir":
        if a == registers[b]:
            registers[c] = 1
        else:
            registers[c] = 0
    elif func == "eqri":
        if registers[a] == b:
            registers[c] = 1
        else:
            registers[c] = 0
    elif func == "eqrr":
        if registers[a] == registers[b]:
            registers[c] = 1
        else:
            registers[c] = 0
    else:
        raise NameError("Unknown function.")
    
    if debug:
        return registers.values()
    else:
        return registers



def part1(data):
    ops = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

    total = 0
    for row in data:
        
        b0, b1, b2, b3, op_code, a, b, c, a0, a1, a2, a3, i = map(int, row)

        works = 0
        for op in ops:
            if list(operation(a, b, c, op, b0, b1, b2, b3)) == [a0, a1, a2, a3]:
                works += 1
    
        if works >= 3:
            total += 1

    return total


def part2(data, program):

    # This first part was used to find all possible op_code mappings and print them out.
    # Then I used process of elimination manually to create the real_codes dictionary below.

    # ops = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]
    # works_total = defaultdict(set)
    # for row in data:
    #     b0, b1, b2, b3, op_code, a, b, c, a0, a1, a2, a3, i = map(int, row)
    #     for op in ops:
    #         if list(operation(a, b, c, op, b0, b1, b2, b3)) == [a0, a1, a2, a3]:
    #             works_total[op_code].add(op)
        
    # for key in works_total:
    #     print(key, works_total[key])



    real_codes = {
        6: "muli",
        0: "addi",
        4: "addr",
        15: "mulr",
        2: "borr",
        12: "bori",
        5: "seti",
        3: "gtri",
        14: "eqir",
        1: "eqrr",
        9: "gtrr",
        13: "eqri",
        11: "gtir",
        7: "bani",
        8: "banr",
        10: "setr",
    }
    
    registers = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }

    program = program[0]

    for i in range(0, len(program), 4):
        op_code = int(program[i])
        a = int(program[i+1])
        b = int(program[i+2])
        c = int(program[i+3])
        registers = operation(a, b, c, real_codes[op_code], debug=False, registers=registers)

    return registers[0]

        

if __name__ == "__main__":

    main()