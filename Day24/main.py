import time
import utils
from copy import deepcopy


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


class Group:

    def __init__(self:"Group", type:str, units:int, hit_points:int, weaknesses:list[str] | None, immunities:list[str] | None, attack_damage:int, attack_type:str, initiative:int) -> None:
        self.type = type # infection, immune_system
        self.units = units
        self.hit_points = hit_points 
        self.weaknesses = weaknesses or []
        self.immunities = immunities or []
        self.attack_damage = attack_damage
        self.attack_type = attack_type # slashing, bludgeoning, cold, radiation, fire
        self.initiative = initiative

    @property 
    def effective_power(self) -> int:
        return self.units * self.attack_damage


    def __gt__(self, other:"Group") -> bool:
        return self.initiative > other.initiative


    def __lt__(self, other:"Group") -> bool:
        return self.initiative < other.initiative


    def __repr__(self) -> str:
        return f"Group({self.type}, {self.units}, {self.hit_points}, {self.weaknesses}, {self.immunities}, {self.attack_damage}, {self.attack_type}, {self.initiative})"

    
    def choose_target(self, groups:list["Group"], being_attacked:set["Group"]) -> tuple["Group", int] | tuple[None, None]:
        '''
        Takes in a particular group, the list of all groups, and a set containing all the targets chosen thus far this round.
        Identify the enemies and decide which one of them to target, if any.
        Return the chosen group to attack.
        '''
        possibles=[]
        for group in groups:
            if self.type != group.type:
                if self.attack_type in group.immunities:
                    continue
                if self.attack_type in group.weaknesses:
                    possibles.append((2*self.effective_power, group, 2))
                else:
                    possibles.append((self.effective_power, group, 1))
        
        possibles = sorted(possibles, key = lambda p: (p[0], p[1].effective_power, p[1].initiative), reverse=True)

        if possibles:
            for i in range(len(possibles)):
                if possibles[i][1] not in being_attacked:
                    return (possibles[i][1], possibles[i][2])

        return None, None
    

    @staticmethod
    def fight(attacks:list[tuple["Group", "Group", int]]) -> bool:
        '''
        Takes in a list of tuples, where each tuple represents (attacking group, defending group).
        Sorts attacking groups by initiative, and go through one by one.
        First check each attacker to make sure they are still alive.
        Then stage each attack, updating the relevant values of the defending group.
        Returns true if someone was damaged, false if no one took any damage
        '''

        attacks = sorted(attacks, key=lambda x: x[0].initiative, reverse=True) 
        anyone_killed = False

        for attacker, defender, multiplier in attacks:
            if attacker.units > 0:
                attack_power = multiplier * attacker.effective_power
                units_killed = attack_power // defender.hit_points
                defender.units -= units_killed
                if units_killed > 0:
                    anyone_killed = True
        
        return anyone_killed



    @staticmethod
    def is_fight_over(groups:list["Group"]) -> bool:
        '''
        Takes in the list of all groups and checks to see if all remaining groups are of the same type.
        Returns True if only one group type left. Otherwise False.
        '''
        return len(set(x.type for x in groups)) == 1
    

    @staticmethod
    def final_score(groups:list["Group"]) -> int:
        '''
        Takes in the list of all groups, which at this point will all be of one type.
        Determines the final score, which is the total number of units remaining.
        '''
        return sum(x.units for x in groups)
    

    def is_immune_winner(groups:list["Group"]) -> bool:
        '''
        For part 2, checks to see if all the remaining groups are immune system groups.
        Returns true if yes, false if no.
        '''
        return all(g.type == "immune_system" for g in groups)


def sample_data(boost):
    groups = []
    groups.append(Group("immune_system", 17, 5390, ["radiation", "bludgeoning"], None, boost+4507, "fire", 2))
    groups.append(Group("immune_system", 989, 1274, ["bludgeoning", "slashing"], ["fire"], boost+25, "slashing", 3))
    groups.append(Group("infection", 801, 4706, ["radiation"], None, 116, "bludgeoning", 1))
    groups.append(Group("infection", 4485, 2961, ["fire", "cold"], ["radiation"], 12, "slashing", 4))

    return groups


