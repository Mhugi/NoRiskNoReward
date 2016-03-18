from warhead.protocol.ttypes import *

from warhead.util import *

class Bot(object):
    def get_move_for_turn(self, num_turn, reinforcement_count, world):
        return Move([], [])