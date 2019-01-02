import copy
import itertools

class FuncElement:

    def __init__(self, values):
        self.values = values

    def __str__(self):
        result = ''
        for v in self.values:
            if v == True:
                result += '1'
            elif v == False:
                result += '0'
            else:
                result += '-'
        return result
    
    def equal(self, element):
        for v1, v2 in zip(self.values, element.values):
            if v1 != v2: return False
        return True

    def include(self, element):
        for v1, v2 in zip(self.values, element.values):
            if v1 is not None and v1 != v2: return False
        return True

    def comboInclude(self, elementList):
        n = len(self.values)
        combinations = itertools.product([False, True], repeat = n)
        for item in combinations:
            #get value of element on set
            v1 = True
            for i in range(n):
                if self.values[i] == True: v1 = v1 and item[i]
                elif self.values[i] == False: v1 and not item[i]
                if not v1: break
            #get value of element list on same set
            v2 = False
            for element in elementList:
                temp = True
                for i in range(n):
                    if element.values[i] == True: temp = temp and item[i]
                    elif element.values[i] == False: temp = temp and not item[i]
                    if not temp: break
                if temp:
                    v2 = True
                    break
            #compare values
            if v1 != v2: return False
        return True
    
    def canUnite(self, element):
        pos, n = -1, len(self.values)
        for i in range(n):
            v1, v2 = self.values[i], element.values[i]
            if v1 != v2:
                if pos != -1: return False, []
                pos = i
        if pos == -1:
            return False, []
        else:
            result = FuncElement(list(copy.copy(self.values)))
            result.values[pos] = None
            return True, result

    def getVector(self):
        n = len(self.values)
        combinations = itertools.product([False, True], repeat = n)
        result = list()
        for item in combinations:
            v = True
            for i in range(n):
                if self.values[i] == True: v = v and item[i]
                elif self.values[i] == False: v = v and not item[i]
                if not v: break
            result.append(v)
        return result


    def __deconStep(self):
        n = len(self.values)
        item1, item2 = None, None
        flag = False
        oldList = list()
        for i in range(n):
            v = self.values[i]
            newList = list()
            if v == None:
                flag = True
                item1, item2 = FuncElement(copy.copy(self.values)), FuncElement(copy.copy(self.values))
                item1.values[i], item2.values[i] = False, True
                #compute new elements
                newList.extend(item1.__deconStep())
                newList.extend(item2.__deconStep())
                #save old elements
                oldList.append(item1)
                oldList.append(item2)
        if flag:
            return oldList + newList
        else:
            return [self]

    def doOneLevelList(self, L):
        if len(L) == 0: return []
        elif type(L[0]) == type(list()):
            return self.doOneLevelList(L[0]) + self.doOneLevelList(L[1::])
        else:
            return [L[0]] + self.doOneLevelList(L[1::])

    def deconstruct(self):
        return self.__deconStep()
        
    def getGroup(self):
        return self.values.count(True)
