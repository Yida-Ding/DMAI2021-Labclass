import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from haversine import haversine

def HW1():
    df=pd.read_csv("DMAI_Lab5_data/runways.csv",na_filter=None)
    df=df[pd.to_numeric(df["length_ft"])<15000]
    fig,ax=plt.subplots(figsize=(10,5))
    ax.set_xlim(0,30000)
    jp=sns.distplot(pd.to_numeric(df["length_ft"]),bins=10,ax=ax,kde=False)    

def HW2():
    df=pd.read_csv("DMAI_Lab5_data/runways.csv",na_filter=None)
    jp=sns.jointplot(pd.to_numeric(df["length_ft"]),pd.to_numeric(df["width_ft"])
        ,height=8,kind="scatter")

def Interval(L,n):
    for i in range(len(L)):
        if L[i]>n:
            return i-1
    return len(L)-1

def Task1():
    df=pd.read_csv("DMAI_Lab5_data/runways.csv",na_filter=None)
    df=df[pd.to_numeric(df["length_ft"])<15000]
    widL=[0,100,200,500,1000,2000]
    clsL=["C1","C2","C3","C4","C5","C6","None"]
    rw_widcls,rw_leng,rw_light=[],[],[]
    for row in df.itertuples():
        if row.length_ft!="":
            if row.width_ft=="":
                rw_widcls.append("None")
            else:
                wid=float(row.width_ft)
                rw_widcls.append(clsL[Interval(widL,wid)])
            rw_leng.append(float(row.length_ft))
            rw_light.append(row.lighted)
            
    fig,ax=plt.subplots(figsize=(12,5))
    dfn=pd.DataFrame({"width_class":rw_widcls,"length_ft":rw_leng,"lighted":rw_light})
    sns.boxplot(x=dfn["width_class"],y=dfn["length_ft"],hue=dfn["lighted"],ax=ax,order=clsL)

Task1()

def Task2(subtask):
    df_air=pd.read_csv("DMAI_Lab5_data/airports.csv",na_filter=None)
    df_nav=pd.read_csv("DMAI_Lab5_data/navaids.csv",na_filter=None)
    df_air["elevation_ft"]=pd.to_numeric(df_air["elevation_ft"])
    df_air=df_air[df_air["iso_country"]=="CN"]
    L_dis=[]
    for air in df_air.itertuples():
        Lat=air.latitude_deg
        Lon=air.longitude_deg
        min_dis=float("inf")
        for nav in df_nav.itertuples():
            if abs(Lat-nav.latitude_deg)<5 and abs(Lon-nav.longitude_deg)<5:
                dis=haversine((Lat,Lon),(nav.latitude_deg,nav.longitude_deg))
                if dis<min_dis:
                    min_dis=dis
        L_dis.append(min_dis)
    df_air["nav_dis"]=L_dis
    if subtask==1:
        fig,ax=plt.subplots(figsize=(12,5))
        sns.boxplot(x=df_air["type"],y=df_air["nav_dis"],ax=ax)
    else:
        jp=sns.jointplot(df_air["elevation_ft"],df_air["nav_dis"],height=5,kind="scatter")
        jp.fig.set_figwidth(10)

#Task3
def Task3():
    df_air=pd.read_csv("DMAI_Lab5_data/airports.csv",na_filter=None)
    df_run=pd.read_csv("DMAI_Lab5_data/runways.csv",na_filter=None)
    df_run["width_ft"]=pd.to_numeric(df_run["width_ft"])
    df_run["length_ft"]=pd.to_numeric(df_run["length_ft"])
    
    df_air=df_air[df_air["type"].isin(["medium_airport","large_airport"])]
    df_air=df_air[df_air["iso_country"].isin(["CN","US","DE","RU"])]
    identL=df_air["ident"]
    ident2country={row.ident:row.iso_country for row in df_air.itertuples()}
    df_run=df_run[df_run["airport_ident"].isin(identL)]

    L_country,L_avelen,L_avewid=[],[],[]
    for ident,df_cur in df_run.groupby("airport_ident"):
        if len(df_run)>0:
            L_country.append(ident2country[ident])
            L_avelen.append(df_cur["length_ft"].mean())
            L_avewid.append(df_cur["length_ft"].mean())
    dfn=pd.DataFrame({"iso_country":L_country,"ave_length":L_avelen,"ave_width":L_avewid})

    fig,axes=plt.subplots(1,3,figsize=(20,10))
    sns.boxplot(x=dfn["iso_country"],y=dfn["ave_length"],ax=axes[0])
    sns.boxplot(x=dfn["iso_country"],y=dfn["ave_width"],ax=axes[1])
    sns.countplot(dfn.iso_country)

#Country()

