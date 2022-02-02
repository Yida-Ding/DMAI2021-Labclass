import random
import matplotlib.pyplot as plt
import numpy as np

def generate(n):
    points=[[random.uniform(0,1),random.uniform(0,1)] for i in range(n)]
    up=[point+[1] for point in points if (point[0]*2+point[1]*3-2)>=0]
    down=[point+[0] for point in points if point[0]*2+point[1]*3-2<0]
    res=up+down
    random.shuffle(res)
    return res

class perceptron:
    def __init__(self,actf_mode='step'):
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
        self.w=[random.uniform(0,1) for i in range(self.n_input)]
        self.bias=random.uniform(0,1)
        l=len(train_data)
        for t in range(iteration):
            xs=train_data[t%l][:self.n_input]
            y=train_data[t%l][self.n_input]
            s=self.f(self.w,self.bias,xs)
            g=self.actf(s)
            self.w=[self.w[i]+alpha*(y-g)*xs[i] for i in range(self.n_input)]
            self.bias=self.bias+alpha*(y-g)
            print('iteration',t,'error',abs(y-g))
    
    def test(self,test_data):
        l=len(test_data)
        print('-------------testing-------------')
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
        plt.plot(x1s,x2s,"bo")
        x1s=[i[0] for i in data if i[2]==0]
        x2s=[i[1] for i in data if i[2]==0]
        plt.plot(x1s,x2s,"go")
        sx,sy=[0,1],[-1*self.bias/w[1],-1*(self.bias+w[0])/w[1]]
        plt.plot(sx,sy,"r-")
        plt.ylim(0,1)
        plt.xlim(0,1)
        
random.seed(1)
train_data=generate(5000)
test_data=generate(50)
p=perceptron("step")
p.train(train_data,alpha=0.1,iteration=3000)
p.test(test_data)
