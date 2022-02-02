import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Board:
    def __init__(self,length,width,t,nl,seed):
        self.length=length
        self.width=width
        self.t=t
        self.nl=nl
        self.lineXpos=np.arange(0,length+1,t)
        random.seed(seed)
        
    def generateNeedles(self,N):
        posL=[]
        for i in range(N):
            xc=random.uniform(0,self.length)
            yc=random.uniform(0,self.width)
            theta=random.uniform(0,np.pi)
            posL.append((xc,yc,theta))
        return posL
    
    def visBoard(self,ax):
        ax.set_xticks(self.lineXpos)
        ax.set_yticks([self.width])
        ax.set_xlim(0,self.length)
        ax.set_ylim(0,self.width)
        ax.grid(alpha=0.8,color='black')
    
    def visNeedles(self,posL,ax):
        for (xc,yc,theta) in posL:
            dx=abs(0.5*self.nl*np.cos(theta))
            dy=abs(0.5*self.nl*np.sin(theta))
            X=np.linspace(xc-dx,xc+dx,100)
            if theta<=np.pi/2:
                Y=np.linspace(yc-dy,yc+dy,100)
            else:
                Y=np.linspace(yc+dy,yc-dy,100)
            ax.plot(X,Y,alpha=0.6,lw=3)
            
    def getCrossPos(self,posL):
        crossPosL=[]
        for (xc,yc,theta) in posL:
            dx=abs(0.5*self.nl*np.cos(theta))
            for xl in self.lineXpos:
                if xc-dx<=xl<=xc+dx:
                    dyl=np.tan(theta)*(xl-xc)
                    crossPosL.append((xl,yc+dyl))
        return crossPosL
    
    def estimatePi(self,posL,crossPosL):
        P=len(crossPosL)/len(posL)
        pi=2*self.nl/(P*self.t)
        return pi
        
    def visCross(self,crossPosL,ax,pi):
        X,Y=list(zip(*crossPosL))
        ax.scatter(X,Y,color='red')
        ax.set_title("Pi estimation is %.5f"%pi,fontsize=20)
        
        
B=Board(100,50,10,5,5)
posL=B.generateNeedles(500)
crossPosL=B.getCrossPos(posL)

fig,ax=plt.subplots(1,1,figsize=(10,6))
B.visBoard(ax)
B.visNeedles(posL,ax)
pi=B.estimatePi(posL,crossPosL) 
B.visCross(crossPosL,ax,pi)
plt.savefig("BuffonNeedle.pdf")
        
    
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    


