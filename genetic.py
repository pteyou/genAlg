import random
import statistics
import time
import sys


class fitness:
    def __init__(self, numberSeqCount, totalGap):
        self.numberSeqCount = numberSeqCount
        self.totalGap = totalGap
        
    def __str__(self):
        return 'nbSeq = {}\t totalGap = {} '.format(self.numberSeqCount, self.totalGap)
    
    def __gt__(self, other):
        if self.numberSeqCount != other.numberSeqCount:
            return self.numberSeqCount > other.numberSeqCount
        else:
            return self.totalGap < other.totalGap

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
    newfitness = getFitness(res)
    return Chromosome(res, newfitness)

def _mutate(parent, GeneSet, getFitness):
    idx = random.randrange(0, len(parent))
    newGene, alternative = random.sample(GeneSet, 2)
    res = parent.Genes[:]
    res[idx] = alternative if newGene == res[idx] else newGene
    newfitness = getFitness(res)
    return Chromosome(res, newfitness)

def _mutate_custom(parent, custom_mutate, getFitness):
    childGenes = parent.Genes[:]
    custom_mutate(childGenes)
    newfitness = getFitness(childGenes)
    return Chromosome(childGenes, newfitness)


def _generate_improvement(generateParent, newChild):
    parent = generateParent()
    yield parent
    while True:
        offspring = newChild(parent)
        if parent.Fitness > offspring.Fitness:
            continue
        if not offspring.Fitness > parent.Fitness:
            parent = offspring
            continue
        yield offspring
        parent = offspring
    
def getBest(ltarget, GeneSet, getFitness, FnDisplay, optimalFitness, custom_mutate=None):
    random.seed()
    def FnGenParent():
        return _generate_parent(ltarget, GeneSet, getFitness)

    if custom_mutate is None:
        def FnNewChild(parent):
            return  _mutate(parent, GeneSet, getFitness)
    else:
        def FnNewChild(parent):
            return _mutate_custom(parent, custom_mutate, getFitness)

    for improvement in _generate_improvement(FnGenParent, FnNewChild):
        FnDisplay(improvement)
        if not optimalFitness > improvement.Fitness:
            return improvement


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



