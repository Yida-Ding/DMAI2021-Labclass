import copy


class State:
    def __init__(self,NearFar,Boat):
        self.NearFar=copy.deepcopy(NearFar)
        self.Boat=Boat
        
    def isGoal(self):
        return self.NearFar[0]==[0,0]
    
    def getLegalActions(self):
        MoveBoat=["NearToFar","FarToNear"]
        Possible=[(0,2),(0,1),(1,1),(1,0),(2,0)]
        L=[]
        if self.NearFar[self.Boat]!=[0,0]:
            for ps in Possible:
                if (self.NearFar[self.Boat][0]>=ps[0] and self.NearFar[self.Boat][1]>=ps[1]) \
                and (self.NearFar[self.Boat][0]-ps[0]>=self.NearFar[self.Boat][1]-ps[1] or self.NearFar[self.Boat][0]-ps[0]==0) \
                and (self.NearFar[1-self.Boat][0]+ps[0]>=self.NearFar[1-self.Boat][1]+ps[1] or self.NearFar[1-self.Boat][0]+ps[0]==0):
                    L.append((ps[0],ps[1],MoveBoat[self.Boat]))
        return L
    
    def toString(self):
        return "Near:%d,%d,Far:%d,%d"%(self.NearFar[0][0],self.NearFar[0][1],self.NearFar[1][0],self.NearFar[1][1])

def step(s,a):
    n=State(s.NearFar,1-s.Boat)
    n.NearFar[s.Boat][0]-=a[0]
    n.NearFar[s.Boat][1]-=a[1]
    n.NearFar[1-s.Boat][0]+=a[0]
    n.NearFar[1-s.Boat][1]+=a[1]
    return n

def BFS(s):
    todo=[(s,[],[s.NearFar+[s.Boat]])]
    while len(todo)>0:
        cur,path,already=todo.pop(0)
        for a in cur.getLegalActions():
            n=step(cur,a)
            if n.NearFar+[n.Boat] not in already:
                todo.append((n,path+[a],already+[n.NearFar+[n.Boat]]))
                if n.isGoal():
                    return path+[a]
                    
def DFS(s,path,already):
    if s.isGoal():
        return path,already
    else:
        for a in s.getLegalActions():
            n=step(s,a)
            if n.NearFar+[n.Boat] not in already:
                IF=DFS(n,path+[a],already+[n.NearFar+[n.Boat]])
                if IF!=None:
                    return IF

s=State([[3,3],[0,0]],0)
Path1,already=DFS(s,[],[s.NearFar+[s.Boat]])
Path2=BFS(s)
print(Path1)
print(Path2)




