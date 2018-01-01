import unittest
import datetime
import genetic
import random


class pWdTest(unittest.TestCase):
    genes = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    genes.extend([chr(i) for i in range(ord('A'), ord('Z') + 1)])
    GeneSet = ''.join(genes).join([' ', '!'])

    def _test_helloWorld(self):
        target = "Hello World!"
        self.guessPwd(target)

    def _test_second(self):
        target = "Hello World i a m single and poor!"
        self.guessPwd(target)

    def _test_random(self):
        length = 50
        target = ''.join([random.choice(self.GeneSet) for _ in range(length)])
        self.guessPwd(target)

    def test_benchmark(self):
        genetic.Benchmark.run(self._test_random)

    def guessPwd(self, target):
        ltarget = len(target)
        optimalFitness = ltarget
        startTime = datetime.datetime.now()

        def FnDisplay(guess):
            return display(guess, startTime)

        def getFitness(guess):
            return get_fitness(guess, target)

        BestGuess = genetic.getBest(ltarget, self.GeneSet, getFitness, FnDisplay, optimalFitness)
        self.assertEqual(BestGuess.Genes, target)


def display(guess, startTime):
    timediff = datetime.datetime.now() - startTime
    print('{0}\t{1}\t{2}'.format(guess.Genes, guess.Fitness, timediff))


def get_fitness(guess, target):
    assert len(guess) == len(target)
    return sum(1 for tried, real in zip(guess, target) if tried == real)


if __name__ == '__main__':
    unittest.main()
