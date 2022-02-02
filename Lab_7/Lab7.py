import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from haversine import haversine
import sqlite3
import os

#Task1
def Load():
    if not os.path.exists('Data/airports.db'):
        con=sqlite3.connect("Data/airports.db")
        pd.read_csv("Data/airports.csv").to_sql("airports",con)
        pd.read_csv("Data/regions.csv").to_sql("regions",con)
        pd.read_csv("Data/runways.csv").to_sql("runways",con)
        pd.read_csv("Data/navaids.csv").to_sql("navaids",con)
        pd.read_csv("Data/airport-frequencies.csv").to_sql("airport-frequencies",con)
        pd.read_csv("Data/countries.csv").to_sql("countries",con)
        con.close()
Load()


#Task2
def Simple_SQL():
    con=sqlite3.connect("Data/airports.db")
    
    df1=pd.read_sql("SELECT name FROM airports \
                WHERE iso_country='CN'",con)
    
    df2=pd.read_sql("SELECT iata_code FROM airports \
                WHERE municipality='London'",con)
    
    df3=pd.read_sql("SELECT * FROM airports \
                WHERE scheduled_service='yes'",con)
    
    df4=pd.read_sql("SELECT * FROM airports \
                WHERE continent='SA'",con)
    
    df5=pd.read_sql("SELECT * FROM airports,regions \
                WHERE airports.type='large_airport' \
                AND airports.iso_region=regions.code \
                AND regions.name='Florida'",con)
    
    df6=pd.read_sql("SELECT * FROM runways \
                WHERE airport_ident='ZBAA'",con)
    
    con.close()

#Simple_SQL()


#Task3
def Complex_SQL():
    con=sqlite3.connect("Data/airports.db")
    df1=pd.read_sql("SELECT airports.name,runways.length_ft \
                    FROM airports,runways \
                    WHERE runways.airport_ref=airports.id \
                    ORDER BY runways.length_ft DESC LIMIT 1",con)
    
    df2=pd.read_sql("SELECT airports.name,runways.surface \
                    FROM airports,runways \
                    WHERE runways.airport_ref=airports.id \
                    AND (runways.surface='concrete' \
                    OR runways.surface='Concrete' \
                    OR runways.surface='CONCRETE')",con)

    df3=pd.read_sql("SELECT runways.* \
                    FROM airports,runways,regions \
                    WHERE runways.airport_ref=airports.id \
                    AND regions.code=airports.iso_region \
                    AND runways.lighted=1 \
                    AND regions.name='Hebei Province'",con)
    con.close()
    print(df1,len(df1))
#Complex_SQL()


#Task3-M2
def Task3_M2():
    con=sqlite3.connect("Data/airports.db")
    cur=con.cursor()
    cur.execute("SELECT airports.name,runways.length_ft \
                 FROM airports,runways \
                 WHERE runways.airport_ref=airports.id \
                 AND runways.length_ft=(SELECT MAX(CAST(runways.length_ft as int)) FROM runways)")
    print(cur.fetchall())
    con.close()
#Task3_M2()  


#Task2
def Task2():
    con=sqlite3.connect("Data/employees.db")
    cur=con.cursor()
#    df=pd.read_sql("SELECT * FROM sqlite_master",con)
#    print(df["sql"])
    
    cur.execute("SELECT * FROM employees")
    for row in cur.description:
        print(row[0])
    
    
    
    
    
Task2()  
    
    
#    tables=[]
#    for row in cur:
#        if row[0]=="table":
#            tables.append(row[1])
#    for table in tables:
#            attr.append(xx[0])
#        print(table,attr,len(cur.fetchall()))
#    cur.close()
#    con.close()


#Task5
def Query():
    con=sqlite3.connect("Data/employees.db")
    df1=pd.read_sql("SELECT employees.first_name,employees.last_name \
                    FROM employees \
                    WHERE hire_date>'1995-00-00' \
                    AND gender='F' \
                    ORDER BY employees.birth_date \
                    LIMIT 5",con)
    
    df2=pd.read_sql("SELECT employees.first_name,employees.last_name \
                    FROM employees \
                    WHERE birth_date>'1957-03-00' \
                    AND birth_date<'1957-04-00' \
                    AND gender='M' \
                    LIMIT 5",con)
    
    df3=pd.read_sql("SELECT *\
                    FROM titles,dept_emp,departments \
                    WHERE titles.emp_no=dept_emp.emp_no \
                    AND dept_emp.dept_no=departments.dept_no \
                    AND titles.title='Senior Engineer' \
                    AND departments.dept_name='Production' \
                    AND titles.from_date<='1995-01-01' \
                    AND titles.to_date>='1995-12-31' \
                    LIMIT 5",con)
    con.close()
    print(df3)
    
Query()
