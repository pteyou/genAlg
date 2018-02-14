import unittest, datetime, genetic
import csv

def readEntry(entryFname):
    with open(entryFname, mode='r') as infile:
        reader = csv.reader(infile)
        adjDict = {row[0] : row[1].split(';') for row in reader if row}
    return  adjDict

class Rule:
    def __init__(self, state, adjacent):
        if state < adjacent:
            state, adjacent = adjacent, state
        self.Node = state
        self.Adjacent = adjacent

    def __eq__(self, other):
        return self.Node == other.Node and self.Adjacent == other.Adjacent

    def __str__(self):
        return self.Node + "-->" + self.Adjacent

    def __hash__(self):
        return hash(self.Node) * 397 ^ hash(self.Adjacent)

def buildRules(adjDict):
    addedRules = {}
    for node, adjacent in adjDict.items():
        for adjState in adjacent:
            if adjState == '':
                continue
            rule = Rule(node, adjacent)
            if rule in addedRules:
                addedRules[rule] += 1
            else:
                addedRules[rule] = 1
    # verification
    for k,v in addedRules.items():
        if v != 2:
            print ("error : state {} is not correctly connected".format(k))
            exit(-1)
    return addedRules.keys()


class graphColoringTests(unittest.TestCase):
    def test(self):
        rules = buildRules(readEntry('usa.csv'))
