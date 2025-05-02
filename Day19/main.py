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

    registers = [1,0,0,0,0,0]
    count = 0

    while registers[pointer] < len(program):
        count += 1
        instruction = registers[pointer]

        func, a, b, c = program[instruction]

        registers = operation(func, a, b, c, registers)

        registers[pointer] += 1

        if count <30:
            print(f"{count=}, {registers=}")

    return registers[0]


def part2():
    
    # Brute force here would run forever, so it was necessary to figure out what the code is doing and subvert that.
    # In part 1, register 4 is set to 906 within the first few iterations and stays that way for the entirety of the program,
    # and the answer (1824) is the sum of all the factors of 906. For part 2, register 4 gets set to a much bigger number
    # (stored in number below). I just wrote a short loop to find the factors and add them up. Much easier (and faster!).

    number = 10551306

    factors = set()
    for i in range(1, number+1):
        if number % i == 0:
            factors.add(i)

    return sum(factors)


if __name__ == "__main__":
    main()