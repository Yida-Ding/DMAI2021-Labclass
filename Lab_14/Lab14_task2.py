import random
import numpy as np


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
        plt.ylim(-0.5,1.5)
        plt.xlim(-0.5,1.5)
        
    def predict(self,xs):
        s=self.f(self.w,self.bias,xs)
        g=self.actf(s)
        return g
    
class NN:
    def __init__(self):
        self.input_layer=[perceptron("step") for i in range(2)]
        self.output_layer=perceptron("step")
        
    def forward_propagation_by_hand(self,data):
        p1=self.input_layer[0] #Nand
        p1.w=[-1,-1]
        p1.bias=1.5
        
        p2=self.input_layer[1] #Or
        p2.w=[1,1]
        p2.bias=-0.5
        
        p3=self.output_layer #And
        p3.w=[1,1]
        p3.bias=-1.5
        
        x11=p1.predict(data[:-1])
        x12=p2.predict(data[:-1])
        prediction=p3.predict([x11,x12])
        print('Predict:',prediction,'Actual:',data[-1])
        
        #Note: You can also automatically train the above three sets of weights using And/Or/Nand data.
            
nn=NN()
Xor=[(1,0,1),(0,1,1),(0,0,0),(1,1,0)]# xor
for data in Xor:
    nn.forward_propagation_by_hand(data)
