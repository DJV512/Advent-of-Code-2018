# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
import re


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

    nanobots = []
    pattern = r"-?\d+,-?\d+,-?\d+"
    pattern2 = r"\d+"
    for line in data:
        matches = re.findall(pattern, line.strip())
        coords = matches[0].split(",")
        x, y, z = int(coords[0]), int(coords[1]), int(coords[2])
        r = int(re.findall(pattern2, line.strip().split()[1])[0])
        nanobots.append((x, y, z, r))

    return nanobots


def part1(data):

    max_range = max(r for x,y,z,r in data)
    for x,y,z,r in data:
        if r == max_range:
            main_bot = (x,y,z)
            break

    in_range = 0
    for nanobot in data:
        x, y, z, _ = nanobot
        if manhattan(main_bot, (x, y, z)) <= max_range:
            in_range += 1
            
    return in_range


def cube_in_nanobot_range(nx, ny, nz, r, x, y, z, xstep, ystep, zstep):
    dx = max(0, x - nx, nx - (x + xstep - 1))
    dy = max(0, y - ny, ny - (y + ystep - 1))
    dz = max(0, z - nz, nz - (z + zstep - 1))
    return dx + dy + dz <= r


def min_dist_to_cube(cube, xstep, ystep, zstep):
    x, y, z = cube
    dx = max(0, 0 - x, x - (x + xstep - 1))
    dy = max(0, 0 - y, y - (y + ystep - 1))
    dz = max(0, 0 - z, z - (z + zstep - 1))
    return dx + dy + dz


def manhattan(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1]) + abs(pos1[2]-pos2[2])


def part2(data):

    xmax = max(data, key=lambda x: x[0])[0]
    xmin = min(data, key=lambda x: x[0])[0]
    ymax = max(data, key=lambda x: x[1])[1]
    ymin = min(data, key=lambda x: x[1])[1]
    zmax = max(data, key=lambda x: x[2])[2]
    zmin = min(data, key=lambda x: x[2])[2]

    xrange = xmax-xmin
    yrange = ymax-ymin
    zrange = zmax-zmin

    xstep = (xrange)//2
    ystep = (yrange)//2
    zstep = (zrange)//2

    while xstep > 10 or ystep > 10 or zstep > 10:

        cube_number = {}
        for x in range(xmin, xmax+1, xstep):
            for y in range(ymin, ymax+1, ystep):
                for z in range(zmin, zmax+1, zstep):
                    in_cube = 0
                    for nanobot in data:
                        nx, ny, nz, r = nanobot
                        if cube_in_nanobot_range(nx, ny, nz, r, x, y, z, xstep, ystep, zstep):
                            in_cube += 1
                    if in_cube != 0:
                        cube_number[(x, y, z)] = in_cube

        chosen_cube_max = max(cube_number.values())
        chosen_cube = min((cube for cube in cube_number if cube_number[cube] == chosen_cube_max), key=lambda x: min_dist_to_cube(x, xstep, ystep, zstep))
        
        xmin, ymin, zmin = chosen_cube
        xmax = xmin + xstep
        ymax = ymin + ystep
        zmax = zmin + zstep

        xrange = xmax-xmin
        yrange = ymax-ymin
        zrange = zmax-zmin

        xstep = (xrange)//2
        ystep = (yrange)//2
        zstep = (zrange)//2
    
    best = 0
    best_coord = []
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            for z in range(zmin, zmax+1):
                total = 0
                for nx, ny, nz, r in data:
                    if manhattan((nx, ny, nz), (x, y, z)) <= r:
                        total += 1
                if total > best:
                    best = total
                    best_coord = [(x,y,z)]
                elif total == best:
                    best_coord.append((x,y,z))

    closest = 1000000000
    for coord in best_coord:
        distance = manhattan(coord, (0,0,0))
        if distance < closest:
            closest = distance

    return closest


if __name__ == "__main__":
    main()