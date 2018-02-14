import unittest
import genetic
import numpy as np
import time

class testSorted(unittest.TestCase):
    genes = np.arange(100)
    def _test_five(self):
        self.sortNumber(10)
        
    def test_bench(self):
        genetic.Benchmark.run(lambda : self.sortNumber(10))
    
    def sortNumber(self, n):
        startTime = time.time()
        optimalFitness = genetic.fitness(n, 0)
        def _FnFitness(candidate):
            return _getFitness(candidate)
        
        def _FnDisplay(candidate):
            return _display(candidate, startTime)
        
        best = genetic.getBest(n, self.genes, _FnFitness, _FnDisplay, 
                               optimalFitness)
        self.assertTrue(not optimalFitness > best.Fitness)
        
def _getFitness(candidate):
    res = 1
    totalGap = 0
    for i in np.arange(1, len(candidate)):
        if candidate[i-1] < candidate[i]:
            res += 1
        else:
            totalGap += candidate[i-1] - candidate[i]
    return genetic.fitness(res, totalGap)
    
def _display(candidate, startTime):
    seconds = time.time() - startTime
    print("-> {}\t{}\t{}".format(', '.join(map(str, candidate.Genes)), candidate.Fitness, seconds))

if __name__ == '__main__':
    unittest.main()
            