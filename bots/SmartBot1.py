from warhead.protocol.ttypes import *

from warhead.util import *

import random
import traceback


def get_k_subsets_aux(n, k, current_k_sum, calculated_k_sums):
    if len(current_k_sum) == k:
        if (sum(current_k_sum) == n):
            calculated_k_sums.append(current_k_sum)
    elif len(current_k_sum) < k:
        for i in range(n + 1 - sum(current_k_sum)):
            test_k_sum = list(current_k_sum)
            test_k_sum.append(i)
            # print test_k_sum
            if sum(test_k_sum) > n:
                break

            calculated_k_sums = get_k_subsets_aux(n, k, list(test_k_sum), calculated_k_sums)
            # print calculated_k_sums

    return calculated_k_sums


def get_k_subsets(n, k):
    '''
    @summary:
        Given a number n, provide all combinations of k positive (or zero)
        numbers whose sum is n.
    '''
    # print "n = " + str(n)
    # print "k = " + str(k)
    return get_k_subsets_aux(n, k, [], [])


class Bot(object):
    def __init__(self):
        pass

    checked_pressure = {}

    # Retruns the average number of enemy solder
    # that might attack a cell
    def calc_cell_pressure(self, world, cell):
        if cell in self.checked_pressure:
            return self.checked_pressure[cell]

        adj = world.get_adj_cells(cell)

        if adj == []:
            self.checked_pressure[cell] = 0
            return 0

        adj_armies = sum([cell.armySize for cell in adj])
        self.checked_pressure[cell] = adj_armies / len(adj_armies)

        return self.checked_pressure[cell]

    #
    def sort_cells_by_pressure(self, world, cells=[]):
        cells.sort(key=(lambda x: self.calc_cell_pressure(world, x)))

    def assign_random_reinforcements(self, move, turn_num, reinforcement_count, world):
        all_my_cells = list(world.get_my_cells())

        for _ in range(reinforcement_count):
            cell = random.choice(all_my_cells)
            world.add_reinforcement(move, cell, 1)

        return move

    def assign_random_attacks(self, move, turn_num, reinforcement_count, world):
        all_my_cells = list(world.get_my_cells())
        for cell in all_my_cells:
            all_my_adj_cells = world.get_adj_cells(cell)
            if len(all_my_adj_cells) == 0:
                continue

            cell_army_num = cell.armySize

            all_sets_of_attacks = get_k_subsets(cell_army_num, len(all_my_adj_cells) + 1)
            attack_vector = random.choice(all_sets_of_attacks)

            for i in range(len(all_my_adj_cells)):
                adj = all_my_adj_cells[i]
                attack_size = attack_vector[i]
                world.add_action(move, cell, adj, attack_size)

        return move

    def reinforcements(self, move, turn_num, reinforcement_count, world):
        print "Hugi reinforcmnet"
        left_to_reinforce = reinforcement_count
        all_my_cells = list(world.get_my_cells())
        sorted_pressure = sort_cells_by_pressure(world, all_my_cells)
        int
        index = 0;
        for _ in range(reinforcement_count):
            cell = sorted_pressure[index]
            world.add_reinforcement(move, cell, 1)
            index = (index + 1) % len(sorted_pressure)

    def move_and_attack(self, move, turn_num, reinforcement_count, world):
        all_my_cells = list(world.get_my_cells())

        self.sort_cells_by_pressure(world, all_my_cells)

        for cell in all_my_cells:
            all_my_adj_cells = world.get_adj_cells(cell)
            if len(all_my_adj_cells) == 0:
                continue

            cell_army_num = cell.armySize

            all_sets_of_attacks = get_k_subsets(cell_army_num, len(all_my_adj_cells) + 1)
            attack_vector = random.choice(all_sets_of_attacks)

            for i in range(len(all_my_adj_cells)):
                adj = all_my_adj_cells[i]
                attack_size = attack_vector[i]
                world.add_action(move, cell, adj, attack_size)

        return move

    def get_move_for_turn(self, move, turn_num, reinforcement_count, world):
        move = Move([], [])

        # Place reinformements on your cells
        try:
            self.reinformements(move, turn_num, reinforcement_count, world)
        except Exception, err:
            try:
                print("ERROR: An exception of type %s occured with the following message %s\n" %
                      (str(type(err)), str(err)) + "Assigning a random reinforcement move.")
                traceback.print_exc()
                move = Bot.assign_random_reinforcements(self, move, turn_num, reinforcement_count, world)

            except Exception, random_err:
                print("ERROR: An exception of type %s occured during RANDOM MOVE with the following message %s\n" %
                      (str(type(random_err)), str(random_err)))
                traceback.print_exc()

        # Move forces / attack
        try:
            self.move_and_attack(move, turn_num, reinforcement_count, world)
        except Exception, err:
            try:
                print("ERROR: An exception of type %s occured with the following message %s\n" %
                      (str(type(err)), str(err)) + "Assigning a random reinforcement move.")
                traceback.print_exc()
                move = Bot.assign_random_attacks(self, move, turn_num, reinforcement_count, world)

            except Exception, random_err:
                print("ERROR: An exception of type %s occured during RANDOM MOVE with the following message %s\n" %
                      (str(type(random_err)), str(random_err)))
                traceback.print_exc()

        return move
