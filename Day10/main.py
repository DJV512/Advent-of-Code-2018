# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
import re
from PIL import Image


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
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

    pattern = r"-?\d+, +-?\d+"
    points = {}
    for i, line in enumerate(data):
        numbers = re.findall(pattern, line.strip())
        final_numbers = []
        for number in numbers:
            parts = number.split(", ")
            final_numbers += parts
        points[i] = [int(final_numbers[0]), int(final_numbers[1]), int(final_numbers[2]), int(final_numbers[3])]

    return points


def part1(data):
    for seconds in range(11000):
        
        for key in data:
            x, y, vx, vy = data[key]
            data[key] = [x+vx, y+vy, vx, vy]
            
        maxx = max(data.values(), key=lambda x: x[0])[0]
        minx = min(data.values(), key=lambda x: x[0])[0]
        maxy = max(data.values(), key=lambda x: x[1])[1]
        miny = min(data.values(), key=lambda x: x[1])[1]

        yrange = maxy-miny+1
        xrange = maxx-minx+1

        if yrange < 15 and xrange < 70:

            # Change the format of the data dictionary for ease of making pixels
            pixel_dict = {}
            for key in data:
                pixel_dict[(data[key][1],data[key][0])] = ""
        
            # Create a new black and white (1-bit) image
            img = Image.new("1", (maxx-minx+1, maxy-miny+1))  # "1" mode for 1-bit pixels (black and white)

            # Convert the string data into pixel data
            pixels = [[0]*(maxx-minx+1) for _ in range(maxy-miny+1)]
            for key in pixel_dict:
                pixels[(key[0]-miny)][(key[1]-minx)] = 1
            final_pixels = []
            for row in pixels:
                final_pixels += row

            # Update the image with the pixel data
            img.putdata(final_pixels)

            # Save the image as a BMP file
            img.save(f"output{seconds+1}.bmp")
                        

    return None


def part2():
    # Just check the file name of the correct image
    return None


if __name__ == "__main__":
    main()