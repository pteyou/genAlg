import datetime
import genetic

class Board:
    def __init__(self, genes, size):
        board = [['.'] * size for _ in range(size)]
        for i in range(0, len(genes), 2):
            row = genes[i]
            column = genes[i+1]
            board[column][row] = 'Q'
        self._board = board
    
    def printb(self):
        for line in reversed(range(len(self._board))):
            print (' '.join(self._board[line]))
    
def display(candidate, size, startTime):
    elapsed = datetime.datetime.now() - startTime
    board = Board(candidate.Genes, size)
    board.printb()
    print('{} \t -> \t {} \t {}'.format(' '.join(map(str, candidate.Genes)), 
          candidate.Fitness, elapsed))

class Fitness:
    def __init__(self, total):
        self.total = total
    def __gt__(self, other):
        return self.total < other.total
    def __str__(self):
        print('{}'.format(total))