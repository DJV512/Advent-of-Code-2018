# FILENAME = "sample_input.txt"
# FILENAME = "sample_mod.txt"
FILENAME = "input.txt"

import time
import utils
from collections import deque
from PIL import Image, ImageDraw
import glob


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, answer2 = part1(data)
    part1_time = time.time()
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

    clay = set()
    for line in data:
        parts = line.strip().split(", ")
        first_coord, first_coord_value = parts[0].split("=")
        _, second_coord_range = parts[1].split("=")
        second_coord_low, second_coord_high = second_coord_range.split("..")
        for i in range(int(second_coord_low), int(second_coord_high)+1):
            if first_coord == "y":
                clay.add((int(first_coord_value), i))
            elif first_coord == "x":
                clay.add((i, int(first_coord_value)))

    return clay


def print_ground(clay, resting_water, flowing_water):
    max_y = max(y for y,x in clay)+1
    max_x = max(max(x for y,x in flowing_water), max(x for y,x in clay))+1
    min_y = 0
    min_x = min(min(x for y,x in flowing_water), min(x for y,x in clay))
    print(f"{min_y=}, {max_y=}, {min_x=}, {max_x=}")
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (y,x) == (0,500):
                print("+", end="")
            elif (y,x) in clay:
                print("#", end="")
            elif (y,x) in resting_water:
                print("~", end="")
            elif (y,x) in flowing_water:
                print("|", end="")
            else:
                print(".", end="")
        print("     ", y)
    print()


def draw_ground_image(clay, resting_water, flowing_water, scale=5):
    max_y = max(y for y,x in clay)+1
    max_x = max(x for y,x in clay)+2
    min_y = 0
    min_x = min(min(x for y,x in flowing_water), min(x for y,x in clay))
    width = (max_x - min_x + 1) * scale
    height = (max_y - min_y + 1) * scale
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            pos = (y,x)
            px = (x - min_x) * scale
            py = (y - min_y) * scale
            box = [px, py, px + scale - 1, py + scale - 1]

            if pos == (0,500):
                draw.rectangle(box, fill="green")
            elif (y,x) in clay:
                draw.rectangle(box, fill="saddlebrown")
            elif (y,x) in resting_water:
                draw.rectangle(box, fill="blue")
            elif (y,x) in flowing_water:
                draw.rectangle(box, fill="lightblue")
            else:
                draw.rectangle(box, fill="white")
    return img


def fillable(position, clay, resting_water):
    y,x = position
    left = x
    right = x
    while True:
        if (y, left) in clay:
            break
        below = (y+1, left)
        if below not in clay and below not in resting_water:
            return None, None
        left -=1
    
    while True:
        if (y, right) in clay:
            break
        below = (y+1, right)
        if below not in clay and below not in resting_water:
            return None, None
        right +=1
    
    return left+1, right
    

def part1(clay):

    max_y = max(y for y,_ in clay)
    min_y = min(y for y,x in clay)
    flowing_water = set()
    resting_water = set()
    stack = deque()
    stack.append((1, 500))
    # frame_count = 0

    while stack:
        spot = stack.popleft()

        if spot[0] > max_y:
            continue

        if all(spot not in s for s in (clay, flowing_water, resting_water)):
            below = (spot[0]+1, spot[1])
            if all(below not in s for s in (clay, flowing_water, resting_water)):
                flowing_water.add(spot)
                stack.append(below)
            elif below in clay or below in resting_water:
                left, right = fillable(spot, clay, resting_water)
                if left is not None and right is not None:
                    for i in range(left, right):
                        resting_water.add((spot[0], i))
                        flowing_water.discard((spot[0],i))
                    stack.append((spot[0]-1, spot[1]))
                else:
                    flowing_water.add(spot)
                    left_side = (spot[0], spot[1]-1)
                    right_side = (spot[0], spot[1]+1)
                    if all(left_side not in s for s in (clay, resting_water, flowing_water)) or (left_side in flowing_water and (left_side[0]-1, left_side[1]) in flowing_water):
                        stack.append(left_side)
                    if all(right_side not in s for s in (clay, resting_water, flowing_water)) or (right_side in flowing_water and (right_side[0]-1, right_side[1]) in flowing_water):
                        stack.append(right_side)
            elif below in flowing_water:
                flowing_water.add(spot)
            
                    
        elif spot in flowing_water:
            left, right = fillable(spot, clay, resting_water)
            if left is not None and right is not None:
                for i in range(left, right):
                    resting_water.add((spot[0], i))
                    flowing_water.discard((spot[0],i))
                stack.append((spot[0]-1, spot[1]))
            else:
                left_side = (spot[0], spot[1]-1)
                right_side = (spot[0], spot[1]+1)
                if all(left_side not in s for s in (clay, resting_water, flowing_water)) or (left_side in flowing_water and (left_side[0]-1, left_side[1]) in flowing_water):
                    stack.append(left_side)
                if all(right_side not in s for s in (clay, resting_water, flowing_water)) or (right_side in flowing_water and (right_side[0]-1, right_side[1]) in flowing_water):
                    stack.append(right_side)
                

        elif spot in resting_water:
            stack.append((spot[0]-1, spot[1]))
    
        
    #     img = draw_ground_image(clay, resting_water, flowing_water)
    #     img.save(f"frames/frame_{frame_count:04d}.png")
    #     frame_count += 1
    
    # frame_files = sorted(glob.glob("frames/frame_*.png"))
    # frames  = [Image.open(f) for f in frame_files]
    # frames[0].save(
    # "animation.gif",
    # save_all=True,
    # append_images=frames[1:],
    # duration=10,
    # loop=0
    # )

    # print_ground(clay, resting_water, flowing_water)
    total_water = sum(1 for y,x in resting_water if y >= min_y) + sum(1 for y,x in flowing_water if y >= min_y)
    return total_water, len(resting_water)


if __name__ == "__main__":
    main()