# The graph class and graph methods
import json
from warhead.protocol.ttypes import *
from warhead.util import *

class Bot(object):
    def get_move_for_turn(self, num_turn, reinforcement_count, world):  
      g = Graph() # create new graph
      hlpr = helper(g,world) # a helper class to tranfer board to graph
      hlpr.transferBoardToGraph() # transfer
      hlpr.printGraph() # print
      # helper ends
      return Move([], [])
      