import unittest, datetime, genetic
import csv

def readEntry(entryFname):
    with open(entryFname, mode='r') as infile:
        reader = csv.reader(infile)
        adjDict = {row[0] : row[1].split(';') for row in reader if row}
    return  adjDict

def convertCsvToCol(ifname):
    states = readEntry(ifname)
    output = []
    nbNodes = nbEdges = 0
    for node, adjacents in states.items():
        nbNodes += 1
        for adjacent in adjacents:
            if adjacent ==  '':
                output.append('n {} 0'.format(node))
            else:
                output.append('e {} {}'.format(node, adjacent))
                nbEdges += 1
    ofname = ifname[:-3] + 'col'
    with open(ofname, mode='w+') as outfile:
        outfile.write('p edge {} {}\n'.format(nbNodes, nbEdges))
        for line in sorted(output):
            outfile.write(line + '\n')

def load_col_data(ifname):
    nodes = set()
    rules = set()
    with open(ifname, mode='r') as infile:
        contents = infile.read().splitlines()
    for line in contents:
        if line[0] == 'e':
            nodeIds = line.split(' ')[1:3]
            rules.add(Rule(nodeIds[0], nodeIds[1]))
            nodes.add(nodeIds[0])
            nodes.add(nodeIds[1])
            continue
        if line[0] == 'n':
            nodeIds = line.split(' ')
            nodes.add(nodeIds[1])
    return nodes, rules


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

    def IsValid(self, genes, nodeIdxLookup):
        index = nodeIdxLookup[self.Node]
        adjIndex = nodeIdxLookup[self.Adjacent]
        return genes[index] != genes[adjIndex]

def buildRules(adjDict):
    addedRules = {}
    for node, adjacent in adjDict.items():
        for adjState in adjacent:
            if adjState == '':
                continue
            rule = Rule(node, adjState)
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
    def test_states(self):
        self.color('usa.col', ["Orange", "Yellow", "Green", "Blue"])

    def test_R100_1gb(self):
        self.color('r100_1gb.col', ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo"])

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test_R100_1gb())

    def color(self, fname, colors):
        nodes, rules = load_col_data(fname)
        optimalValue = len(rules)
        stateIndexLookup = {key : index for index, key in enumerate(sorted(nodes))}
        colorLookup = {color[0] : color for color in colors}
        geneset = list(colorLookup.keys())

        startTime = datetime.datetime.now()
        def FnDisplay(candidate):
            return display(candidate, startTime)

        def getFitness(genes):
            return get_fitness(genes, rules, stateIndexLookup)

        BestGuess = genetic.getBest(len(nodes), geneset, getFitness, FnDisplay, optimalValue)
        self.assertTrue(not optimalValue > BestGuess.Fitness) # redondant

        keys = sorted(nodes)
        for i in range(len(nodes)):
            print (keys[i] + ' is ' + colorLookup[BestGuess.Genes[i]])

def display(guess, startTime):
    timediff = datetime.datetime.now() - startTime
    print('{0}\t{1}\t{2}'.format(''.join(map(str, guess.Genes)), guess.Fitness, timediff))

def get_fitness(genes, rules, stateIndexLookup):
    return sum(1 for rule in rules if rule.IsValid(genes, stateIndexLookup))

if __name__ == '__main__':
    unittest.main()
    #convertCsvToCol('usa.csv')