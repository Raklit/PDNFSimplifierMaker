import BoolFunc
import FuncElement
import itertools

class Includer:

    def __init__(self, bf):
        self.bf = bf

    def buildCombinations(self):
        n = len(self.bf.elements)
        s = range(n)
        for i in range(0, n + 1):
            for combination in itertools.combinations(s, i):
                yield combination
    
    def simplify(self):
        vectors = [element.getVector() for element in self.bf.elements]
        for item in self.buildCombinations():
            if (self.bf.equalVectors([vectors[i] for i in item])):
                result = [self.bf.elements[i] for i in item]
                self.bf.elements = result
                break    
