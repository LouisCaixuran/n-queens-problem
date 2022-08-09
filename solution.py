import random
from typing import List, Tuple

class M_Queen(object):
    def __init__(self,size,fixed_queen):
        self.n = size          # n表示皇后数量
        self.queen = [0]*size  # queen[i]表示第i行的皇后在第几列
        self.attack =[0]*size  # 表示哪些皇后是可以相互攻击的
        self.diagonalNegative = []*2*size # 正反对角线的冲突数量2*n
        self.diagonalPositive = []*2*size
        # 记录某一列是不是已经放了东西了，这保证[0..n-1]序列不重不漏，所以列一定不会有冲突
        self.fixed_queen = fixed_queen
        self.columnUsed = [False] * size 
        self.columnUsed[fixed_queen[1]] = True # 设定固定点


    #   想在第row行第col列放皇后，检查这个皇后是不是和以前放的有冲突
    #   row 行数 col 列数
    #   如果没有冲突，返回true，否则，false
    def check(self, row:int, col:int) ->bool :
        negativeIndex = row + col
        positiveIndex = row - col
        return self.diagonalNegative[negativeIndex] == 0 and self.diagonalPositive[self.n - 1 + positiveIndex] == 0

    #  随机生成一个棋盘布局
    def generateARadomPermutation(self) :
        # 前THRESHOLD行要保证没有冲突，这是为了减少collision的数量，尽可能加速程序运行，这里的THRESHOLD参考了几篇论文，最终定在5/12
        THRESHOLD = (int) (5.0 / 12.0 * self.n)
        generatedQueenNumber = 0

        self.diagonalPositive = [0] * self.n * 2
        self.diagonalNegative = [0] * self.n * 2

        self.queen[self.fixed_queen[0]] = self.fixed_queen[1]
        self.columnUsed[self.fixed_queen[1]] = True
        negativeIndex = self.fixed_queen[0] + self.fixed_queen[1]
        self.diagonalNegative[negativeIndex] += 1
        positiveIndex = self.fixed_queen[0] - self.fixed_queen[1]
        self.diagonalPositive[self.n - 1 + positiveIndex] += 1   
        print(self.queen)
        while ( generatedQueenNumber < self.n) :            
            if generatedQueenNumber == self.fixed_queen[0]:
                generatedQueenNumber +=1
                continue
            col = random.randint(0,self.n-1)
            while True:
                if self.columnUsed[col] == False:  break 
                col = random.randint(0,self.n-1)

            #  前面5/12行是没有冲突的，所以放下去之前要check
            if (generatedQueenNumber < THRESHOLD):
                if (self.check(generatedQueenNumber, col) == False) : continue

            self.queen[generatedQueenNumber] = col
            self.columnUsed[col] = True
            negativeIndex = generatedQueenNumber + col
            self.diagonalNegative[negativeIndex] += 1

            positiveIndex = generatedQueenNumber - col
            self.diagonalPositive[self.n - 1 + positiveIndex] += 1
            generatedQueenNumber += 1
        print(self.queen)
    #  执行交换给定两行的皇后
    #  i 第i行  j 第j行
    def performSwap(self, i:int, j:int) :
        #  首先更新对角线的冲突数组，减去原来的冲突数
        self.diagonalNegative[i + self.queen[i]] -=1
        self.diagonalNegative[j + self.queen[j]] -=1
        self.diagonalPositive[self.n - 1 + i - self.queen[i]] -=1
        self.diagonalPositive[self.n - 1 + j - self.queen[j]] -=1
        # 交换皇后
        self.queen[i],self.queen[j] = self.queen[j],self.queen[i]

        #  把交换后增加的冲突加入到对角线冲突数组
        self.diagonalNegative[i + self.queen[i]] += 1
        self.diagonalNegative[j + self.queen[j]] += 1
        self.diagonalPositive[self.n - 1 + i - self.queen[i]] +=1
        self.diagonalPositive[self.n - 1 + j - self.queen[j]] +=1

    #  检查交换给定的两个皇后会不会减少冲突数
    #  i 第i行 ,j 第j行
    #  return 交换后的冲突数的变化量，小于0表示冲突减少  
    def swapWillReduceCollisions(self, i:int, j:int)->int :

        delta = 0
        #  计算原来正反对角线的冲突量，交换后会使得这些冲突减少
        delta =delta - (self.diagonalNegative[i + self.queen[i]] - 1)
        delta =delta - (self.diagonalNegative[j + self.queen[j]] - 1)

        #  容斥原理，如果正好是同一条对角线，要去掉重复计算的那个
        if (i + self.queen[i] == j + self.queen[j]) :
            delta = delta + 1
        
        delta =delta - (self.diagonalPositive[self.n - 1 + i - self.queen[i]] - 1)
        delta =delta - (self.diagonalPositive[self.n - 1 + j - self.queen[j]] - 1)

        if (i - self.queen[i] == j - self.queen[j]) :
            delta =delta +1
        
        # 计算新对角线的冲突量，交换后的新位置将会额外增加这些冲突
        delta =delta + self.diagonalNegative[i + self.queen[j]]
        delta =delta + self.diagonalNegative[j + self.queen[i]]

        if (i + self.queen[j] == j + self.queen[i]) :
            delta = delta +1

        delta = delta + self.diagonalPositive[self.n - 1 + i - self.queen[j]]
        delta = delta + self.diagonalPositive[self.n - 1 + j - self.queen[i]]

        if (i - self.queen[j] == j - self.queen[i]) :
            delta = delta + 1    
        return delta

    #  计算冲突
    #  return 冲突数量  
    def computeCollisions(self)->int :
        collisions = 0
        # 遍历对角线数组计算冲突数量
        for i in range(2 * self.n - 1) :
            collisions += self.diagonalNegative[i] * (self.diagonalNegative[i] - 1) / 2
            collisions += self.diagonalPositive[i] * (self.diagonalPositive[i] - 1) / 2        
        return collisions
 
    #  获得能够相互攻击的皇后的编号
    #  return 能够相互攻击的皇后的个数 
    def computeAttacks(self)->int:
        # 注：能够相互攻击的皇后数量不等于冲突数量
        self.attack =[0] * self.n
        numberOfAttacks = 0

        for i in range(self.n) :
            negativeIndex = i + self.queen[i]
            positiveIndex = i - self.queen[i]

            #  如果某皇后所在对角线有其他皇后，那就是可以攻击的，计数器加1，并记录这是第几个皇后
            if (self.diagonalNegative[negativeIndex] > 1 or self.diagonalPositive[self.n - 1 + positiveIndex] > 1) :
                self.attack[numberOfAttacks] = i
                numberOfAttacks +=1  
        return numberOfAttacks

