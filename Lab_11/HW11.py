import time
import numpy as np
import copy
import random
import heapq as hq
import matplotlib.pyplot as plt
import matplotlib

class State:
    def __init__(self,data,N):
        self.data=data
        self.N=N
        self.A=int(np.sqrt(N+1))
        self.num2pos={self.data[i][j]:(i,j) for i in range(self.A) for j in range(self.A)}
    
    def isGoal(self,gs):
        return self.data==gs.data
    
    def __repr__(self):
        res=''
        for row in self.data:
            row=[str(i) for i in row]
            res+=("|"+"\t".join(row)+"|\n")
        return res
        
    def getLegalActions(self):
        r,c=self.num2pos[0]
        conditionL=["r!=0","r!=self.A-1","c!=0","c!=self.A-1"]
        actionL=["Up","Down","Left","Right"]
        res=[]
        for i in range(len(actionL)):
            if eval(conditionL[i]):
                res.append(actionL[i])
        return res
        
    def getMht(self,gs):
        dis=0
        for n in range(1,self.N+1):
            r1,c1=self.num2pos[n]
            r2,c2=gs.num2pos[n]
            dis=dis+abs(r1-r2)+abs(c1-c2)
        return dis
    

def getGoalState(N):
    A=int(np.sqrt(N+1))
    L=[i for i in range(1,N+1)]
    goalData=[L[j*A:(j+1)*A] for j in range(A)]
    goalData[-1].append(0)
    return State(goalData,N)

def step(s,a):
    r,c=s.num2pos[0]
    nsData=[list(s.data[i]) for i in range(s.A)]
    if a=="Up":
        nsData[r][c],nsData[r-1][c]=nsData[r-1][c],nsData[r][c]
    elif a=="Down":
        nsData[r][c],nsData[r+1][c]=nsData[r+1][c],nsData[r][c]
    elif a=="Left":
        nsData[r][c],nsData[r][c-1]=nsData[r][c-1],nsData[r][c]
    elif a=="Right":
        nsData[r][c],nsData[r][c+1]=nsData[r][c+1],nsData[r][c]
    return State(nsData,s.N)

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
                
def ASTAR(s,gs,nflag=False):
    Q=[]
    hq.heappush(Q,(0+s.getMht(gs),id(s),s,[],[s.data]))
    ncount=0
    while len(Q)>0:
        cur,path,seen=hq.heappop(Q)[2:]
        ncount+=1
        aL=cur.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                hq.heappush(Q,(len(path)+n.getMht(gs),id(n),n,path+[a],seen+[n.data]))
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
    hq.heappush(Q,(s.getMht(gs),id(s),s,[],[s.data]))
    ncount=0
    while len(Q)>0:
        cur,path,seen=hq.heappop(Q)[2:]
        ncount+=1
        aL=cur.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            n=step(cur,a)
            if n.data not in seen:
                hq.heappush(Q,(n.getMht(gs),id(n),n,path+[a],seen+[n.data]))
                if n.isGoal(gs):
                    return path+[a] if nflag==False else ncount


def getInitState(N,k,gs):
    ns=State([list(gs.data[i]) for i in range(gs.A)],gs.N)
    seen=[ns.data]
    for i in range(k):
        aL=ns.getLegalActions()
        random.shuffle(aL)
        for a in aL:
            if step(ns,a).data not in seen:
                ns=step(ns,a)
                seen.append(ns.data)
                break
    return ns

def testNodeTime(NL,kL,mL):
    Nkm2nodetime={}
    for N in NL:
        gs=getGoalState(N)
        for k in kL:
            inits=getInitState(N,k,gs)
            for m in mL:
                t1=time.time()
                node=eval(m)(inits,gs,True)
                t2=time.time()
                Nkm2nodetime[(N,k,m)]=[node,t2-t1]
                print((N,k,m),[node,t2-t1])
    return Nkm2nodetime

def visData(Nkm2nodetime,vtype):
    fig,axes=plt.subplots(2,2,figsize=(20,10))
    for i,ax in enumerate(axes.flat):
        N=NL[i]
        for m in mL:
            ys=[]
            for k in kL:
                ys.append(Nkm2nodetime[(N,k,m)][vtype])
            ax.plot(kL,ys,label=m)
        ax.set_title("N=%d"%N)  
        ax.legend()
        ax.set_xlabel("k")
        if vtype==0:
            ax.set_ylabel("#ExpandedNodes")
            plt.savefig("ExpandedNodes.pdf")
        else:
            ax.set_ylabel("Runtime")
            plt.savefig("Runtime.pdf")

                
#N=8
#gs=getGoalState(N)
#s=State([[1,2,3],[4,8,0],[7,6,5]],N)
#s2=State([[1,2,3],[4,8,5],[7,6,0]],N)
#
#inits=getInitState(N,5,gs)
#print(inits)
#res=BFS(inits,gs)
#print(res)

random.seed(0)
NL=[8,15,24,35]  
kL=[3,6,9,12,15]
mL=["BFS","UCS","GBFS","ASTAR"]
Nkm2nodetime=testNodeTime(NL,kL,mL)
visData(Nkm2nodetime,0)
    
        






