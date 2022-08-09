import random
def toString(n,queenspos):
    s=[["." for i in range(n)] for j in range(n)]
    for i in range(n):
        s[i].append("\n")
        s[i][queenspos[i]]="Q"
    s2=[]
    for sublist in s:
        s2.extend(sublist)
    
    return "".join(s2)


def findconflict(queenspos, row, col,n):
    conflict=0
    for i in range(n):
        if i!=row:
            if abs(i-row)==abs(queenspos[i]-col):
                conflict=conflict+1
    return conflict

def movQueen(pos,queenspos,n,fixed_queen):
    npos=-1
    minconflict=n
    for i in range(n):
        if i!=pos and i!=fixed_queen[0]:
            queenspos[i],queenspos[pos]=queenspos[pos],queenspos[i]
            conflict=findconflict(queenspos,i,queenspos[i],n)
            if conflict<minconflict:
                npos=i
                minconflict=conflict
            queenspos[i],queenspos[pos]=queenspos[pos],queenspos[i]

    if npos!=-1:
        queenspos[npos],queenspos[pos]=queenspos[pos],queenspos[npos]




def solveNQUtil(fixed_queen, n,timer,queenspos):
    timer=timer+1
    maxconflict=0
    row=-1
    for i in range(n):
        if i!= fixed_queen[0]:
            conflict=findconflict(queenspos,i,queenspos[i],n)
            if conflict>maxconflict:
                row=i
                maxconflict=conflict
    if  maxconflict==0:
        return True
    if timer>1000:
        return False
    movQueen(row,queenspos,n,fixed_queen)

    return solveNQUtil(fixed_queen, n,timer+1,queenspos)
    

def solve_n_queens(n, fixed_queen):
    queenspos=[]
    pos=list(range(0,n))
    pos.remove(fixed_queen[1])
    for i in range(n):
        if i!=fixed_queen[0]:
            randomIndex = random.randint(0,len(pos)-1)
            queenspos.append(pos[randomIndex])
            pos.remove(pos[randomIndex])
        else:
            queenspos.append( fixed_queen[1])
    if solveNQUtil(fixed_queen,n,0,queenspos)==True: 
        return toString(n,queenspos)
    else:
        return None




