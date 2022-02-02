import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(1)
def generate(n):
    points=[[random.uniform(0,1),random.uniform(0,1)] for i in range(n)]
    up=[point+[1] for point in points if (point[0]*1+point[1]*1-0.9)>=0]
    points=[[random.uniform(0,1),random.uniform(0,1)] for i in range(n)]
    down=[point+[0] for point in points if (point[0]*1+point[1]*1-1.1)<=0]
    re=up+down
    random.shuffle(re)
    return re

class perceptron:
    def __init__(self,actf_mode='sigmoid'):
        self.actf_mode=actf_mode

    def actf(self,s):
        if self.actf_mode=='step':
            return int(s>=0)
        elif self.actf_mode=='sign':
            return -1+2*int(s>=0)
        elif self.actf_mode=='sigmoid':
            return 1/(1+np.e**(-1*s))
        
    def f(self,W,bias,X):
        return np.dot(np.array(W),np.array(X))+bias
    
    def train(self,train_data,alpha=0.1,iteration=100):
        self.n_input=len(train_data[0])-1
        self.w=[0,0]
        self.bias=0
        l=len(train_data)
        delta_ws=[],[]
        for t in range(iteration):
            delta_w=[0 for i in range(len(self.w))]
            delta_bias=0
            for xs_y in train_data:
                y=xs_y[-1]
                xs=xs_y[:-1]
                s=self.f(self.w,self.bias,xs)
                g=self.actf(s)
                for i in range(len(self.w)):
                    delta_w[i]+=(y-g)*g*(1-g)*xs[i]
                delta_bias+=(y-g)*g*(1-g)  
                
            print("iteration:",t)
            self.w=[self.w[i]+2*alpha*delta_w[i] for i in range(len(self.w))]
            self.bias+=2*alpha*delta_bias
            
    def test(self,test_data):
        l=len(test_data)
        print('-----------------testing-------------')
        for i in range(len(test_data)):
            xs=test_data[i%l][:self.n_input]
            y=test_data[i%l][self.n_input]
            s=self.f(self.w,self.bias,xs)
            g=self.actf(s)
            print("Predicted:",g,"Actual:",test_data[i][-1])
        self.vis(test_data,self.w)
        print("Weight:",self.w,"Bias:",self.bias)
        
    def vis(self,data,w):
        fig,ax=plt.subplots(1,1)
        x1s=[i[0] for i in data if i[2]==1]
        x2s=[i[1] for i in data if i[2]==1]
        plt.plot(x1s,x2s,"ro")
        x1s=[i[0] for i in data if i[2]==0]
        x2s=[i[1] for i in data if i[2]==0]
        plt.plot(x1s,x2s,"go")
        sx,sy=[0,1],[-1*self.bias/w[1],-1*(self.bias+w[0])/w[1]]
        plt.plot(sx,sy,"r-")
        plt.ylim(0,1)
        plt.xlim(0,1)
        
train_data=generate(2000)
test_data=generate(200)

p=perceptron('sigmoid')
p.train(train_data,alpha=0.1,iteration=500)
p.test(test_data)
