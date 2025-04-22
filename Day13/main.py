# FILENAME = "sample_input.txt"
FILENAME = "input.txt"


import time
import utils


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


output = False  # Toggle this flag to enable/disable prints
def debug_print(*args, **kwargs):
    if output:
        print(*args, **kwargs)


def parse_data():
    with open(FILENAME, "r") as f:
        data = f.readlines()

    return [list(line) for line in data]


def part1(data):
    
    carts = []
    for i, y in enumerate(data):
        for j, x in enumerate(y):
            if x in ["^", "v", ">", "<"]:
                carts.append((i,j,x,0)) 

    tick = 1
    while True:
        carts = sorted(carts, key = lambda x: (x[0], x[1]))
        new_carts = []
        for z, cart in enumerate(carts):
            y, x, direction, turn = cart
            if direction == "^":
                next_spot = data[y-1][x]
                if next_spot in ["|", "^", "v"]:
                    new_carts.append((y-1, x, "^", turn))
                elif next_spot == "/":
                    new_carts.append((y-1, x, ">", turn))
                elif next_spot == "\\":
                    new_carts.append((y-1, x, "<", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y-1, x, "<", 1))
                    elif turn == 1:
                        new_carts.append((y-1, x, "^", 2))
                    elif turn == 2:
                        new_carts.append((y-1, x, ">", 0))
            
            elif direction == "v":
                next_spot = data[y+1][x]
                if next_spot in ["|", "^", "v"]:
                    new_carts.append((y+1, x, "v", turn))
                elif next_spot == "/":
                    new_carts.append((y+1, x, "<", turn))
                elif next_spot == "\\":
                    new_carts.append((y+1, x, ">", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y+1, x, ">", 1))
                    elif turn == 1:
                        new_carts.append((y+1, x, "v", 2))
                    elif turn == 2:
                        new_carts.append((y+1, x, "<", 0))
            
            elif direction == ">":
                next_spot = data[y][x+1]
                if next_spot in ["-", ">", "<"]:
                    new_carts.append((y, x+1, ">", turn))
                elif next_spot == "/":
                    new_carts.append((y, x+1, "^", turn))
                elif next_spot == "\\":
                    new_carts.append((y, x+1, "v", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y, x+1, "^", 1))
                    elif turn == 1:
                        new_carts.append((y, x+1, ">", 2))
                    elif turn == 2:
                        new_carts.append((y, x+1, "v", 0))
            
            elif direction == "<":
                next_spot = data[y][x-1]
                if next_spot in ["-", ">", "<"]:
                    new_carts.append((y, x-1, "<", turn))
                elif next_spot == "/":
                    new_carts.append((y, x-1, "v", turn))
                elif next_spot == "\\":
                    new_carts.append((y, x-1, "^", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y, x-1, "v", 1))
                    elif turn == 1:
                        new_carts.append((y, x-1, "<", 2))
                    elif turn == 2:
                        new_carts.append((y, x-1, "^", 0))

            newly_moved = new_carts[-1]
            for q in range(len(new_carts)-1):
                if new_carts[q][0] == newly_moved[0] and new_carts[q][1] == newly_moved[1]:
                    return newly_moved[1], newly_moved[0]
            for q in range(z+1, len(carts)):
                if carts[q][0] == newly_moved[0] and carts[q][1] == newly_moved[1]:
                    return newly_moved[1], newly_moved[0]
            
        tick += 1
        carts = new_carts


def part2(data):

    carts = []
    for i, y in enumerate(data):
        for j, x in enumerate(y):
            if x in ["^", "v", ">", "<"]:
                carts.append((i,j,x,0)) 

    tick = 1
    while True:
        carts = sorted(carts, key = lambda x: (x[0], x[1]))
        new_carts = []
        popped = 0
        to_remove=[]
        for z, cart in enumerate(carts.copy()):
            if z in to_remove:
                continue

            y, x, direction, turn = cart
            if direction == "^":
                next_spot = data[y-1][x]
                if next_spot in ["|", "^", "v"]:
                    new_carts.append((y-1, x, "^", turn))
                elif next_spot == "/":
                    new_carts.append((y-1, x, ">", turn))
                elif next_spot == "\\":
                    new_carts.append((y-1, x, "<", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y-1, x, "<", 1))
                    elif turn == 1:
                        new_carts.append((y-1, x, "^", 2))
                    elif turn == 2:
                        new_carts.append((y-1, x, ">", 0))
            
            elif direction == "v":
                next_spot = data[y+1][x]
                if next_spot in ["|", "^", "v"]:
                    new_carts.append((y+1, x, "v", turn))
                elif next_spot == "/":
                    new_carts.append((y+1, x, "<", turn))
                elif next_spot == "\\":
                    new_carts.append((y+1, x, ">", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y+1, x, ">", 1))
                    elif turn == 1:
                        new_carts.append((y+1, x, "v", 2))
                    elif turn == 2:
                        new_carts.append((y+1, x, "<", 0))
            
            elif direction == ">":
                next_spot = data[y][x+1]
                if next_spot in ["-", ">", "<"]:
                    new_carts.append((y, x+1, ">", turn))
                elif next_spot == "/":
                    new_carts.append((y, x+1, "^", turn))
                elif next_spot == "\\":
                    new_carts.append((y, x+1, "v", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y, x+1, "^", 1))
                    elif turn == 1:
                        new_carts.append((y, x+1, ">", 2))
                    elif turn == 2:
                        new_carts.append((y, x+1, "v", 0))
            
            elif direction == "<":
                next_spot = data[y][x-1]
                if next_spot in ["-", ">", "<"]:
                    new_carts.append((y, x-1, "<", turn))
                elif next_spot == "/":
                    new_carts.append((y, x-1, "v", turn))
                elif next_spot == "\\":
                    new_carts.append((y, x-1, "^", turn))
                elif next_spot == "+":
                    if turn == 0:
                        new_carts.append((y, x-1, "v", 1))
                    elif turn == 1:
                        new_carts.append((y, x-1, "<", 2))
                    elif turn == 2:
                        new_carts.append((y, x-1, "^", 0))


            newly_moved = new_carts[-1]
            keep_going = True
            for q in range(len(new_carts)-1):
                if new_carts[q][0] == newly_moved[0] and new_carts[q][1] == newly_moved[1]:
                    new_carts.pop()
                    new_carts.pop(q)
                    keep_going = False
                    break
            if keep_going:
                for q in range(z+1, len(carts)):
                    if carts[q-popped][0] == newly_moved[0] and carts[q-popped][1] == newly_moved[1]:
                        new_carts.pop()
                        to_remove.append((q-popped))
                        popped += 1
                        break
                
        for cart in to_remove:
            carts.pop(cart)

        tick +=1

        carts = new_carts
        if len(carts) == 1:
            return carts[0][1], carts[0][0]
        
        if len(carts) == 0:
            print("ERROR")
            break

        

if __name__ == "__main__":
    main()