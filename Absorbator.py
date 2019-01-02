import FuncElement
import BoolFunc

class Absorbator:

    def __init__(self, bf):
        self.bf = bf
        self.se = None
        self.ft = None
        self.ids = None
        self.__buildTable()

    def __buildTable(self):
        if len(self.bf.elements) == 0: return None
        n = len(self.bf.elements[0].values)
        self.se = dict()
        self.ft = dict()
        self.ids = list()
        for i in range(n + 1):
            self.se[i] = list()
            self.ft[i] = list()
        
        n = len(self.bf.elements)
        self.ids = [i for i in range(n)]
        group = None
        for i in range(n):
            group = self.bf.elements[i].getGroup()
            self.se[group].append(i)
            self.ft[group].append(False)

    def __addElement(self, element):
        index = len(self.bf.elements)
        self.ids.append(index)
        self.bf.elements.append(element)
        group = element.getGroup()
        self.se[group].append(index)
        self.ft[group].append(False)

    def __delElement(self, i):
        group = self.bf.elements[i].getGroup()
        pos = self.se[group].index(i)
        self.se[group].pop(pos)
        self.ft[group].pop(pos)
        self.ids.pop(self.ids.index(i))

    def __setFlag(self, i, v):
        group = self.bf.elements[i].getGroup()
        pos = self.se[group].index(i)
        self.ft[group][pos] = v

    def __getFlag(self, i):
        group = self.bf.elements[i].getGroup()
        pos = self.se[group].index(i)
        return self.ft[group][pos]

    def __contain(self, element):
        group = element.getGroup()
        for i in self.se[group]:
            if self.bf.elements[i].equal(element):
                return True
        return False
    
    def __delAllWhereFlag(self):
        i, n = 0, len(self.ids)
        while (i < n):
            pos = self.ids[i]
            if self.__getFlag(pos) == True:
                self.__delElement(pos)
                n -= 1
            else:
                i += 1

    def __getNearNotEmptyIndex(self, index):
        result = index
        n = len(self.se.keys())
        while True:
            if result >= n - 1: return None
            result += 1
            if len(self.se[result]) != 0: return result

    def __absorbHalfStep(self, index):
        i1 = index
        if len(self.se[i1]) == 0: return False
        i2 = self.__getNearNotEmptyIndex(index)
        if i2 is None: return False
        
        elem1, elem2 = None, None
        global_flag = False
        n, m = len(self.se[i1]), len(self.se[i2])
        k1 = 0
        while k1 < n:
            elem1 = self.bf.elements[self.se[i1][k1]]
            local_flag = False
            k2 = 0
            while k2 < m:
                elem2 = self.bf.elements[self.se[i2][k2]]
                status, new_element = elem1.canUnite(elem2)
                if status:
                    local_flag = True
                    self.__setFlag(self.se[i2][k2], True)
                    if not self.__contain(new_element):
                        global_flag = True
                        self.__addElement(new_element)
                k2 += 1
            if local_flag: self.__setFlag(self.se[i1][k1], True)
            k1 += 1
        return global_flag

    def __absorbStep(self):
        if self.se is None: return False
        n = len(self.se.keys())
        global_flag = False
        for i in range(n):
            local_flag = self.__absorbHalfStep(i)
            if local_flag: global_flag = True
        if global_flag:
            self.__delAllWhereFlag()
            return True
        else:
            return False
    
    def absorb(self):
        prev_step = True
        while prev_step:
            prev_step = self.__absorbStep()
        if self.ids is None: result = []
        else: result = [self.bf.elements[i] for i in self.ids]
        self.bf.elements = result
