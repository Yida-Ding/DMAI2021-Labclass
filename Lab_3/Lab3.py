import pandas as pd
from haversine import haversine
import time
import numpy as np


#HW Task2
def Selection():
    df=pd.read_csv("runways.csv")
    df_select=df[(df["length_ft"]>10000)&(df["width_ft"]>60)&(df["lighted"]==1)]
    df_res=df_select.loc[:,["airport_ident","id"]]
    df_res.to_csv("T2.csv")
#Selection()

#HW Task3
def BCIA():
    df_air=pd.read_csv("airports.csv")
    df_run=pd.read_csv("runways.csv")
    df_BCIA=df_air[df_air["name"]=="Beijing Capital International Airport"]
    ident=df_BCIA["ident"].tolist()[0]  
    df_select=df_run[df_run["airport_ident"]==ident]
    aveLen=sum(df_select["length_ft"].tolist())/len(df_select["length_ft"].tolist())
    Num=len(df_select)
    return Num,"%.1f"%aveLen
#print(BCIA())

#Task1(1)
def longest_runway():
    df_run=pd.read_csv("runways.csv")
    df_air=pd.read_csv("airports.csv")
    df_cur=df_run[df_run["length_ft"]==df_run["length_ft"].max()]
    ident=df_cur["airport_ident"].tolist()[0]
    df_select=df_air[df_air["ident"]==ident]
    name=df_select["name"].tolist()[0]
    return name
#print(longest_runway())

#Task1(2)
def concrete_surface():
    df_air=pd.read_csv("airports.csv")
    df_run=pd.read_csv("runways.csv")
    df_run=df_run[df_run["surface"].isin(["Concrete","concrete","CONCRETE"])]
    L=list(set(df_run["airport_ident"].tolist()))
    df_res=df_air[df_air["ident"].isin(L)]
    return len(df_res["name"])

#print(concrete_surface())


def Hebei_lighted():
    df_air=pd.read_csv("airports.csv")
    df_run=pd.read_csv("runways.csv")
    df_reg=pd.read_csv("regions.csv")
    code=df_reg[df_reg["name"]=="Hebei Province"]["code"].tolist()[0]
    L_hba=df_air[df_air["iso_region"]==code]["ident"].tolist()
    df_res=df_run[(df_run["lighted"]==1)&(df_run["airport_ident"].isin(L_hba))]
    print(df_res)
    
#Hebei_lighted()


#Task2(1)
def average_length1():
    df_fq=pd.read_csv("airport-frequencies.csv")
    df_fq=df_fq[(df_fq["frequency_mhz"]>119)&(df_fq["frequency_mhz"]<121)]
    df_run=pd.read_csv("runways.csv")
    L=df_fq["airport_ident"].tolist()
    res_dict={}
    for ident in L:
        df_cur=df_run[df_run["airport_ident"]==ident]
        M=df_cur["length_ft"].tolist()
        if len(M)!=0:
            res_dict[ident]=sum(M)/len(M)
    return res_dict

def average_length2():
    df_fq=pd.read_csv("airport-frequencies.csv")
    df_fq=df_fq[(df_fq["frequency_mhz"]>119)&(df_fq["frequency_mhz"]<121)]
    L=df_fq["airport_ident"].tolist()
    df_run=pd.read_csv("runways.csv")
    df_run=df_run[df_run["airport_ident"].isin(L)]
    res_dict={}
    for ident,df_cur in df_run.groupby("airport_ident"):
        M=df_cur["length_ft"].tolist()
        if len(M)!=0:
            res_dict[ident]=sum(M)/len(M)
    return res_dict

#print(average_length2())


#Task2(2)
def region_country():
    df_fq=pd.read_csv("airport-frequencies.csv")
    df_fq=df_fq[(df_fq["frequency_mhz"]>119)&(df_fq["frequency_mhz"]<121)]
    L=df_fq["airport_ident"].tolist()
    df_air=pd.read_csv("airports.csv")
    df_air=df_air[df_air["ident"].isin(L)]
    res=[]
    for ident,df_cur in df_air.groupby("ident"):
        res.append([df_cur["iso_country"].tolist()[0],df_cur["iso_region"].tolist()[0]])
    return res

#print(region_country())


#Task3
def great_airports():
    df_air=pd.read_csv("airports.csv")
    df_run=pd.read_csv("runways.csv")
    df_nav=pd.read_csv("navaids.csv")
    df_CN=df_air[df_air["iso_country"]=="CN"]
    L=df_CN["ident"].tolist()
    df_run=df_run[df_run["airport_ident"].isin(L)]
    ident2info={row.ident:[row.name,row.iso_region,row.latitude_deg,row.longitude_deg] for row in df_air.itertuples()}        
    num_run,name_air,region_air,name_navaid=[],[],[],[]
    for ident,df_cur in df_run.groupby("airport_ident"):
        n=len(df_cur)
        if n>1:
            num_run.append(n)
            name_air.append(ident2info[ident][0])   #O(1) operation
            region_air.append(ident2info[ident][1])
            lat=ident2info[ident][2]
            lon=ident2info[ident][3]
            min_dis=float("inf")
            name_nav=None
            for row in df_nav.itertuples():
                dis=haversine((lat,lon),(row.latitude_deg,row.longitude_deg))
                if dis<min_dis:
                    min_dis=dis
                    name_nav=row.name
            name_navaid.append(name_nav)
    df_res=pd.DataFrame({"Airport":name_air,"Closest_Navaid":name_navaid,"Region":region_air,"Runways":num_run},index=None)
    df_res.to_csv("Task3.csv",index=None)
    
#great_airports()

#Task4
def great_region():
    df_reg=pd.read_csv("regions.csv",encoding='utf-8')
    df_air=pd.read_csv("airports.csv",encoding='utf-8')
    df_run=pd.read_csv("runways.csv")
    code2name={row.code:row.name for row in df_reg.itertuples()}
    codes=set(df_reg["code"].tolist())
    df_air=df_air[df_air["iso_region"].isin(codes)]
    typeL=['small_airport','medium_airport','large_airport']
    
    #precompute sum of runway length,number of runways for each airport
    air2rwleng={}
    air2rwnum={}
    for ident,df_cur in df_run.groupby("airport_ident"):
        air2rwleng[ident]=sum(df_cur["length_ft"].tolist())
        air2rwnum[ident]=len(df_cur["length_ft"].tolist())
    
    reg_name,num_air,aver_len=[],[],[]
    for code,df_locAir in df_air.groupby("iso_region"):
        reg_name.append(code2name[code])
        countL=[0,0,0]
        sum_of_rwleng=0
        num_of_rw=0
        for row in df_locAir.itertuples():
            if row.type in typeL:
                countL[typeL.index(row.type)]+=1
                sum_of_rwleng+=air2rwleng.get(row.ident,0) #O(1) dictionary operation, if key not in dict return 0
                num_of_rw+=air2rwnum.get(row.ident,0)
        num_air.append(countL)
        if num_of_rw==0 or sum_of_rwleng==0:
            aver_len.append(0)
        else:
            aver_len.append(sum_of_rwleng/num_of_rw)
    num_air=np.array(num_air)
    df_res=pd.DataFrame({"region":reg_name,"small":num_air[:,0],"medium":num_air[:,1],"large":num_air[:,2],"average length":aver_len})
    df_res.dropna(inplace=True)
    df_res.to_csv("Task7.csv",index=None)
    
#great_region()
        
        