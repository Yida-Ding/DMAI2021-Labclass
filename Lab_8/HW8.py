import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlite3

def Task1():
    con=sqlite3.connect("Data/airports.db")
    df1=pd.read_sql("SELECT regions.name AS name, \
                    COUNT(airports.id) AS num_airports, \
                    COUNT(runways.id) AS num_runways, \
                    AVG(runways.length_ft) AS avg_length, \
                    regions.iso_country AS country \
                    FROM airports,runways,regions \
                    WHERE airports.id=runways.airport_ref \
                    AND airports.iso_region=regions.code \
                    GROUP BY airports.iso_region \
                    ORDER BY COUNT(airports.id) DESC \
                    LIMIT 10",con)
    df1.to_csv("Data/Task1.csv",index=None)
    
Task1()


def Task2():
    con=sqlite3.connect("Data/employees.db")
    
    df1=pd.read_sql("SELECT emp_no,AVG(salary) AS ave_salaries, \
                    MIN(salary) AS min_salaries, \
                    MAX(salary) AS max_salaries \
                    FROM salaries \
                    GROUP BY emp_no",con)

    df2=pd.read_sql("SELECT first_name,MIN(salary),MAX(salary),AVG(salary) \
                    FROM salaries,employees \
                    WHERE salaries.emp_no=employees.emp_no \
                    GROUP BY salaries.emp_no \
                    HAVING (MAX(salary)-MIN(salary)<10000) \
                    ORDER BY AVG(salary) ASC",con)
    
    df3=pd.read_sql("SELECT title,COUNT(emp_no) \
                    FROM titles \
                    WHERE (from_date>'1995-00-00') \
                    AND (to_date<'1996-00-00') \
                    GROUP BY title ",con)

#Task2()

def Task3():
    con=sqlite3.connect("Data/employees.db")
    cur=con.cursor()
    
    cur.execute("CREATE VIEW IF NOT EXISTS View1 AS \
                SELECT emp_no,AVG(salary) AS ave_salaries,MIN(salary) \
                AS min_salaries,MAX(salary) AS max_salaries \
                FROM salaries \
                GROUP BY emp_no")
    
    cur.execute("CREATE VIEW IF NOT EXISTS View2 AS \
                SELECT first_name,MIN(salary),MAX(salary),AVG(salary) \
                FROM salaries,employees \
                WHERE salaries.emp_no=employees.emp_no \
                GROUP BY salaries.emp_no \
                HAVING (MAX(salary)-MIN(salary)<10000) \
                ORDER BY AVG(salary) ASC")
    
    cur.execute("CREATE VIEW IF NOT EXISTS View3 AS \
                SELECT title,COUNT(emp_no) \
                FROM titles \
                WHERE (from_date>'1995-00-00') \
                AND (to_date<'1996-00-00') \
                GROUP BY title ")
#Task3()

def Access_view():
    con=sqlite3.connect("Data/employees.db")
    
    df1=pd.read_sql("SELECT * FROM View1",con)
    df2=pd.read_sql("SELECT * FROM View2",con)
    df3=pd.read_sql("SELECT * FROM View3",con)
    print(df1)
#Access_view()

