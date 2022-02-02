from lxml import etree 
import matplotlib.pyplot as plt
import pandas as pd
from haversine import haversine

tree=etree.parse(r'DMAI_HW_Data/cycle.xml')

def Bike(subtask):
    if subtask==2:
        p1="/stations/station"
        print(len(tree.xpath(p1)))
        p2="//name"
        nameL=[e.text for e in tree.xpath(p2)]
        print(nameL)
    
    elif subtask==3:  
        p1="/stations/station[(locked='false') and (nbBikes>40)]/id"
        p2="/stations/station[(locked='false') and (nbBikes>40)]/nbBikes"
        idL=[e.text for e in tree.xpath(p1)]
        nbL=[e.text for e in tree.xpath(p2)]
        print(idL,nbL)
    
    elif subtask==4:
        valL=["<=10",">10"]
        colL=["red","blue"]
        
        fig,ax=plt.subplots(figsize=(20,10))
        for i in range(len(valL)):
            p1="/stations/station[nbBikes%s]/long"%(valL[i])
            p2="/stations/station[nbBikes%s]/lat"%(valL[i])
            Lon=[float(e.text) for e in tree.xpath(p1)]
            Lat=[float(e.text) for e in tree.xpath(p2)]
            ax.scatter(Lon,Lat,color=colL[i],marker="o",label=valL[i])
        
        ax.legend()
        plt.savefig("DMAI_HW_Data/HW9.pdf")

Bike(4)
