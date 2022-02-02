import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from haversine import haversine


#Task1(1)
def fun1():
    x=np.linspace(-np.pi,np.pi,101)
    y_sin=np.sin(x)
    y_cos=np.cos(x)
    
    fig,ax=plt.subplots(1,1,figsize=(6,4),dpi=100)
    ax.plot(x,y_cos,color='red')
    ax.plot(x,y_sin,color='green')
    plt.savefig("Figure1.png")


#Task1(2)
def fun2():
    x=np.linspace(-np.pi,np.pi,101)
    y_sin=np.sin(x)
    y_cos=np.cos(x)
    
    fig,ax=plt.subplots(1,1,figsize=(6,4),dpi=100)
    ax.plot(x,y_sin,color='red',linewidth=2.5,linestyle='dashed',label='sine')
    ax.plot(x,y_cos,color='blue',linewidth=2.5,label='cosine')
    ax.legend(loc='upper left')
    plt.savefig("Figure2.png")

#Task1(3)
def fun3():
    x=np.linspace(-np.pi,np.pi,101)
    y_sin=np.sin(x)
    y_cos=np.cos(x)
    
    fig,axes=plt.subplots(1,2,figsize=(6,3),dpi=100)
    axes[0].plot(x,y_sin,color='red',linewidth=2.5,linestyle='dashed',label='sine')
    axes[1].plot(x,y_cos,color='blue',linewidth=2.5,label='cosine')
    axes[0].legend(loc='upper left')
    axes[1].legend(loc='upper left')


#Task2
def Beijing_subway():
    df_link=pd.read_csv("DMAI_Lab4_data/subwaylinks.csv")
    df_node=pd.read_csv("DMAI_Lab4_data/subwaynodes.csv")
    fig,ax=plt.subplots(1,1,figsize=(20,10),dpi=100)
    Lon,Lat=116.344193,39.975848
    node2latlon={}
    node_dis=[]
    for row in df_node.itertuples():
        node2latlon[row.node]=(row.longitude,row.latitude)
        dis=haversine((row.latitude,row.longitude),(Lat,Lon))
        node_dis.append((row.node,dis))
    for row in df_link.itertuples():
        lon=[node2latlon[row.nodefrom][0],node2latlon[row.nodeto][0]]
        lat=[node2latlon[row.nodefrom][1],node2latlon[row.nodeto][1]]
        ax.plot(lon,lat,color="blue")
        ax.scatter(lon,lat,color="red",marker=".")
    ax.plot(Lon,Lat,"gx",markersize=20)
    
    ax.set_ylim(39.6,40.3)
    ax.set_xlim(116,116.8)
    node_dis_sorted=sorted(node_dis,key=lambda xx:xx[1])
    for i in range(3):
        lon=node2latlon[node_dis_sorted[i][0]][0]
        lat=node2latlon[node_dis_sorted[i][0]][1]
        ax.scatter(lon,lat,color="green",marker="o")
    plt.tight_layout()
    
#Beijing_subway()


#Task3(version1)
def Interval(L,n):
    for i in range(len(L)):
        if L[i]>n:
            return i
    return len(L)

def Coronavirus1():
    df_covid=pd.read_csv("DMAI_Lab4_data/coronavirus_China.csv")
    df_city=pd.read_csv("DMAI_Lab4_data/cities.csv")
    L_conf=[10,30,100,300,1000,3000,10000]
    L_dead=[1,3,10,30,100,300,1000]
    L_color=["green","lightgreen","yellow","gold","darkorange","red","darkred","purple"]
    color2confLabel={L_color[i]:"<"+str(L_conf[i]) for i in range(len(L_color)-1)}
    color2deadLabel={L_color[i]:"<"+str(L_dead[i]) for i in range(len(L_color)-1)}
    color2confLabel["purple"]=">="+str(L_conf[-1])
    color2deadLabel["purple"]=">="+str(L_dead[-1])

    dict_city={}
    for row in df_city.itertuples():
        dict_city[row.City]=(float(row.Lon[2:]),float(row.Lat[2:]))
    fig,axes=plt.subplots(1,2,figsize=(20,10),dpi=100)
    for row in df_covid.itertuples():
        city=row.Region
        conf=row.Total_confirm
        dead=row.Total_dead
        conf_ind=Interval(L_conf,conf)
        dead_ind=Interval(L_dead,dead)
        conf_color=L_color[conf_ind]
        dead_color=L_color[dead_ind]
        if city in dict_city:
            Lon=dict_city[city][0]
            Lat=dict_city[city][1]
            axes[0].plot(Lon,Lat,color=conf_color,marker=".",markersize=4,label=color2confLabel[conf_color])
            axes[1].plot(Lon,Lat,color=dead_color,marker=".",markersize=4,label=color2deadLabel[dead_color])
    axes[0].set(title='Confirm',xlabel='Lontitude',ylabel='Latitude')
    axes[1].set(title='Dead',xlabel='Longitude',ylabel='Latitude')

    for i in range(2):
        handles,labels=axes[i].get_legend_handles_labels()
        by_label=dict(zip(labels,handles))
        axes[i].legend(by_label.values(),by_label.keys())

Coronavirus1()


#Task3(version2)
def Coronavirus2():
    df_covid=pd.read_csv("DMAI_Lab4_data/coronavirus_China.csv")
    df_city=pd.read_csv("DMAI_Lab4_data/cities.csv")
    dict_city={}
    for row in df_city.itertuples():
        dict_city[row.City]=(float(row.Lon[2:]),float(row.Lat[2:]))
    L_conf=[10,30,100,300,1000,3000,10000]
    L_dead=[1,3,10,30,100,300,1000]
    L_color=["green","lightgreen","yellow","gold","darkorange","red","darkred","purple"]
    dict_conf={c:[[],[]] for c in L_color}
    dict_dead={c:[[],[]] for c in L_color}
    dict_lab_conf={L_color[i]:"<"+str((L_conf+[10000])[i]) for i in range(len(L_color))}
    dict_lab_dead={L_color[i]:"<"+str((L_dead+[1000])[i]) for i in range(len(L_color))}
    dict_lab_conf["purple"]=">=10000"
    dict_lab_dead["purple"]=">=1000"
    
    fig,axes=plt.subplots(1,2,figsize=(20,10),dpi=100)
    for row in df_covid.itertuples():
        city=row.Region
        conf=row.Total_confirm
        dead=row.Total_dead
        conf_color=L_color[Interval(L_conf,conf)]
        dead_color=L_color[Interval(L_dead,dead)]
        if city in dict_city:
            Lon=dict_city[city][0]
            Lat=dict_city[city][1]
            dict_conf[conf_color][0].append(Lon)
            dict_conf[conf_color][1].append(Lat)
            dict_dead[dead_color][0].append(Lon)
            dict_dead[dead_color][1].append(Lat)
    for color,loc in dict_conf.items():
        axes[0].scatter(loc[0],loc[1],marker="o",label=dict_lab_conf[color])
    for color,loc in dict_dead.items():
        axes[1].scatter(loc[0],loc[1],marker="o",label=dict_lab_dead[color])
    axes[0].set(title='Confirm',xlabel='Lontitude',ylabel='Latitude')
    axes[1].set(title='Dead',xlabel='Longitude',ylabel='Latitude')
    axes[0].legend(ncol=2)
    axes[1].legend(ncol=2)
    

#Coronavirus2()

