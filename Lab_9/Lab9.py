import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from lxml import etree 
from haversine import haversine


def get_attribute_set(F):
    att_set=set()
    for (left,right) in F:
        att_set=att_set.union(left)
        att_set=att_set.union(right)
    return att_set
    
def get_subsets(S):
    S=sorted(list(S))
    if len(S)==1:
        return [S]
    else:
        subs=[]
        for i in range(len(S)):
            subsub=get_subsets(S[i+1:])
            subs.append([S[i]])
            for j in subsub:
                subs.append([S[i]]+j)
        return subs

def Reflexity(F,att_set):
    F_cur=F.copy()
    for X in get_subsets(att_set):
        for Y in get_subsets(X):
            F_cur.append((set(X),set(Y)))
    return F_cur

def Augmentation(F_cur,att_set):
    change=False
    for (left,right) in F_cur.copy():
        for W in att_set:
            if (left|{W},right|{W}) not in F_cur:
                F_cur.append((left|{W},right|{W}))
                change=True
    return F_cur,change

def Transitivity(F_cur):
    change=False
    for (left1,right1) in F_cur.copy():
        for (left2,right2) in F_cur.copy():
            if right1==left2:
                if (left1,right2) not in F_cur:
                    F_cur.append((left1,right2))
                    change=True  
    return F_cur,change
    
def computeClosure(F):
    att_set=get_attribute_set(F)
    F_cur=Reflexity(F,att_set)
    print('Reflexity')
    change=True
    while change:
        F_cur,aug_change=Augmentation(F_cur,att_set)        
        if aug_change:
            print('Augmentation')

        F_cur,tran_change=Transitivity(F_cur)        
        if tran_change:
            print('Transitivity')
        change=(aug_change or tran_change)
    return F_cur

F=[({'A'},{'B'}),
   ({'B'},{'C'}),
   ({'C'},{'D'}),
   ({'G','D'},{'H'})]
F_plus=computeClosure(F)
print(len(F_plus))

tree=etree.parse(r'DMAI_HW_Data/cycle.xml')
tree2=etree.parse(r'DMAI_HW_Data/books_collection.xml')

def XML_CSV():
    path="/catalog/book"
    nameL=["author","title","genre","price","publish_date","description"]
    
    idL=[e.attrib['id'] for e in tree2.xpath(path)]
    dataDict={"id":idL}
    for i in range(len(nameL)):
        dataL=[e.text for e in tree2.xpath(path+"/"+nameL[i])]
        dataDict[nameL[i]]=dataL
       
    pd.DataFrame(dataDict).to_csv("DMAI_HW_Data/book_collection.csv",index=None)
#XML_CSV()    

def Visualization():
    LD_Lat,LD_Lon=51.5,0.183333
    p1="/stations/station/long"
    p2="/stations/station/lat"
    p3="/stations/station/nbBikes"
    Lon=[float(x.text) for x in tree.xpath(p1)]
    Lat=[float(x.text) for x in tree.xpath(p2)]
    Nbi=[int(x.text) for x in tree.xpath(p3)]
    Dis=[]
    for i in range(len(Lon)):
        dis=haversine((LD_Lat,LD_Lon),(Lon[i],Lat[i]))
        Dis.append(dis)
    
    df=pd.DataFrame({"nbBikes":Nbi,"distance":Dis})
    sns.pairplot(df,kind="reg")
    sns.set(style="ticks",color_codes=True)
Visualization()





