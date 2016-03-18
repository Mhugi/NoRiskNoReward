def uniqMat(mat):
    # TODO: return a uniq matrix
    return  mat

class RadiusMatrix(object):
    """  """

    def __init__(self, g):
        self.g = g

    clist = range(0,42)

    checked = []

    mat = []

    newmat = []

    # Matrix helper recursive function:
    # Scan for countries in next radius for "level" times
    def nextRaidus(self, level):
        for row in self.mat:
            last = row[-1]

            if not last is None:
                for adj in g.nodes[last].adjList:
                    newrow = list(row)


                    if not adj in self.checked:
                        newrow.append(adj)
                    else:
                        newrow.append(-1)

                    self.newmat.append(newrow)
            else:
                newrow = list(row)
                newrow.append(-1)
                self.newmat.append(newrow)

        # Done with every row
        # reset mat as the expanded version (no duplicate rows)
        self.mat = uniqMat(self.mat)

        mat = uniqMat(self.newmat)

        newmat = []

        checked = list(set(self.checked) | sum([], mat))

        level -= 1

        # continue recursively
        if level > 1:
            self.nextRadius(level)

        return mat
    #
    def computeRM(self, i):
        self.checked = [i]
        self.mat = []
        self.newmat = []
        for adj in g.nodes[i].adjList:
            self.mat.append([adj])

        checked = list(set(self.checked) | sum([], self.mat))

        # calc for 5 steps raduis
        return self.nextRaidus(5)


    def computeRMs(self):
        print('computing radius matrixes!')
        RMs = {}
        for i in self.clist:
            mat = self.computeRM(i)
            RMs[i] = mat

    ##################
    ## RM partition ##
    ##################

    ###This is directly dependent of the RM generated


    # partition RMs[i] by the first entry of RMrow.
    # returns array whose entry = number of rows with same first node,
    # array.length = the degree of country i

    def partRM(self, i):
        partdeg = []
        # init part and prevhead term
        part  = [0]

        prevhead = self.RMs[i][0][0]

        for row in self.RMs[i]:
            if row[0] is not prevhead:
                part.append(1)
                partdeg.append(len(g.nodes[prevhead].adjList))
            else:
                part.append(part.pop()+1)


