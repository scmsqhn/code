import numpy as np
import pdb
import numpy.random as random
wrong = set()

def conflict(state,nextx):
    '定义冲突函数,state为元组，nextx为下一个皇后的水平位置，nexty为下一个皇后的垂直位置'
    nexty = int(np.sqrt(len(state)))
    for i in range(nexty):
        for j in range(nexty):
            if abs(state[i].index(j)-nextx.index(j)) in (0,nextx.index(j)-i):#若下一个皇后和前面的皇后列相同或者在一条对角线上，则冲突
                return True
    return False

def queens(num=8,state=()):
    '八皇后问题，这里num表示规模'
    for _ in range(num):
        line = [i for i in range(num)]
        np.random.shuffle(line)
        positions = tuple(line)
        if not conflict(state,positions):#位置不冲突
            if len(state) == num - 1:#若是最后一个皇后，则返回该位置
                print('state', state)
                print('positions', positions)
                yield (state,)
            else:#若不是最后一个皇后，则将该位置返回到state元组并传给后面的皇后
                for result in queens(num,state + (positions,)):
                    yield (statepositions,) + result


def __prettyp(solution):
    '打印函数'
    def line(pos,length = len(solution)):
        '打印一行，皇后位置用X填充，其余用0填充'
        return 'O'*(pos)+'X'+'O'*(length-pos-1)
    for pos in solution:
        print(line(pos))

def prettyp(solution):
    pdb.set_trace()
    '打印函数'
    def line(pos):
        '打印一行，皇后位置用X填充，其余用0填充'
        print(np.array(pos))
    for pos in solution:
        print(line(pos))


def shuff(num,line):
    line2d = []
    for _ in range(num):
        np.random.shuffle(line)
        _line = line
        line2d.extend(_line)
    return np.array(line2d).reshape(num,num)

def ifconflict_four(line2d):
    array2d = np.array(line2d)
    array2d_T = array2d.T
    for line in array2d_T:
        if len(list(set(line))) < len(line):
            return True
    print('正确答案之一')
    prettypass(array2d)
    pdb.set_trace()
    return False

def ifconflict_eight(line2d):
    nine = []
    #if ifconflict_four(line2d):
    #    return True
    for i in range(len(line2d)):
        for j in range(len(line2d)):
            for dt_i in [-1,0,1]:
                for dt_j in [-1,0,1]:
                    _i=i+dt_i
                    _j=j+dt_j
                    if _i in range(0,len(line2d)) and _j in range(0,len(line2d)):
                        if i==_i and j==_j:
                            continue
                        nine.append(line2d[_i][_j])
                        if line2d[i][j] in nine:
                            return True
    array2d = np.array(line2d)
    print('正确答案之一')
    prettypass(array2d)
    pdb.set_trace()
    return False

def prettypass(line2d):
    # '打印函数'
    ss = ''
    for line in line2d:
        for char in line:
            ss+=str(char)
            ss+=" "
    print(ss)

def run(size):
    cnt=0
    line = [i for i in range(size)]
    while(1):
        cnt+=1
        base = shuff(size,line)
        prettypass(base)
        if not str(base) in wrong:
            if not ifconflict_four(base) or cnt<-10000:
                break
            wrong.add(str(base))
    print('运算结束')

#run(5)
q = queens(3)
for i in q:
    prettyp(i)
