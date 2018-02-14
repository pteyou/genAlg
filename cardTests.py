import genetic, datetime, unittest
import functools, operator, random

class cardTests(unittest.TestCase):
    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.atest())

    def atest(self):
        geneset = range(1, 11)
        startTime = datetime.datetime.now()
        def FnDisplay(guess):
            return display(guess, startTime)

        def getFitness(guess):
            return get_fitness(guess)

        def fnMutate(genes):
            return mutate(genes, geneset)

        optimalFitness = Fitness(36,360,0)
        best = genetic.getBest(10, geneset, getFitness, FnDisplay, optimalFitness, fnMutate)
        self.assertTrue(not optimalFitness > best.Fitness)

def mutate(genes, geneset):
    if len(genes) == len(set(genes)):
        count = random.randint(1,4)
        while count > 0:
            count -= 1
            indexA, indexB = random.sample(range(len(genes)), 2)
            genes[indexA], genes[indexB] = genes[indexB], genes[indexA]
    else:
        indexA = random.randrange(0, len(genes))
        newgene, alternative = random.sample(geneset, 2)
        genes[indexA] = alternative if genes[indexA] == newgene else newgene

def get_fitness(genes):
    groupe1sum = sum(genes[0:5])
    groupe2mul = functools.reduce(operator.mul, genes[5:10])
    totalDuplicates = len(genes) - len(set(genes))
    return Fitness(groupe1sum, groupe2mul, totalDuplicates)

def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{} - {}\t{}\t{}".format(
        ', '.join(map(str, candidate.Genes[0:5])),
        ', '.join(map(str, candidate.Genes[5:10])),
        candidate.Fitness,
        timeDiff
    ))

class Fitness:
    def __init__(self, groupe1sum, groupe2mul, totalDuplicates):
        self.Groupe1Sum = groupe1sum
        self.Goupe2Mul = groupe2mul
        sumDiff = abs(36 - groupe1sum)
        mulDiff = abs(360 - groupe2mul)
        self.totalDifference = sumDiff + mulDiff
        self.DuplicateCount = totalDuplicates

    def __str__(self):
        return("sum : {}, prod : {}, dups : {}".format(self.Groupe1Sum, self.Goupe2Mul, self.DuplicateCount))

    def __gt__(self, other):
        if self.DuplicateCount != other.DuplicateCount:
            return self.DuplicateCount < other.DuplicateCount
        else:
            return self.totalDifference < other.totalDifference

if __name__ == '__main__':
    unittest.main()