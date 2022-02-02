import random
import numpy as np
import copy

class Knapsack:
    def __init__(self,dataset):
        f=open('DMAI_Lab2_data/%s.txt'%dataset,'r')
        input_data=f.read()
        f.close()
        lines=input_data.split('\n')
        firstLine = lines[0].split()
        self.item_count = int(firstLine[0])
        self.capacity = int(firstLine[1])
        
        self.value,self.weight={},{}
        for i in range(1,self.item_count+1):
            line=lines[i]
            parts = line.split()
            self.value[i-1]=int(parts[0])
            self.weight[i-1]=int(parts[1])
        
    def getValue(self,L):
        return sum([L[i]*self.value[i] for i in range(self.item_count)])
    
    def getWeight(self,L):
        return sum([L[i]*self.weight[i] for i in range(self.item_count)])

    #GA Part
    def getRandomIndividual(self):
        rate=self.capacity/sum(self.weight.values())
        L=[int(random.uniform(0,1)<rate) for i in range(self.item_count)]
        return (self.fitness(L),L)

    def fitness(self,L):
        if self.getWeight(L)<=self.capacity:
            return self.getValue(L)
        else:
            return 0
        
    def selectParents(self,P,nParents):
        parents=[]
        for i in range(nParents):
            choiceArea=[p[0] for p in P]
            pick=random.uniform(0,sum(choiceArea))
            val=0
            for j in range(len(P)):
                val=val+choiceArea[j]
                if val>=pick:
                    parents.append(P[j])
                    break
        return parents
    
    def crossover(self,p1,p2):
        pos=random.randint(1,self.item_count-2)
        L1n=p1[1][:pos]+p2[1][pos:]
        L2n=p2[1][:pos]+p1[1][pos:]
        return [(self.fitness(L1n),L1n),(self.fitness(L2n),L2n)]

    def mutate(self,p,mutRate):
        if random.uniform(0,1)<mutRate:
            return p
        Ln=p[1].copy()
        pos=random.randint(0,self.item_count-1)
        Ln[pos]=1-Ln[pos]
        return (self.fitness(Ln),Ln)
    
    def evolve(self,P,maxPop,mutRate):
        parents=self.selectParents(P,maxPop*2)
        Pnew=P+parents
        for i in range(maxPop):
            offspring=self.crossover(parents[i*2],parents[i*2+1])
            Pnew+=[self.mutate(p,mutRate) for p in offspring]
        return sorted(Pnew,reverse=True)[:maxPop]
    
    def GA(self,parameters):
        maxPop,numIter,mutRate=parameters
        
        P=sorted([self.getRandomIndividual() for i in range(maxPop)],reverse=True)
        for i in range(numIter):
            print("iteration",i,"best=",P[0])
            P=self.evolve(P,maxPop,mutRate)
                
ks=Knapsack("ks_100")
parameters=20,100,0.2
ks.GA(parameters)






