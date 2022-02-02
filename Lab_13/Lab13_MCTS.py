import matplotlib.pyplot as plt
import numpy as np
import random
import math

def generatePointsOnCircle(N):
    dtheta=2*math.pi/N
    return [(math.cos(i*dtheta),math.sin(i*dtheta)) for i in range(N)]

def computeDistance(Lxy):
    dis={}
    N=len(Lxy)
    for i in range(N):
        dis[i]={}
        for j in range(N):
            dis[i][j]=math.sqrt((Lxy[i][0]-Lxy[j][0])**2+(Lxy[i][1]-Lxy[j][1])**2)
    return dis

def computeLength(dis,path):
    n=len(path)
    leng=dis[path[-1]][path[0]]
    for i in range(n-1):
        leng+=dis[path[i]][path[i+1]]
    return leng

class MCTNode:
    def __init__(self,Path,parent,node):
        self.Path=Path+[node]
        self.parent=parent
        self.children=[]
        self.Reward=0
        self.Na=0
        self.UCB=float('inf')
        
    def updateUCB(self,Nt):
        if self.Na>0 and Nt>0:
            self.UCB=self.Reward/self.Na+math.sqrt((2*math.log(Nt))/self.Na)
        else:
            self.UCB=float('inf')
            
def RandomPath(dis,Path0):
    s=Path0[-1]
    n=len(dis)
    Left=list(set(range(n))-set(Path0))
    Path=list(Path0)
    for i in range(n-len(Path0)):
        sumD=sum([1/dis[s][j] for j in Left])
        rand=random.uniform(0,sumD)
        val=0
        for j in Left:
            val+=1/dis[s][j]
            if val>rand:
                Path.append(j)
                Left.remove(j)
                break
    return Path

def TSP_MCTS(dis,Lxy,iteration_max):
    nt=0
    best_length,best_path=float("inf"),[]
    root=MCTNode([],'root',0)
    refer_length=2*math.pi
    iteration_num=0
    while iteration_num<iteration_max:
        now=root
        line=[now]
        #selection
        while True:
            if now.children==[]:
                break
            list_UCB=[child.UCB for child in now.children]
            max_UCB=max(list_UCB)
            L=[child for child in now.children if child.UCB==max_UCB]
            now=random.choice(L)
            line.append(now)
        
        #expansion
        n=len(Lxy)
        if len(now.Path)<n:
            L_dist=[[dis[now.Path[-1]][i],i] for i in set(range(n))-set(now.Path)]
            L_dist.sort()
            for item in L_dist[:int(n/2)]:
                new=MCTNode(now.Path,now,item[1])
                now.children.append(new)
        
        #simulation
            for new in now.children:
                path_new=RandomPath(dis,new.Path)
                leng_new=computeLength(dis,path_new)
                if leng_new<best_length:
                    best_length=leng_new
                    best_path=list(path_new)
                new.Reward+=refer_length/leng_new
                new.Na+=1
                nt+=1
                new.updateUCB(nt)
                
        #backpropagation
                for pre in line:
                    pre.Reward+=refer_length/leng_new
                    pre.Na+=1
                    pre.updateUCB(nt)
        else:
            now.UCB=float('inf')
            
        if iteration_num%100==0:
            print(iteration_num,best_length)
            
        iteration_num+=1
        
    return (best_length,best_path)

Lxy=generatePointsOnCircle(10)
dis=computeDistance(Lxy)
res=TSP_MCTS(dis,Lxy,5000)
print(res)  
        
        
        
    
    
    
    
        
        
        
    
    
    
    
    


