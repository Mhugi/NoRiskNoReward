import json

from scipy.io.matlab.tests.test_streams import fs

from helpers import graph
from helpers.graph import Graph

rawMap = None
rawCont = None

with open('./srcdata/world-map.pyg', 'r', encoding='utf8') as f:
    rawMap = f.read().splitlines()

with open('./srcdata/world-continent.txt', 'r', encoding='utf8') as f:
    rawCont = f.read().splitlines()

# out map
g = Graph()

# the list 0-41, representing countries
clist = range(0, 42)


def ContinentTxt2Json():
    # the continents: key-array map
    cont = {}
    # add to continents
    for line in rawCont:
        line_ = line.split(" ")
        con = line_[0]
        country = line_[1]

        # add country(index) to each continent
        cont[con] = list(set(cont[con]) | [int(country)])

    with open('./srcdata/continents.json', 'rw', encoding='utf8') as f:
        json.dump(cont, f)

        # fs.writeFileSync('./srcdata/continents.json', JSON.stringify(cont, null, 4));


def makeG():
    conti = {}
    for touple_ in list(map((lambda c: c.split(" ")), rawCont)):
        conti[int(touple_[1])] = touple_[0]

    # there's 42 countries indexed  0-41; access by g.nodes[i]
    for country in clist:
        g.addNode(country, conti[country])

    for line in rawMap:
        line_ = line.split(" ")
        # line is now [src, -, target, dist]
        src = int(line_[0])
        tar = int(line_[2])

        #  add neigh's key instead of object (g is undirected)
        g.nodes[src].addEdge(tar)
        g.nodes[tar].addEdge(src)

makeG()

print(g.nodes[0].adjList)