import tflearn
import tensorflow as tf
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

def preprocess(df):
    trainX=np.array(df[["pclass","sex","age","sibsp","parch","fare"]])
    for i in range(len(trainX)):
        if trainX[i][1]=="female":
            trainX[i][1]=1.0
        else:
            trainX[i][1]=0.0
    return trainX

def TitanicTrain():
    df=pd.read_csv('titanic_dataset.csv')
    trainY=np.array([[i,1-i] for i in df.survived.tolist()])
    trainX=preprocess(df)

    tf.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(trainX[0])])
    net = tflearn.fully_connected(net, 32)
    net = tflearn.fully_connected(net, 32)
    net = tflearn.fully_connected(net, len(trainY[0]), activation='softmax')
    net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy',
                             learning_rate=0.001)
    model = tflearn.DNN(net, tensorboard_verbose=3)
    model.fit(trainX, trainY, n_epoch=100, show_metric=True,batch_size=16)
    return model

def TitanicTest(model):
#    dicaprio = [3, 'Jack', 'male', 19, 0, 0, 'N/A', 5.0000]
#    winslet = [1, 'rose', 'female', 17, 1, 2, 'N/A', 100.0000]
    testX=np.array([[3,0, 19, 0, 0, 5.0000],[1,1, 17, 1, 2,100.0000]])
    pred = model.predict(testX)
    print("Jack Surviving Rate:", pred[0][0])
    print("Rose Surviving Rate:", pred[1][0])

model=TitanicTrain()
TitanicTest(model)