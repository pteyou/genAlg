import genetic
import time
import unittest

class OneMaxTest(unittest.TestCase):
    GeneSet = [0, 1]
    def test(self, length=30):
        startTime = time.time()
        optimalFitness = length
        def fnGetFitness(candidate):
            return get_fitness(candidate)
        def fnDisplay(candidate):
            return display(candidate, startTime)

        BestGuess = genetic.getBest(length, self.GeneSet, fnGetFitness, fnDisplay, optimalFitness)
        self.assertEqual(BestGuess.Fitness, optimalFitness)

def get_fitness(gene):
    return gene.count(1)

def display(candidate, startTime):
    timeDiff = time.time() - startTime
    print('{}...{}\t{}\t{:.2e}'.format(''.join(map(str, candidate.Genes[:10])),
                                        ''.join(map(str, candidate.Genes[-10:])),
                                        candidate.Fitness,
                                        timeDiff))

if __name__ == '__main__':
    unittest.main()