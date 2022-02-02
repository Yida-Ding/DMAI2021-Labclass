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
        
    def visState(self,data):
        my_cmap=matplotlib.colors.LinearSegmentedColormap.from_list('my_camp',['white','grey','green'],3)
        self.ax.imshow(data,cmap=my_cmap)
            
fig,axes=plt.subplots(2,3,figsize=(20,10))
plt.tight_layout()
sizeL=[10,15,20,25,30,35]
seedL=[12,9,3,6,6,6]

for i,ax in enumerate(axes.flat):
    mg=MazeGenerator(sizeL[i],seedL[i])
    initData=mg.getInitData()
    goalData=mg.getGoalData()
    
    mv=MazeVisualizer(ax,sizeL[i])
    mv.visState(initData)
#    mv.visState(goalData)
    