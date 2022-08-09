import math 

def toString(n,queenspos):
    s=[["." for i in range(n)] for j in range(n)]
    for i in range(n):
        s[i].append("\n")
        s[i][(int)(n-math.log2(queenspos[i][1])-1)]="Q"
    s2=[]
    for sublist in s:
        s2.extend(sublist)
    
    return "".join(s2)



def test(row,ld,rd,time,rown,n,upperlim,queenspos,dire,lda,rda):
    if time==n:
        return True
    if rown>=n:
        if test(row, lda, rda,time,queenspos[0][0]-1,n,upperlim,queenspos,1,lda,rda):
            return True
        else:
            return False
        

    pos = upperlim & ~(row | ld | rd);
    if(row != upperlim):
        while(pos):
            p = pos &(~pos + 1)
            queenspos.append((rown,p))
            pos= pos - p
            if dire==0:
                ldab=lda| (p<<(time+1))
                rdab=rda| (p>>(time+1))
                if test(row| p, (ld | p) << 1, (rd | p) >> 1,time+1,rown+1,n,upperlim,queenspos,dire,ldab,rdab):
                    return True
                else:
                    queenspos.pop()

            else:
                if test(row| p, (ld | p) << 1, (rd | p) >> 1,time+1,rown-1,n,upperlim,queenspos,dire,lda,rda):
                    return True
                else:
                    queenspos.pop()
        return False
    else:
        return False





def solve_n_queens(n, fixed_queen):
    upperlim= (1 << n)-1
    queenspos=[(fixed_queen[0],2**(n-fixed_queen[1]-1))]
    row=queenspos[0][1]
    ld=row<<1
    rd=row>>1
    if test(row,ld,rd,1,fixed_queen[0]+1,n,upperlim,queenspos,0,ld,rd):
        return toString(n,queenspos)
    else:
        return None