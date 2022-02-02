import matplotlib.pyplot as plt
import random
import pandas as pd

df_loc=pd.read_csv("DMAI_Lab12_data/location.csv")
df_dis=pd.read_csv("DMAI_Lab12_data/distances.csv")
dict_loc={row.ID:[row.longitude,row.latitude] for row in df_loc.itertuples()}
dict_dis={(row.fromnode,row.tonode):row.c for row in df_dis.itertuples()}

def fitness(G):
    dis=dict_dis[(G[-1],G[0])]
    for i in range(len(G)-1):
        dis+=dict_dis[(G[i],G[i+1])]
    return 1/dis*100000
        
#fitness函数值越大越好，而一个回路的总长越小越好

def getRandomIndividual():
    G=df_loc["ID"].tolist()
    part=G[1:]
    random.shuffle(part)
    return (fitness([G[0]]+part),[G[0]]+part)

def initPopulation():
    return sorted([getRandomIndividual() for i in range(MAXPOP)],reverse=True)

def visualizeIndividual(p):
    Lon,Lat=[],[]
    for n in p[1]:
        Lon.append(dict_loc[n][0])
        Lat.append(dict_loc[n][1])
    
    fig,ax=plt.subplots(1,1,figsize=(10,5),dpi=100)
    ax.plot(Lon+[Lon[0]],Lat+[Lat[0]],c='red')
    ax.scatter(Lon,Lat,c='blue')
    for n in p[1]:
        ax.annotate(n,(dict_loc[n][0],dict_loc[n][1]))

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

def crossover(p1,p2):
    ind1=random.randint(0,len(df_loc["ID"].tolist())-1)
    ind2=random.randint(0,len(df_loc["ID"].tolist())-1)
    if ind1>=ind2:
        ind1,ind2=ind2,ind1
    tempGene=p2[1][ind1:ind2]
    newGene=[]
    for g in p1[1]:
        if g not in tempGene:
            newGene.append(g)
    newGene=newGene[:ind1]+tempGene+newGene[ind1:]
    return (fitness(newGene),newGene)

def mutate(p):
    if random.uniform(0,1)<=0.1:
        return p
    
    ind1=random.randint(0,len(df_loc["ID"].tolist())-1)
    ind2=random.randint(0,len(df_loc["ID"].tolist())-1)
    ng=p[1].copy()
    ng[ind1],ng[ind2]=ng[ind2],ng[ind1]
    return (fitness(ng),ng)
    
def evolve(P):
    parents=selectParents(P,MAXPOP*2)
    Pnew=P+parents
    for i in range(MAXPOP):
        offspring=crossover(parents[i*2],parents[i*2+1])
        Pnew+=[mutate(offspring)]
    return sorted(Pnew,reverse=True)[:MAXPOP]

MAXPOP=300
P=initPopulation()
for i in range(200):
    print("iteration",i,"best=",P[0])
    P=evolve(P)

visualizeIndividual(P[0])



