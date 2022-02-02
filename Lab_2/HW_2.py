import string

class Book:
    def __init__(self,name):
        self.name=name
        f=open("DMAI_HW2_data/%s.txt"%self.name,"r")
        self.M=f.readlines()[1:]
        f.close()

    def getOccurence(self):
        occurD={l:0 for l in string.ascii_lowercase+string.ascii_uppercase}
        for stri in self.M:
            for l in stri:
                if l in occurD.keys():
                    occurD[l]+=1            
        return occurD        
    
    def write(self,occurD):
        string=""
        for k,v in occurD.items():
            string+=str(k)+":"+str(v)+'\n'
        f=open("DMAI_HW2_data/%s_res.txt"%self.name,"w")
        f.writelines(string)
        f.close()
        
B=Book("Jane_Eyre")
occurD=B.getOccurence()
B.write(occurD)




def test(i,curset,L,k):
    if i>=len(L):
        return []
    else:
        res=[]
        if sum(curset)<=k:
            res.append(curset)
        res+=test(i+1,curset+[L[i]],L,k)
        res+=test(i+1,curset,L,k)
        return res
    
    

    
    