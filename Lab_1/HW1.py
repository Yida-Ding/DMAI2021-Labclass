import networkx as nx

#HW
#Task1: get used to networkx basics

nodeL=['s','a','b','c','d','e','f','g']
edgeL=[('s','a'),('s','b'),('s','f'),('f','g'),('b','g'),('b','c'),('b','e'),('d','c'),('e','d'),('g','d')]

G=nx.Graph()
G.add_nodes_from(nodeL)
G.add_edges_from(edgeL)
G.nodes['s']['st']=0

#print(G.nodes())
#print(G.edges())
#print(G.degree('g'))
#print(list(G.neighbors('s')))
#print(G.nodes['s'])
#Task2 DFS

for n in G.nodes:
    G.nodes[n]["color"]=-1
    G.nodes[n]["st"]=None
    G.nodes[n]["et"]=None

def DFS(u,ct=0):
    G.nodes[u]["st"]=ct
    ct+=1
    G.nodes[u]["color"]=0
    for v in list(G.neighbors(u)):
        if G.nodes[v]["color"]==-1:
            ct=DFS(v,ct)
            ct+=1
    G.nodes[u]["et"]=ct
#    G.nodes[u]["color"]=1
    print(u,G.nodes[u]["st"],G.nodes[u]["et"])
    return ct

DFS('s')

for n in G.nodes:
    G.nodes[n]["stat"]=0
    
def BFS(s):
    G.nodes[s]["stat"]=1
    L=[[] for i in range(len(G.nodes))]
    L[0].append(s)
    for i in range(len(G.nodes)):
        for u in L[i]:
            for v in list(G.neighbors(u)):
                if G.nodes[v]["stat"]==0:
                    G.nodes[v]["stat"]=1
                    L[i+1].append(v)
    return L

print(BFS('s'))


