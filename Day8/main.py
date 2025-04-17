# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import namedtuple


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
        data = f.read()

    return data


def part1(data):

    parts = data.strip().split()

    node = namedtuple("node", ["children", "meta_number"])

    nodes = []
    total_meta = 0
    nodes.append(node(int(parts[0]), int(parts[1])))
    i = 2

    while True:
            
            current_node = nodes[-1]

            if current_node.children == 0:
                current_node = nodes.pop()
                for z in range(i, i+current_node.meta_number):
                    total_meta += int(parts[z])
                i = z + 1
                try:
                    last_node = nodes.pop()
                    nodes.append(node(children=last_node.children-1, meta_number=last_node.meta_number))
                except IndexError:
                    return total_meta
                
            else:
                current_node = node(int(parts[i]), int(parts[i+1]))
                nodes.append(current_node)
                i += 2


def node_value(node, all_nodes, all_meta, value):
    if node.children == 0:

        for meta in all_meta:
            if meta.node_id == node.id:
                meta_sum = 0
                for number in meta.values:
                    meta_sum += number
        return meta_sum
    
    else:

        all_children = []
        for thing in all_nodes:
            if thing.parent == node.id:
                all_children.append(thing)

        for meta in all_meta:
            if meta.node_id == node.id:
                relevant_children = meta.values
                break
        
        for child in relevant_children:
            try:
                value += node_value(all_children[child-1], all_nodes, all_meta, 0)
            except IndexError:
                pass
        
        return value


def part2(data):
    parts = data.strip().split()

    node = namedtuple("node", ["id", "parent", "children", "meta_number"])
    meta = namedtuple("meta", ["node_id", "values"])

    all_nodes = []
    all_meta = []
    nodes = []
    node_number = 1
    parent = 1
    nodes.append(node(id = node_number, parent = 0, children=int(parts[0]), meta_number = int(parts[1])))
    all_nodes.append(node(id = node_number, parent = 0, children=int(parts[0]), meta_number = int(parts[1])))
    i = 2

    while True:

            current_node = nodes[-1]

            if current_node.children == 0:
                current_node = nodes.pop()
                meta_numbers = []
                for z in range(i, i+current_node.meta_number):
                    meta_numbers.append(int(parts[z]))
                new_meta = meta(node_id=current_node.id, values=meta_numbers)
                all_meta.append(new_meta)
                i = z + 1
                try:
                    last_node = nodes.pop()
                    nodes.append(node(id = last_node.id, parent = last_node.parent, children=last_node.children-1, meta_number=last_node.meta_number))
                    parent = last_node.parent
                except IndexError:
                    break
                
            else:
                node_number += 1
                parent = current_node.id
                current_node = node(id = node_number, parent=parent, children = int(parts[i]), meta_number=int(parts[i+1]))
                nodes.append(current_node)
                all_nodes.append(current_node)
                i += 2

    for thing in all_nodes:
        if thing.id == 1:
            root_node = thing

    return node_value(root_node, all_nodes, all_meta, 0)




if __name__ == "__main__":
    main()