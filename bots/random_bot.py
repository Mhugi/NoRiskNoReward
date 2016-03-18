from warhead.protocol.ttypes import *

from warhead.util import *

import random

def get_k_subsets_aux(n, k, current_k_sum, calculated_k_sums):
    if len(current_k_sum) == k:
        if (sum(current_k_sum) == n):
            calculated_k_sums.append(current_k_sum)
    elif len(current_k_sum) < k:
        for i in range(n+1 - sum(current_k_sum)):
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

    def get_move_for_turn(self, turn_num, reinforcement_count, world):
        move = Move([], [])
        
        # Place reinformements on your cells
        try:
            raise NotImplementedError("Place your own reinforment logic here")
        except Exception, err:
            try:
                print ("ERROR: An exception of type %s occured with the following message %s\n" %
                       (str(type(err)), str(err)) + "Assigning a random reinforcement move.")
                move = Bot.assign_random_reinforcements(self, move, turn_num, reinforcement_count, world)
                
            except Exception, random_err:
                print ("ERROR: An exception of type %s occured during RANDOM MOVE with the following message %s\n" %
                       (str(type(random_err)), str(random_err)))
            
        # Move forces / attack
        try:
            raise NotImplementedError("Place your own move / attack logic here")
            
        except Exception, err:
            try:
                print ("ERROR: An exception of type %s occured with the following message %s\n" %
                       (str(type(err)), str(err)) + "Assigning a random reinforcement move.")
                move = Bot.assign_random_attacks(self, move, turn_num, reinforcement_count, world)
                
            except Exception, random_err:
                print ("ERROR: An exception of type %s occured during RANDOM MOVE with the following message %s\n" %
                       (str(type(random_err)), str(random_err)))

        return move