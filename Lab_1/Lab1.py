import networkx as nx

G=nx.Graph()
G.add_edge('A','B',weight=10)
G.add_edge('A','C',weight=3)
G.add_edge('B','C',weight=1)
G.add_edge('C','B',weight=4)
G.add_edge('B','D',weight=2)
G.add_edge('C','D',weight=8)
G.add_edge('C','E',weight=2)
G.add_edge('D','E',weight=7)
G.add_edge('E','D',weight=9)

def Dijk_dis(s):
    dis={i:float("inf") for i in G.nodes}
    dis[s]=0
    Q=set(G.nodes)
    while len(Q)>0:
        u=min([[i,dis[i]] for i in Q],key=lambda xx:xx[1])[0]
        Q.remove(u)
        for v in list(G.neighbors(u)):
            if dis[v]>dis[u]+G.edges[u,v]["weight"]:
                dis[v]=dis[u]+G.edges[u,v]["weight"]
    return dis

def getPaths(n,parD):
    if parD[n]==None:
        return []
    else:
        par=parD[n]
        return getPaths(par,parD)+[par]

def Dijk_path(s):
    parD={n:None for n in G.nodes}
    
    dis={i:float("inf") for i in G.nodes}
    dis[s]=0
    Q=set(G.nodes)
    while len(Q)>0:
        u=min([[i,dis[i]] for i in Q],key=lambda xx:xx[1])[0]
        Q.remove(u)
        for v in list(G.neighbors(u)):
            if dis[v]>dis[u]+G.edges[u,v]["weight"]:
                dis[v]=dis[u]+G.edges[u,v]["weight"]
                parD[v]=u
    
    pathD={}
    for n in G.nodes:
        path=getPaths(n,parD)+[n]
        print(s,'->',n,'=',path)
        pathD[n]=path
    return pathD

#print(Dijk_path("A"))

G=nx.Graph()
G.add_edge('A','B',weight=2)
G.add_edge('A','D',weight=8)
G.add_edge('A','E',weight=14)
G.add_edge('D','E',weight=21)
G.add_edge('B','E',weight=25)
G.add_edge('B','C',weight=19)
G.add_edge('E','C',weight=17)
G.add_edge('E','F',weight=13)
G.add_edge('C','F',weight=5)
G.add_edge('C','G',weight=9)
G.add_edge('F','G',weight=1)

#Kruskal 
def Kruskal():
    res=[]
    S=[{v} for v in G.nodes]
    L=sorted(G.edges.data('weight'),key=lambda xx:xx[2])
    for edge in L:
        
        findDict={e:sind for sind,s in enumerate(S) for e in s}
        sind1,sind2=findDict[edge[0]],findDict[edge[1]]
        if sind1!=sind2:
            res.append((edge[0],edge[1]))
            if sind1>sind2:
                sind1,sind2=sind2,sind1
            set1=S.pop(sind1)
            set2=S.pop(sind2-1)            
            S.append(set1|set2)
    return res

print(Kruskal())



