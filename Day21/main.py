# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils


def main():
    start_time = time.time()

    pointer, program = parse_data()
    parse_time = time.time()

    answer1 = part1(pointer, program)
    part1_time = time.time()
    answer2 = part2(pointer, program)
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

    program = []
    for i, line in enumerate(data):
        if i == 0:
            pointer = int(line[4])
        else:
            parts = line.strip().split()
            program.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))

    return pointer, program


def operation(func, a, b, c, registers):
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
    
    return registers


def part1(pointer, program):
    registers = [18051,0,0,0,0,0]
    count = 0

    while registers[pointer] < len(program):
        count += 1
        instruction = registers[pointer]

        func, a, b, c = program[instruction]

        registers = operation(func, a, b, c, registers)

        if instruction == 28:
            return registers[4]

        registers[pointer] += 1



def part2(pointer, program):

    # this program works and does spit out the right answer, though it took 6.5 minutes in pure Cpython
    # even using pypy3 it takes 37 seconds, which is much faster, but still slow for an AOC puzzle
    # i don't understand enough about the math of what the program is actually doing to write an optimized version,
    # so this will have to do

    registers = [0,0,0,0,0,0]
    count = 0
    possibles = set()

    while registers[pointer] < len(program):
        count += 1
        instruction = registers[pointer]

        func, a, b, c = program[instruction]

        registers = operation(func, a, b, c, registers)

        if instruction == 28:  
            if registers[4] not in possibles:
                possibles.add(registers[4])
                most_recent = registers[4]
            else:
                return most_recent

        registers[pointer] += 1
    return


if __name__ == "__main__":
    main()