
import random
import statistics
import time
import sys

class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

    def __len__(self):
        return len(self.Genes)


def _generate_parent(size, GeneSet, getFitness):
    size_field = len(GeneSet)
    res = []
    while len(res) < size:
        length = min(size_field, size - len(res))
        res.extend(random.sample(GeneSet, length))
    newgenes = ''.join(res)
    newfitness = getFitness(newgenes)
    return Chromosome(newgenes, newfitness)

def _mutate(parent, GeneSet, getFitness):
    idx = random.randrange(0, len(parent))
    newGene, alternative = random.sample(GeneSet, 2)
    res = list(parent.Genes)
    res[idx] = alternative if newGene == res[idx] else newGene
    newgenes = ''.join(res)
    newfitness = getFitness(newgenes)
    return Chromosome(newgenes, newfitness)

def getBest(ltarget, GeneSet, getFitness, FnDisplay, optimalFitness):
    random.seed()
    BestGuess = _generate_parent(ltarget, GeneSet, getFitness)
    FnDisplay(BestGuess)
    if BestGuess.Fitness >= optimalFitness:
        return BestGuess
    while True:
        offspring = _mutate(BestGuess, GeneSet, getFitness)
        if offspring.Fitness <= BestGuess.Fitness:
            continue
        FnDisplay(offspring)
        if offspring.Fitness >= optimalFitness:
            return offspring
        BestGuess = offspring

class NullWriter():
    def write(self, s):
        pass

class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = NullWriter()
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i <= 10 or i % 10 == 0:
                print('step {0}\t mean {1:3.2f}\t stddev {2:3.2f}'.format(1+i, mean,
                            statistics.stdev(timings, mean) if i > 1 else 0))



