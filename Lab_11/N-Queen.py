import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def fitness(L):
    attackCount=0
    for i in range(N-1):
        for j in range(i+1,N):
            if L[i]==L[j]:
                attackCount+=1
            elif abs(i-j)==abs(L[i]-L[j]):
                attackCount+=1
    return N*(N-1)-attackCount
    
def getRandomIndividual():
    L=[random.choice(list(range(N))) for i in range(N)]
    return (fitness(L),L)

def visualizeIndividual(p):
    color1=(1,1,1)
    color2=(0,0,0)
    mat=np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if (i+j)%2==0:
                mat[i,j]=1
            else:
                mat[i,j]=-1
    my_cmap=matplotlib.colors.LinearSegmentedColormap.from_list('my_camp',[color1,color2],2)
    cs=plt.imshow(mat,cmap=my_cmap)
    plt.scatter(list(range(N)),p[1],marker='*',c='orange',s=250)
    plt.show()
    
def initPopulation():
    return sorted([getRandomIndividual() for i in range(MAXPOP)],reverse=True)

def selectParents(P,nParents):
    parents=[]
    choiceArea=[p[0] for p in P]
    for i in range(nParents):
        pick=random.uniform(0,sum(choiceArea))
        val=0
        for j in range(len(P)):
            val=val+choiceArea[j]
            if val>=pick:
                parents.append(P[j])
                break
    return parents

def recombine(p1,p2):
    pos=random.randint(1,N-2)
    b1n=p1[1][:pos]+p2[1][pos:]
    b2n=p2[1][:pos]+p1[1][pos:]
    return [(fitness(b1n),b1n),(fitness(b2n),b2n)]

def mutate(p):
    if random.uniform(0,1)<0.1:
        return p
    bn=p[1].copy()
    bn[random.randint(0,N-1)]=random.randint(0,N-1)
    return (fitness(bn),bn)

def evolve(P):
    parents=selectParents(P,MAXPOP*2)
    Pnew=P+parents
    for i in range(MAXPOP):
        offspring=recombine(parents[i*2],parents[i*2+1])
        Pnew+=[mutate(p) for p in offspring]
    return sorted(Pnew,reverse=True)[:MAXPOP]

def generation(n):
    P=initPopulation()
    for i in range(n):
        print("iteration",i,"best=",P[0])
        P=evolve(P)
    visualizeIndividual(P[0])

N=8
MAXPOP=40
generation(100)
    
    
    
