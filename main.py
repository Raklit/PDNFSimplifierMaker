import Absorbator
import Includer
import BoolFunc

def vectorFromBits(inp):
    return [v == '1' for v in inp if v in ['0', '1']]

def readFromFile(filename):
    vectors = list()
    f = open(filename, 'r')
    for line in f:
        vectors.append(vectorFromBits(line))
    f.close()
    return vectors

def vectorToStr(vector):
    result = ''
    for v in vector:
        if v: result += '1'
        else: result += '0'
    return result

def test():
    bf = BoolFunc.BoolFunc()
    vector = vectorFromBits('0' + '1' * 126 + '0')
    bf.setFromVector(vector)
    a = Absorbator.Absorbator(bf)
    print('Start absorbator')
    a.absorb()
    print(a.bf)
    
    inc = Includer.Includer(a.bf)
    print('Start includer')
    inc.simplify()
    print(inc.bf)
    
    s = input('Press any key for exit...')

def main():
    vectors = readFromFile('input.txt')
    bf = BoolFunc.BoolFunc()
    ab, inc = None, None
    for vector in vectors:
        print('Function')
        print(vectorToStr(vector))
        bf.setFromVector(vector)
        ab = Absorbator.Absorbator(bf)
        print('Start absorbator')
        ab.absorb()
        print(ab.bf)
        inc = Includer.Includer(ab.bf)
        print('Start includer')
        inc.simplify()
        print(inc.bf)
        print()
        print('Answer')
        print(inc.bf)
        print()
    s = input('Press any key for exit...')

if __name__ == '__main__':
    main()
