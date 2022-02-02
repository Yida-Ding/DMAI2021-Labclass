import time
import copy
import heapq as hq
import random 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class MazeGenerator:
    def __init__(self,a,seed):
        self.a=a
        random.seed(seed)
        self.data=[[0 for i in range(a)] for j in range(a)]
        self.src,self.dest=(a-2,1),(1,a-2)
        self.setBlockPoints()
                
    def setBlockPoints(self):
        boundary={(i,j) for i in [0,self.a-1] for j in range(self.a)}|{(i,j) for j in [0,self.a-1] for i in range(self.a)}
        choice={(i,j) for i in range(self.a) for j in range(self.a)}-boundary-{self.src,self.dest}
        select=set(random.sample(choice,k=len(choice)//4))
        for (i,j) in boundary|select:
            self.data[i][j]=1
    
    def getInitData(self):
        initData=copy.deepcopy(self.data)
        initData[self.src[0]][self.src[1]]=2
        return initData
    
    def getGoalData(self):
        goalData=copy.deepcopy(self.data)
        goalData[self.dest[0]][self.dest[1]]=2
        return goalData        
        
class MazeVisualizer:
    def __init__(self,ax,a):
        self.ax=ax
        self.ax.set_title("%dx%d"%(a,a))
        
    def visState(self,s):
        my_cmap=matplotlib.colors.LinearSegmentedColormap.from_list('my_camp',['white','grey','green'],3)
        self.ax.imshow(s.data,cmap=my_cmap)
        
    def visPath(self,path,s):
        r,c=s.r,s.c
        nameL=["Up","Down","Left","Right"]
        actionL=["r-1,c","r+1,c","r,c-1","r,c+1"]
        for name in path:
            r,c=eval(actionL[nameL.index(name)])
            s.data[r][c]=2
        my_cmap=matplotlib.colors.LinearSegmentedColormap.from_list('my_camp',['white','grey','lightgreen'],3)
        self.ax.imshow(s.data,cmap=my_cmap)
        
class MazeState:
    def __init__(self,data):
        self.data=data
        self.r,self.c=self.getLoc(2)
        
    def getLoc(self,key):
        for row in self.data:
            if key in row:
                return (self.data.index(row),row.index(key))

    def isGoal(self,gs):
        return self.data==gs.data

    def getLegalActions(self):
        L=[]
        if self.data[self.r-1][self.c]==0:
            L+=["Up"]
        if self.data[self.r+1][self.c]==0:
            L+=["Down"]
        if self.data[self.r][self.c-1]==0:
            L+=["Left"]
        if self.data[self.r][self.c+1]==0:
            L+=["Right"]
        return L

    def Manhattan(self,gs):
        return abs(self.r-gs.r)+abs(self.c-gs.c)
    
    def Euclidean(self,gs):
        return np.sqrt((self.r-gs.r)**2+(self.c-gs.c)**2)

def step(s,a):
    nData=copy.deepcopy(s.data)
    print(nData)
    if a=="Up":
        nData[s.r-1][s.c],nData[s.r][s.c]=nData[s.r][s.c],nData[s.r-1][s.c]
    elif a=="Down":
        nData[s.r+1][s.c],nData[s.r][s.c]=nData[s.r][s.c],nData[s.r+1][s.c]
    elif a=="Left":
        nData[s.r][s.c-1],nData[s.r][s.c]=nData[s.r][s.c],nData[s.r][s.c-1]
    elif a=="Right":
        nData[s.r][s.c+1],nData[s.r][s.c]=nData[s.r][s.c],nData[s.r][s.c+1]
    return MazeState(nData)
                    
def BFS(s,gs,nflag=False):
    todo=[(s,[],[s.data])]
    ncount=0
    while len(todo)>0:
        cur,path,seen=todo.pop(0)
        ncount+=1
        aL=cur.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                todo.append((n,path+[a],seen+[n.data]))
                if n.isGoal(gs):
                    return path+[a] if nflag==False else ncount

def DFS(s,gs,nflag=False):
    todo=[(s,[],[s.data])]
    ncount=0
    while len(todo)>0:
        cur,path,seen=todo.pop()
        ncount+=1
        aL=cur.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                todo.append((n,path+[a],seen+[n.data]))
                if n.isGoal(gs):
                    return path+[a] if nflag==False else ncount

def UCS(s,gs,nflag=False):
    Q=[]
    hq.heappush(Q,(0,id(s),s,[],[s.data]))
    ncount=0
    while len(Q)>0:
        cur,path,seen=hq.heappop(Q)[2:]
        ncount+=1
        aL=cur.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                hq.heappush(Q,(len(path),id(n),n,path+[a],seen+[n.data]))
                if n.isGoal(gs):
                    return path+[a] if nflag==False else ncount

def GBFS(s,gs,nflag=False):
    Q=[]
    hq.heappush(Q,(s.Manhattan(gs),id(s),s,[],[s.data]))
    ncount=0
    while len(Q)>0:
        cur,path,seen=hq.heappop(Q)[2:]
        ncount+=1
        aL=cur.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                hq.heappush(Q,(n.Manhattan(gs),id(n),n,path+[a],seen+[n.data]))
                if n.isGoal(gs):
                    return path+[a] if nflag==False else ncount

def ASTAR(s,gs,nflag=False):
    Q=[]
    hq.heappush(Q,(0+s.Manhattan(gs),id(s),s,[],[s.data]))
    ncount=0
    while len(Q)>0:
        cur,path,seen=hq.heappop(Q)[2:]
        ncount+=1
        aL=cur.getLegalActions()
        # random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                hq.heappush(Q,(len(path)+n.Manhattan(gs),id(n),n,path+[a],seen+[n.data]))
                if n.isGoal(gs):
                    return path+[a] if nflag==False else ncount

def testNodeTime(sizeL,seedL,mL):
    infodict={}
    for i in range(len(sizeL)):
        mg=MazeGenerator(sizeL[i],seedL[i])
        s=MazeState(mg.getInitData())
        gs=MazeState(mg.getGoalData())
        for m in mL:
            t1=time.time()
            node=eval(m)(s,gs,True)
            t2=time.time()
            infodict[(sizeL[i],m)]=[node,t2-t1]
            print((sizeL[i],m),[node,t2-t1])
    return infodict

fig,axes=plt.subplots(2,3,figsize=(20,10))
mg=MazeGenerator(15,9)
s=MazeState(mg.getInitData())
gs=MazeState(mg.getGoalData())
path=ASTAR(s,gs)

mv=MazeVisualizer(axes[0][0],15)
mv.visPath(path,s)


# fig,axes=plt.subplots(2,3,figsize=(20,10))
# plt.tight_layout()
# sizeL=[10,15,20,25,30,35]
# seedL=[12,9,3,6,6,6]

# for i,ax in enumerate(axes.flat):
#     mg=MazeGenerator(sizeL[i],seedL[i])
#     s=MazeState(mg.getInitData())
#     gs=MazeState(mg.getGoalData())
    
#     path=ASTAR(s,gs)
    # print(path)
    
    # mv=MazeVisualizer(ax,sizeL[i])
    # mv.visPath(path,s)
    
#sizeL=[10,15,20,25,30,35]
#seedL=[12,9,3,6,6,6]
#mL=["BFS","UCS","GBFS","ASTAR"]
#testNodeTime(sizeL,seedL,mL)
        
        

    













