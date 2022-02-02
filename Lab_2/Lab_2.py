import os
import networkx as nx

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
#For O(ElogE), see another code file
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
        
        if len(S)==1:
            break
    return res

print(Kruskal())

class Knapsack:
    def __init__(self,filename):
        f=open("DMAI_Lab2_data/%s.txt"%filename,"r")
        data=f.readlines()
        self.itemD={}
        for i,row in enumerate(data):
            row=row.split(" ") 
            if i==0:
                self.Nitem=int(row[0])
                self.maxWgt=int(row[1])
                self.L=[i for i in range(1,self.Nitem+1)]
            else:
                self.itemD[i]=[int(row[0]),int(row[1])]
                
    def greedy(self):
        L=self.L.copy()
        for i in range(1,self.Nitem+1):
            for j in range(i+1,self.Nitem+1):
                if self.itemD[i][0]/self.itemD[i][1]<self.itemD[j][0]/self.itemD[j][1]:
                    L[i-1],L[j-1]=L[j-1],L[i-1]
        curWgt=0
        curVal=0
        selItem=[]
        while len(L)!=0:
            i=L.pop(0)
            if curWgt+self.itemD[i][1]<=self.maxWgt: 
                selItem.append(i)
                curVal+=self.itemD[i][0]
                curWgt+=self.itemD[i][1]
            else:
                break
        return selItem,curVal
        
    def full_enum(self,i,curset,curWgt):
        if i>len(self.L):
            return []
        elif i==len(self.L):
            if curWgt<=self.maxWgt:
                return [curset]
            else:
                return []
        else:
            res=[]
            if curWgt<=self.maxWgt:
                res.append(curset)
            res+=self.full_enum(i+1,curset+[self.L[i]],curWgt+self.itemD[self.L[i]][1])
            res+=self.full_enum(i+1,curset,curWgt)
            return res
    
    def get_enum_best(self,resL):
        maxVal=0
        bestChoice=None
        for res in resL:
            val=sum([self.itemD[item][0] for item in res])
            if val>maxVal:
                maxVal=val
                bestChoice=res
        return bestChoice,maxVal
                
ks=Knapsack("ks_4")
#greedy
print(ks.greedy())
#full enumeration
resL=ks.full_enum(0,[],0)
print(resL)
print(ks.get_enum_best(resL))



class Toy:
    def __init__(self,name):
        f=open("DMAI_Lab2_data/%s.csv"%name,"r")
        self.M=f.readlines()[1:]
        f.close()

    def selection(self,n):
        res=[]
        for L in self.M:
            score=int(L.split(",")[2])
            if score>n:
               res.append(L.split(",")[0])
        return res
    
    def AverageScore():
        res=[]
        for L in self.M:
            score=int(L.split(",")[2])
            res.append(score)
        return sum(res)/len(res)
        
    def GPA(self):
        d={}
        for L in self.M:
            score=int(L.split(",")[2])
            if score>=90:
                gpa=4
            elif score>=80:
                gpa=3
            elif score>=60:
                gpa=1
            else:
                gpa=0
            d[L.split(",")[0]]=gpa
        return d

#T=Toy("toy")
#print(T.selection(60))

class Airport:
    def __init__(self,name):
        self.f=open("DMAI_Lab2_data/%s.csv"%name,"r",encoding="UTF-8")
        self.M=self.f.readlines()[1:]
        self.f.close()
    
    def SelectedColumns(self):
        res=[]
        for L in self.M:
            Item=L.split(",")
            rowselected=[Item[3],Item[8],Item[10]]
            res.append(rowselected)
        f.close()
        return res

    def SelectChineseAirports(self):
        res=[]
        for L in self.M:
            Item=L.split(",")
            if Item[8]=='"CN"':
                res.append(L[:-1]) #remove \n
        return res
    
    def Statistic(self):
        Items=self.M[0][:-1].split(",")
        DList=[{} for i in range(len(Items))]
        for L in self.M[1:]:
            for i in range(len(Items)):
                if L.split(",")[i] not in DList[i]:
                    DList[i][L.split(",")[i]]=1
                else:
                    pass
        Num=[len(d) for d in DList]
        res={Items[i]:Num[i] for i in range(len(Items))}
        return res

    def Split(self):
        if not os.path.exists('DMAI_Lab2_data/Continent'):
            os.makedirs("DMAI_Lab2_data/Continent")
        Cont=[]
        for L in self.M:
            Cont.append(L.split(",")[7])
        for name in list(set(Cont)):
            LinesL=[]
            for L in self.M:
                if L.split(",")[7]==name:
                    LinesL.append(L)
            f=open("DMAI_Lab2_data/Continent/%s.csv"%name[1:-1],"w",encoding="UTF-8")
            f.writelines(LinesL)
            f.close()
        return 

    def Sort(self):
        temp=[]
        for L in self.M:
            elev=L.split(",")[6]
            if elev=="":
                continue
            else:
                Line=L.split(",")
                Line[6]=int(elev)
                temp.append(Line)
        sortedlist=sorted(temp,key=lambda xx:xx[6])
        LineL=[]
        for Line in sortedlist:
            Line[6]=str(Line[6])
            LineL.append(",".join(Line))            
        f=open("DMAI_Lab2_data/airports-sorted.csv","w",encoding="UTF-8")
        f.writelines(LineL)
        f.close()

#A=Airport("airports")
#res=A.Split()
#print(res)





