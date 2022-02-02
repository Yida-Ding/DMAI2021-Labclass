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
