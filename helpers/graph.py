# The graph class and graph methods
import json


class Node(object):
    "The node for graph. game = country index"

    # --- Fields for the game ---
    # player owning this node
    owner = 'none'

    # number of owner's army on this node
    army = 0

    # pressure from AM matrix, previous and current
    prevPressure = 0
    pressure = 0

    # worth, or value, from degree, etc
    worth = 0

    def __init__(self, name, continent):
        self.name = name
        self.continent = continent
        self.adjList = []

    def addEdge(self, neighbour):
        if neighbour not in self.adjList:
            self.adjList.append(neighbour)


class Graph(object):
    nodes = []

    def addNode(self, name, continent):
        temp = Node(name, continent)
        self.nodes.append(temp)
        return temp


##################################
## The helper methods for graph ##
##################################

class helper(object):
    def __init__(self, dg, regions=[], borders=[], attackable=[], dist=[], shape=[], continentFrac=[]):
        # the dynamic graph for use below
        self.g = dg

    def regions(self, player):
        """ split player's countries into regions = connected subgraph, of the dynamic graph dg"""
        myregions = []

        # my countries ( return a new list)
        # minestatic = player.countries.sort(key=lambda x: x.name, reverse=True)
        minestatic = sorted(player.countries)

        mine = sorted(player.countries)

        # function to find next of your connected region
        def enumNextRegion():
            # add first base to new region
            # then remove first from nodes
            newreg = [mine.pop()]
            # new region found, add
            newreg = list(set(newreg) | set(myconnected(newreg)))
            myregions.append(newreg)
            # update mine
            return list(set(mine) - set(newreg))

        # my nodes that are already checked
        self.checked = []

        # get my nodes that are connected, input radius arr
        def myconnected(radarr):
            # next radius adj nodes from radarr
            nextRad = []
            # from next radius arr, expand radius further
            for i, item in range(radarr):
                # adj to radarr element that's mine
                adjMine = list(list(set(self.g.nodes[item].adjList) & set(minestatic)) - set(self.checked))
                nextRad.append(adjMine)

            # the next radius from radarr
            nextRad = set(sum([], nextRad))

            # update checked
            self.checked = list(set(self.checked) | set(nextRad))

            # recurse while still has more
            if len(nextRad) > 0:
                return sum(list(set(nextRad) | myconnected(nextRad)), [])
            else:
                return []

        # call enum
        while len(mine) > 0:
            mine = enumNextRegion()

        # sort regions by size (desc)
        myregions = myregions.sort(key=lambda x: len(x), reverse=True)

        return myregions

    # enum the border nodes of a player
    # Ordered by the regions
    def borders(self, player):
        bnodes = []

        # start from player regions for ordering
        # for all my owned nodes n
        for n in sum(player.regions, []):
            # all its neigh is assumed mine
            neighsmine = True

            # until check, see n's neighs
            for i in g.nodes[n].adjList:
                if g.nodes[i].owner != player.name:
                    neighsmine = False

            # We want n with neigh = not mine
            if not neighsmine:
                bnodes.append(n)

        return bnodes

    # all the attackable nodes from player's borders
    #  retain ordering from borders, from regions
    def attackable(self, player, borders):
        att = []
        # for each border node of player
        for b in borders:
            # check its neighs
            for a in self.g.nodes[b].adjList:
                if (not a in player.countries) and (a not in att):
                    att.append(a)
        return att

    # find min distance between nodes i,j
    def dist(self, i, j):
        # distance 0 first, init wave
        self.d = 0
        wave = [i]
        # while next wave(radius-expand) has no j
        while not j in wave:
            # expand wave
            for n in wave:
                for k in self.g.nodes[n].adjList:
                    if not k in wave:
                        wave.append(k)
            self.d += 1

        return self.d

    # Calc the shape of a region, i.e. connected countries. by max - min
    # Return a random max/min pair of pairs
    def shape(self, player, region):
        # calc radius only for border nodes in a region
        reg = list(set(region) & set(player.borders))

        # the node-pair with min/max dist
        minpair = {'d': 50, 'nodes': []}
        maxpair = {'d': 50, 'nodes': []}

        # upperbound = reg size
        up = len(reg)

        # if reg has only one node
        if up < 1:
            return {
                'roundness': 0,
                'mins': reg,
                'maxs': reg}

        # enum pair of reg
        for i in len(up - 1):
            for j in range(i + 1,up):
                dis = self.dist(reg[i], reg[j])
                # if find new min pair, update
                if dis < minpair.d:
                    minpair.d = dis;
                    # nodes forming min-pairs
                    minpair.nodes = [i, j]
                    # minpair['i'] = i;
                    # minpair['j'] = j;

                 # if another max found, add
                if dis == minpair.d:
                    minpair.nodes.append(i)
                    minpair.nodes.append(j)

                # if find max pair, update
                if maxpair.d < dis:
                    maxpair.d = dis
                    # nodes forming max-pairs
                    maxpair.nodes = [i, j];
                    # maxpair['i'] = i;
                    # maxpair['j'] = j;

                # if another max found, add
                if dis == maxpair.d:
                    maxpair.nodes.append(i)
                    maxpair.nodes.append(j)
        # the difference in radius
        diff = maxpair.d - minpair.d
        roundness = diff/maxpair.d
        return {
            # measure roundness, 0 = round, 1 = not
            'roundness': roundness,
            'mins': map((lambda i: reg[i]), set(minpair.nodes)),
            'maxs': map((lambda i: reg[i]), set(maxpair.nodes)),
        }

    cont = None
    # continents
    with open('./srcdata/continents.json') as data_file:
        cont = json.load(data_file)

    # helper, compute fraction of continent owned
    def continentFrac(self, node):
        self.allyNum = 0
        owner = node.owner
        icont = node.continent
        contclist = self.cont[str(icont)]

        for n in contclist:
            if self.g.nodes[n].owner == owner:
                self.allyNum += 1

        return self.allyNum / len(contclist)

# helper ends

