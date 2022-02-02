import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlite3
import time

def Task1(subtask):
    con=sqlite3.connect("Data/employees.db")
    
    df1=pd.read_sql("SELECT departments.dept_name,MIN(salary),MAX(salary),AVG(salary)\
                    FROM dept_manager,salaries,departments,employees \
                    WHERE dept_manager.dept_no=departments.dept_no \
                    AND dept_manager.emp_no=employees.emp_no \
                    AND salaries.emp_no=employees.emp_no \
                    AND dept_manager.from_date<=salaries.from_date \
                    AND dept_manager.to_date>=salaries.to_date \
                    GROUP BY dept_manager.dept_no",con)

    df2=pd.read_sql("SELECT titles.emp_no,dept_no,titles.title \
                    FROM dept_manager,titles \
                    WHERE dept_manager.emp_no=titles.emp_no \
                    AND (dept_manager.from_date<=titles.to_date \
                    OR (dept_manager.from_date<=titles.from_date AND dept_manager.to_date>=titles.to_date)) \
                    GROUP BY titles.emp_no,titles.title",con)
                            
    if subtask==2:
        L_title=df2["title"].tolist()
        L_dist=list(set(L_title))
        dict_res={}
        for t in L_dist:
            dict_res[t]=L_title.count(t)
        print(df2)
        print(dict_res)

Task1(2)

    
def Query(subtask,con):
    t1=time.time()
    if subtask==1:
        df1=pd.read_sql("SELECT employees.emp_no,salary \
                        FROM employees,salaries \
                        WHERE employees.emp_no=salaries.emp_no \
                        AND salary=70000",con)
    else:
        df2=pd.read_sql("SELECT emp_no,first_name \
                        FROM employees \
                        WHERE first_name='Dietrich'",con)
    t2=time.time()
    return t2-t1

def Task2(subtask):
    con=sqlite3.connect("Data/employees.db")
    cur=con.cursor()
    
    cur.execute("CREATE INDEX IF NOT EXISTS salaryIndex on salaries(salary)")
    cur.execute("CREATE INDEX IF NOT EXISTS nameIndex on employees(first_name)")
    index_time=Query(subtask,con)
    
    cur.execute("DROP INDEX salaryIndex")
    cur.execute("DROP INDEX nameIndex")
    normal_time=Query(subtask,con)
    
    con.commit()
    con.close()
    
    print("index_time",index_time)
    print("normal_time",normal_time)
    
#Task2(2)


def Task3():
    con=sqlite3.connect("Data/employees.db")
    cur=con.cursor()
    cur.execute("CREATE VIEW IF NOT EXISTS task3view1 AS \
                SELECT departments.dept_name,AVG(salary) AS avg_salary,COUNT(dept_emp.emp_no) AS num_employee \
                FROM salaries,departments,employees,dept_emp \
                WHERE dept_emp.dept_no=departments.dept_no \
                AND salaries.emp_no=employees.emp_no \
                AND employees.emp_no=dept_emp.emp_no \
                GROUP BY departments.dept_no")
    
    cur.execute("CREATE VIEW IF NOT EXISTS task3view2 AS \
                SELECT MIN(salary) AS min_salary,COUNT(dept_emp.emp_no) AS num_employee \
                FROM salaries,employees,dept_emp,titles \
                WHERE employees.emp_no=titles.emp_no \
                AND salaries.emp_no=employees.emp_no \
                AND employees.emp_no=dept_emp.emp_no \
                GROUP BY titles.title")    
    con.commit()
    con.close()


def Task4(subtask):
    con=sqlite3.connect("Data/employees.db")
    
    df1=pd.read_sql("SELECT emp_no,AVG(salary) AS ave_salaries,MIN(salary) \
                    AS min_salaries,MAX(salary) AS max_salaries \
                    FROM salaries \
                    GROUP BY emp_no",con)
    
    df2=pd.read_sql("SELECT departments.dept_name,salaries.salary\
                    FROM dept_manager,salaries,departments,employees \
                    WHERE dept_manager.from_date<=salaries.from_date \
                    AND dept_manager.to_date>=salaries.to_date \
                    AND dept_manager.dept_no=departments.dept_no \
                    AND salaries.emp_no=employees.emp_no \
                    AND dept_manager.emp_no=employees.emp_no",con)

    if subtask==1:
        print(df1)
        fig,ax=plt.subplots(1,3,figsize=(20,10))
        sns.distplot(pd.to_numeric(df1["ave_salaries"]),
            kde=False,bins=10,ax=ax[0])    
        ax[0].set_title("Average salaries")
        
        sns.distplot(pd.to_numeric(df1["min_salaries"]),
            kde=False,bins=10,ax=ax[1])    
        ax[1].set_title("Minimum salaries")
        
        sns.distplot(pd.to_numeric(df1["max_salaries"]),
            kde=False,bins=10,ax=ax[2])    
        ax[2].set_title("Maximum salaries")

    elif subtask==2:
        fig,ax=plt.subplots(figsize=(30,10))
        sns.boxplot(x=df2["dept_name"],y=pd.to_numeric(df2["salary"])
                ,ax=ax)
        ax.set_xlabel("dept_name")
        ax.set_ylabel("salary")
        print(df1)

#Task4(2)



