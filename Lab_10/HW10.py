
class WJState:
    def __init__(self,xytuple):
        self.x,self.y=xytuple
    
    def isGoal(self):
        return self.y==1
    
    def getLegalActions(self):
        L=[]
        if self.x>0:
            L.append("EmptyX")
        if self.y>0:
            L.append("EmptyY")
        if self.x>0 and self.x+self.y<=2:
            L.append("XtoYall")
        if self.x>0 and self.x+self.y>2 and self.y<2:
            L.append("XtoYpart")
        if self.y>0 and self.x+self.y<=5:
            L.append("YtoXall")
        if self.y>0 and self.x+self.y>5 and self.x<5:
            L.append("YtoXpart")
        return L
    
    def __repr__(self):
        return "X=%d,Y=%d"%(self.x,self.y)
    
def step(s,a):
    actionL=["EmptyX","EmptyY","XtoYall","XtoYpart","YtoXall","YtoXpart"]
    stateL=[(0,s.y),(s.x,0),(0,s.x+s.y),(s.x+s.y-2,2),(s.x+s.y,0),(5,s.x+s.y-5)]
    return WJState(stateL[actionL.index(a)])
        
def BFS(s):
    todo=[(s,[],[(s.x,s.y)])]
    while len(todo)>0:
        cur,path,seen=todo.pop(0)
        for a in cur.getLegalActions():
            n=step(cur,a)
            if (n.x,n.y) not in seen:
                todo.append((n,path+[a],seen+[(n.x,n.y)]))
                if n.isGoal():
                    return path+[a],seen+[(n.x,n.y)]

def DFS1(s):
    todo=[(s,[],[(s.x,s.y)])]
    while len(todo)>0:
        cur,path,seen=todo.pop()
        for a in cur.getLegalActions():
            n=step(cur,a)
            if (n.x,n.y) not in seen:
                todo.append((n,path+[a],seen+[(n.x,n.y)]))
                if n.isGoal():
                    return path+[a],seen+[(n.x,n.y)]

def DFS2(s,path,seen):
    if s.isGoal():
        return path,seen
    else:
        for a in s.getLegalActions():
            n=step(s,a)
            if (n.x,n.y) not in seen:
                IF=DFS2(n,path+[a],seen+[(n.x,n.y)])
                if IF!=None:
                    return IF
                
s=WJState((5,0))
print(BFS(s))
print(DFS1(s))
print(DFS2(s,[],[(s.x,s.y)]))
    
    