def input_data(boost):
    groups = []
    groups.append(Group("immune_system", 3115, 1585, ["slashing", "bludgeoning"], None, boost+4, "slashing", 7))
    groups.append(Group("immune_system", 3866, 6411, ["cold", "radiation"], ["fire"], boost+14, "slashing", 11))
    groups.append(Group("immune_system", 40, 10471, ["bludgeoning", "slashing"], ["cold"], boost+2223, "cold", 3))
    groups.append(Group("immune_system", 1923, 2231, ["slashing", "fire"], None, boost+10, "bludgeoning", 13))
    groups.append(Group("immune_system", 4033, 10164, None, ["slashing"], boost+22, "radiation", 5))
    groups.append(Group("immune_system", 36, 5938, ["bludgeoning", "cold"], ["fire"], boost+1589, "slashing", 4))
    groups.append(Group("immune_system", 2814, 7671, ["cold"], None, boost+21, "radiation", 15))
    groups.append(Group("immune_system", 217, 9312, None, ["slashing"], boost+345, "radiation", 8))
    groups.append(Group("immune_system", 38, 7686, ["bludgeoning"], None, boost+1464, "radiation", 14))
    groups.append(Group("immune_system", 5552, 3756, ["slashing"], None, boost+6, "fire", 10))
    groups.append(Group("infection", 263, 28458, ["fire", "radiation"], None, 186, "cold", 9))
    groups.append(Group("infection", 137, 29425, ["cold"], ["fire"], 367, "radiation", 1))
    groups.append(Group("infection", 2374, 41150, ["cold"], ["bludgeoning", "slashing", "radiation"], 34, "bludgeoning", 6))
    groups.append(Group("infection", 1287, 24213, None, ["fire"], 36, "cold", 17))
    groups.append(Group("infection", 43, 32463, ["radiation"], ["slashing", "bludgeoning"], 1347, "fire", 16))
    groups.append(Group("infection", 140, 51919, ["slashing", "bludgeoning"], None, 633, "fire", 12))
    groups.append(Group("infection", 3814, 33403, None, None, 15, "fire", 19))
    groups.append(Group("infection", 3470, 44599, ["slashing", "radiation"], None, 23, "radiation", 18))
    groups.append(Group("infection", 394, 36279, None, None, 164, "fire", 20))
    groups.append(Group("infection", 4288, 20026, None, None, 7, "radiation", 2))

    return groups


def part1():
    # groups = sample_data(0)
    groups = input_data(0)

    while True:
        attacks = []
        being_attacked = set()
        for group in sorted(groups, key = lambda g: (g.effective_power, g.initiative), reverse=True):
            target, multiplier = group.choose_target(groups, being_attacked)
            if target:
                attacks.append((group, target, multiplier))
                being_attacked.add(target)

        anyone_killed = Group.fight(attacks)
        if not anyone_killed:
            break

        groups = [g for g in groups if g.units > 0]
        
        if Group.is_fight_over(groups):
            return Group.final_score(groups)
    
        

def part2():

    boost = 0

    while True:
        boost += 1
        # groups = sample_data(boost)
        groups = input_data(boost)

        while True:
            attacks = []
            being_attacked = set()
            for group in sorted(groups, key = lambda g: (g.effective_power, g.initiative), reverse=True):
                target, multiplier = group.choose_target(groups, being_attacked)
                if target:
                    attacks.append((group, target, multiplier))
                    being_attacked.add(target)

            anyone_killed = Group.fight(attacks)
            if not anyone_killed:
                break

            groups = [g for g in groups if g.units > 0]
            
            if Group.is_fight_over(groups):
                if Group.is_immune_winner(groups):
                    return Group.final_score(groups)
                else:
                    break



if __name__ == "__main__":
    main()