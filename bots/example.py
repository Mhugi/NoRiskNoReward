from warhead.protocol.ttypes import *

from warhead.util import *

class Bot(object):
    def __init__(self):
        pass

    def get_move_for_turn(self, turn_num, reinforcement_count, world):
        move = Move([], [])

        cell = list(world.get_my_cells())[0]
        world.add_reinforcement(move, cell, reinforcement_count)

        adj = world.get_adj_cells(cell)[0]
        world.add_action(move, cell, adj, cell.armySize)

        return move