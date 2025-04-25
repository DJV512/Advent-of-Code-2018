FILENAME = "input.txt"
# FILENAME = "sample9.txt"

import time
import utils
from collections import deque
from copy import copy


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, _ = part1(data.copy())
    part1_time = time.time()
    answer2 = part2(data.copy())
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

    return utils.grid_parse_dict(data)


class Unit:

    def __init__(self, position, species, attack_damage):
        self.position = position
        self.species = species
        self.health = 200
        self.attack_damage = attack_damage

    
    def __repr__(self) -> str:
        return f"({self.species}, {self.position}, {self.health})"


    def still_alive(self) -> bool:
        '''
        Checks if the unit is still alive before letting it take a turn. \n
        Necessary for when a unit dies but it hasn't yet been removed from
        the unit list, which only happens at the end of a round.
        '''
        
        return self.health > 0
    
    
    def find_possible_enemies_to_attack(self, battlefield:dict[tuple[int, int], str], units:list["Unit"]) -> None | tuple[int, int] :
        '''
        Checks if self is adjacent to one or more enemy units on the battlefield. \n
        If no attackable enemies, return None. \n
        If at least one, check how many targets. \n
        If one attackable enemy, return that one. \n
        If more than one, use choose_attack_target method to choose which to attack and return the chosen one.
        '''

        self_species = self.species
        possible_attack_targets = []
        for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]: # up, left, right, down - reading order
            adjacent = (self.position[0]+direction[0], self.position[1]+direction[1])
            if battlefield[adjacent] in ["G", "E"]:
                if self_species != battlefield[adjacent]:
                    possible_attack_targets.append(adjacent)
        
        if len(possible_attack_targets) == 0:
            return None

        elif len(possible_attack_targets) == 1:
            return possible_attack_targets[0]

        else:
            return Unit.choose_attack_target(possible_attack_targets, units)


    @staticmethod
    def choose_attack_target(targets:list[tuple[int, int]], units:list["Unit"]) -> tuple[int, int]:
        '''
        Takes list of adjacent enemy units and the list of all units. \n
        Chooses which adjacent target to attack. \n
        Chooses first on lowest hit points, and ties are broken by reading order. \n
        Returns chosen enemy unit to attack.
        '''

        lowest_health = 201
        potentials = []
        for unit in units:
            if unit.position in targets:
                if unit.health <= 0:
                    continue
                if unit.health < lowest_health:
                    lowest_health = unit.health
                    potentials = []
                    potentials.append(unit)
                elif unit.health == lowest_health:
                    potentials.append(unit)

        if len(potentials) == 1:
            return potentials[0].position
        else:
            for target in targets:
                for potential in potentials:
                    if target == potential.position:
                        return target


    
    def attack(self, unit:"Unit", battlefield:dict[tuple[int,int],str]) -> None:
        '''
        Takes a self to do the attacking, and a separate unit to be attacked. \n
        There is no return value, it just updates unit.health based on self.attack_damage. \n
        If unit.health drops to 0 or below, update the battlefield to remove that unit. \n
        Unit will not yet be removed from the unit list, that will occur at the end of the round by culling all units with health < 0. 
        '''
        
        unit.health -= self.attack_damage
        debug_print(f"{self} attacks {unit}.")
        if unit.health <= 0:
            battlefield[unit.position] = "."
            unit.position = (10000,10000)
            debug_print(f"{utils.RED}{unit} HAS DIED!{utils.RESET}")
        
        

    
    def find_possible_enemies_in_range(self, units:list["Unit"], battlefield:dict[tuple[int, int], str]) -> None | list[tuple[int, int]]:
        '''
        If the find_possible_enemies_to_attack method returns None, this method is run. \n
        It takes a self unit, the list of all units, and the battlefield map. \n
        Iterate through the list of units and identify all enemy units with open adjacent spots. \n
        For every enemy unit that has open adjacent spots, adds the open spot to a list of in range positions on the battlefield. \n
        If no empty spots in range, then return None. \n
        Otherwise, returns a list of possible open positions to move towards.
        '''

        open_spots = []
        for unit in units:
            if self != unit and self.species != unit.species and unit.health > 0:
                for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]: # up, left, right, down
                    adjacent = (unit.position[0] + direction[0], unit.position[1] + direction[1])
                    if battlefield[adjacent] == ".":
                        open_spots.append(adjacent)

        if not open_spots:
            debug_print(f"{self} has no open positions in range.")
            return None
        else:
            return open_spots


    
    def find_best_move(self, possibles:list[tuple[int, int]], battlefield:dict[tuple[int, int], str]) -> tuple[int, int] | None:
        '''
        Takes in a self unit, a list of possible positions to move towards returned from the find_possible_enemies_in_range method, and the battlefield map. \n
        Uses the reachable method to determine if each open position is actually reachable from self.position. \n
        If so, add steps and first_move to a list of move_choices. \n
        Sorts list of move_choices by the shortest distance, and then by reading order. \n
        Returns the first_move variable of the first item in the sorted move_choices list. \n
        Returns None if no open position is reachable (if move_choices is empty).
        '''
        
        if not possibles:
            return None
        else:
            start = self.position
            move_choices = []
            for possible in possibles:
                reachable, steps, first_move = Unit.reachable(start, possible, battlefield)
                if reachable:
                    move_choices.append((steps, possible, first_move))
            
            if not move_choices:
                return None
            else:
                move_choices = sorted(move_choices, key=lambda x: (x[0], x[1], x[2]))
                return move_choices[0][2]
            


    @staticmethod
    def reachable(start:tuple[int, int], end_position:tuple[int, int], battlefield:dict[tuple[int, int], str]) -> tuple[bool, int, tuple[int, int] | None]:
        '''
        Takes in a starting position, an open position adjacent to an enemy unit, and the battlefield map. \n
        Uses breadth first search to determine wehther the open position is reachable without going through wall or another unit. \n
        Returns (True, shortest distance, first_move) if the position is reachable, else (False, 0, None).
        '''

        stack = deque()
        visited = set()
        visited.add(start)
        stack.append((start, 0, [start]))

        while stack:
            position, steps, journey = stack.popleft()

            if position == end_position:
                return (True, steps, journey[1])

            for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]: # up, left, right, down
                next_position = (position[0]+direction[0], position[1]+direction[1])

                if battlefield[next_position] == "." and next_position not in visited:
                    new_journey = journey + [next_position]
                    visited.add(next_position)
                    stack.append((next_position, steps + 1, new_journey))

        return (False, 0, None)



    def move(self, move:tuple[int, int], battlefield:dict[tuple[int, int], str]) -> None:
        '''
        Takes the first_move variable returned from find_best_move method. \n
        Updates self.position to the position of the first_move. \n
        Updates the battlefield (unit moves to first_move, old unit position becomes "."). \n
        No return value.
        '''

        if move == None:
            debug_print(f"{self} has no valid moves.")
            return None
        else:
            debug_print(f"{self} moves to {move}.")

            battlefield[self.position] = "."
            battlefield[move] = self.species
            self.position = move

        
        

    @staticmethod
    def determine_turn_order(units:list["Unit"]) -> list["Unit"]:
        '''
        Takes in the list of units and sorts them by reading order based on their positions. \n
        Returns the sorted list for iteration over for that round.
        '''

        return sorted(units, key=lambda u: u.position)



    @staticmethod
    def is_battle_won(units:list["Unit"]) -> bool:
        '''
        Takes in the list of all units still in the game. \n
        Returns True if all remaining units are of one species. \n
        Returns False otherwise.
        '''

        species_left = {u.species for u in units if u.health > 0}
        return len(species_left) == 1


    @staticmethod
    def get_final_score(round:int, units:list["Unit"], starting_elves:int) -> tuple[int, bool]:
        '''
        When the is_battle_won method returns True, pass the list of all the units still in the game, and the round number, into this method. \n
        Uses round number and remaining unit health (if above 0) to determine and return final score.
        '''

        debug_print(f"Final complete {round=}")
        total_health = sum(u.health for u in units if u.health > 0)
        debug_print(f"{total_health=}")
        return (round * total_health, Unit.all_elves_still_alive(starting_elves, units))
    

    @staticmethod
    def cull_the_dead(units:list["Unit"]) -> list["Unit"]:
        '''
        Takes in the list of units, and uses a list comprehension to construct and 
        return a new list with the dead units removed.
        '''

        return [unit for unit in units if unit.health > 0]
    

    @staticmethod
    def identify_unit(position:tuple[int, int], units:list["Unit"]) -> "Unit":
        '''
        Given a position and the list of all units, identify which unit is at the given position. \n
        Return that unit at that position. \n
        If no unit at that position, return None.
        '''
        for unit in units:
            if unit.position == position:
                return unit
        return None


    @staticmethod
    def print_battlefield(units:list["Unit"], battlefield:dict[tuple[int, int], str]) -> None:
        '''
        Give the battlefield dictionary and the list of units, nicely prints the battlefield
        along with the health of all current alive units.
        '''

        max_y = max(y for y,x in battlefield.keys())+1
        max_x = max(x for y,x in battlefield.keys())+1
        min_y = min(y for y,x in battlefield.keys())
        min_x = min(x for y,x in battlefield.keys())
        for y in range(min_y, max_y):
            units_to_print = []
            for x in range(min_x, max_x):
                print(battlefield[(y,x)], end="")
                combatant = Unit.identify_unit((y,x), units)
                if combatant:
                    units_to_print.append(combatant)
            print("      ", end="")
            for unit in units_to_print:
                print(f"{unit.species}({unit.health}) ", end="")
            print()
        print()

    
    @staticmethod
    def all_elves_still_alive(starting_elves:int, units:list["Unit"]) -> bool:
        '''
        Checks to see if the number of living elf units is equal to the number of starting elf units. \n
        Returns True if they are equal. Returns False if they are not.
        '''

        remaining_elves = sum(1 for u in units if u.species == "E" and u.health > 0)
        return starting_elves == remaining_elves


   
