FILENAME = "sample_input.txt"
#FILENAME = "input.txt"

import time
import utils


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
    recipes = 990941

    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(scores) < recipes + 15:
        new_score = scores[elf1] + scores[elf2]
        if new_score < 10:
            scores.append(new_score)
        else:
            scores.append(1)
            scores.append((new_score % 10))
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)
    
    str_scores = [str(x) for x in scores]

    return "".join(str_scores[recipes:recipes+10])


def part2():
    recipes = 990941
    pattern = [int(x) for x in str(recipes)]

    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    while True:
        new_score = scores[elf1] + scores[elf2]
        if new_score < 10:
            scores.append(new_score)
            if scores[-len(str(recipes)):] == pattern:
                break

        else:
            scores.append(1)
            if scores[-len(str(recipes)):] == pattern:
                break

            scores.append((new_score % 10))
            if scores[-len(str(recipes)):] == pattern:
                break

        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)
    
    return len(scores) - len(str(recipes))


if __name__ == "__main__":
    main()