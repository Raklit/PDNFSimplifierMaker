import FuncElement
import math
import itertools

class BoolFunc:

    def __init__(self):
        self.vector = None
        self.elements = None
    
    def __str__(self):
        return str(tuple(str(element) for element in self.elements))

    def setFromVector(self, vector):
        self.vector = vector
        self.buildPDNF()

    def buildPDNF(self):
        self.elements = list()
        n = int(math.log2(len(self.vector)))
        combinations = itertools.product([False, True], repeat = n)
        for v, item in zip(self.vector, combinations):
            if v: self.elements.append(FuncElement.FuncElement(item))

    def setFromElements(self, elementList):
        self.elements = elementList
        self.vector = list()
        n = len(elementList[0].values)
        combinations = itertools.product([False, True], repeat = n)
        for item in combinations:
            v = False
            for element in elementList:
                temp = True
                for i in range(n):
                    if element.values[i] == True: temp = temp and item[i]
                    elif element.values[i] == False: temp = temp and not item[i]
                    if not temp: break
                if temp:
                    v = True
                    break
            self.vector.append(v)

    def equalElements(self, elementList):
        n = len(elementList[0].values)
        combinations = itertools.product([False, True], repeat = n)
        for i, item in zip(range(pow(2, n)), combinations):
            v1 = self.vector[i]
            v2 = False
            for element in elementList:
                temp = True
                for j in range(n):
                    if element.values[j] == True: temp = temp and item[j]
                    elif element.values[j] == False: temp = temp and not item[j]
                    if not temp: break
                if temp:
                    v2 = True
                    break
            if v1 != v2: return False
        return True

    def equalVectors(self, vectorList):
        n = len(self.vector)
        for i in range(n):
            v1 = self.vector[i]
            v2 = False
            for vector in vectorList:
                if vector[i] == True:
                    v2 = True
                    break
            if v1 != v2: return False
        return True
    
def main():
    bf1 = BoolFunc()
    bf1.setFromVector([False, True, True, True])
    bf2 = BoolFunc()
    bf2.setFromElements([FuncElement.FuncElement([True, None]), FuncElement.FuncElement([None, True])])
    print(bf1.equalVectors([element.getVector() for element in bf2.elements]))

if __name__ == '__main__':
    main()