def solve_n_queens(size:int, fixed_queen) ->List[int]:    
    if size == 1 : return "Q\n"
    if size in [0 , 2 ,3 ]: return None
    
    # C1是为了计算一个阈值，当冲突小于阈值的时候重新计算attack数组，这里的常系数定义参考了Rok sosic和Jun Gu的QS2算法的定义，C1取0.53
    C1 = 0.45
    # C2是为了最大化N较小的时候的运行速度，对较大的N没有影响，这里的常系数定义参考了Rok sosic和Jun Gu的QS2算法的定义，C2取32
    C2 = 32
    nqueen_count = 0
    while nqueen_count <= 20:
        nqueen_count +=1;
        nqueen = M_Queen(size,fixed_queen)
        nqueen.generateARadomPermutation()
        collisions = nqueen.computeCollisions()
        if (collisions == 0): break 
        limit = int(C1 * collisions)
        numberOfAttacks = nqueen.computeAttacks()
        loopCount = 0
        
        while (loopCount <= C2 * size):
            if (collisions == 0): break
            # 只遍历能够相互攻击的皇后
            for k  in  range(numberOfAttacks):
                # 找到一个具有攻击性的皇后，再随机地找一个和自己不一样的皇后
                if nqueen.attack[k] == fixed_queen[0]: continue

                i = nqueen.attack[k]
                j = random.randint(0,size-1)

                count = 0
                while (i == j or j== fixed_queen[0]):  #去除固定点
                    j = random.randint(0,size-1)
                    count +=1
                    if count > size : return None       

                delta = nqueen.swapWillReduceCollisions(i, j)
                #  如果交换后的冲突是减小的，执行交换
                if (delta < 0) :
                    # 更新冲突数，并执行交换
                    collisions += delta
                    nqueen.performSwap(i, j)

                    # 冲突数为0，找到解，输出，冲突数小于阈值，重新计算阈值和attack数组
                    if (collisions == 0) : break

                    if (collisions < limit) :
                        limit = (int) (C1 * collisions)
                        numberOfAttacks = nqueen.computeAttacks()        
            loopCount += numberOfAttacks
        if collisions == 0: break   
    if collisions == 0:
        print(nqueen.queen)  #返回[]
        str=""
        for i in range(size):
            for j in range(size):
                if nqueen.queen[i] == j:
                    str += "Q"
                else:
                    str +="." 
            str +="\n"
        return str           
    else:
        return None