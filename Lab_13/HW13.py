import random
import math
import numpy as np

def f(x):
    return math.sin(x)

def getBoundary(a,b):
    xs=list(np.arange(a,b+0.001,0.001))
    ys=[f(x) for x in xs]
    return [min(ys),max(ys)]
    
def MonteCarlo(a,b,N):
    ya,yb=getBoundary(a,b)
    squareArea=(yb-ya)*(b-a)
    Upper,Lower,Outside=[],[],[]
    for i in range(N):
        x=random.uniform(a,b)
        y=random.uniform(ya,yb)
        if 0<=y<=f(x):
            Upper.append((x,y))
        elif f(x)<=y<=0:
            Lower.append((x,y))
        else:
            Outside.append((x,y))
    integral=(len(Upper)-len(Lower))/(len(Upper)+len(Lower)+len(Outside))*squareArea
    
    fig,ax=plt.subplots(1,1,figsize=(6,6),dpi=100)
    xsU,ysU=list(zip(*Upper))
    xsL,ysL=list(zip(*Lower))
    ax.plot(xsU,ysU,'kx',c='g')
    ax.plot(xsL,ysL,'kx',c='b')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title("Integral=%f"%integral)

MonteCarlo(0,np.pi*2,10000)