def part1(battlefield, attack_damage=3):

    starting_elves = 0
    round = 1
    units = []
    for key in battlefield:
        if battlefield[key] in ["G", "E"]:
            if battlefield[key] == "G":
                units.append(Unit(key, battlefield[key], 3))
            else:
                units.append(Unit(key, battlefield[key], attack_damage))
                starting_elves += 1
    
    debug_print("Starting battlefield:")
    # Unit.print_battlefield(units, battlefield)
    debug_print()
    debug_print()

    while True:
        debug_print("Round ", round)
        units = Unit.determine_turn_order(units)

        for unit in units:
            if not unit.still_alive():
                debug_print(f"{unit} is dead!")
                continue
            else:

                targeted_enemy = unit.find_possible_enemies_to_attack(battlefield, units)
                if targeted_enemy:
                    targeted_enemy = Unit.identify_unit(targeted_enemy, units)
                    unit.attack(targeted_enemy, battlefield)

                    if Unit.is_battle_won(units):
                        debug_print("The battle is won!")
                        # Unit.print_battlefield(units, battlefield)
                        if unit != units[-1]:
                            return Unit.get_final_score(round-1, units, starting_elves)
                        else:
                            return Unit.get_final_score(round, units, starting_elves)
                
                else:

                    possibles = unit.find_possible_enemies_in_range(units, battlefield)
                    if possibles:
                        chosen_move = unit.find_best_move(possibles, battlefield)
                        unit.move(chosen_move, battlefield)

                        targeted_enemy = unit.find_possible_enemies_to_attack(battlefield, units)
                        if targeted_enemy:
                            targeted_enemy = Unit.identify_unit(targeted_enemy, units)
                            unit.attack(targeted_enemy, battlefield)

                            if Unit.is_battle_won(units):
                                debug_print("The battle is won!")
                                # Unit.print_battlefield(units, battlefield)
                                if unit != units[-1]:
                                    return Unit.get_final_score(round-1, units, starting_elves)
                                else:
                                    return Unit.get_final_score(round, units, starting_elves)
            debug_print()
        
        units = Unit.cull_the_dead(units)
        debug_print(f"Battlefield after {round} complete rounds:")
        # Unit.print_battlefield(units, battlefield)
        debug_print()
        debug_print()
        round += 1




def part2(battlefield):

    attack_damage = 3

    while True:
        attack_damage += 1
        outcome, all_elves_alive = part1(battlefield.copy(), attack_damage)

        if all_elves_alive:
            print(f"{attack_damage=}")
            return outcome
    
        debug_print(f"{attack_damage=}, {outcome=}, {all_elves_alive=}")



if __name__ == "__main__":
    main()