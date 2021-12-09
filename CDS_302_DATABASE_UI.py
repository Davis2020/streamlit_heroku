# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:07:54 2021

@author: davis
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3 as sql

def app():
    conn = sql.connect("github.com/Davis2020/streamlit_heroku/blob/master/Levels_FYI.db")
    comp_query = "select company_name from company"
    title_query = "select title from employee"
    title_df = pd.read_sql(title_query, conn)
    title_df = pd.read_sql_query(title_query, conn)
    l = title_df['title'].values.tolist()
    r = []
    for i in l:
        if i not in r:
            r.append(i)
    ed_query = "select highest_ed_level from experience"
    cmp_df = pd.read_sql(comp_query, conn)
    st.subheader("STEM SALARY DATABASE SEARCH....")
    selection = st.radio("Do you want to view all companies ?", ("No", "Yes"))
    
    if(selection == "Yes"):
        query = '''select company.company_name, employee.name, employee.gender, employee.level, employee.title, employee.base_salary, employee.stock, employee.bonus, employee.highest_ed_level, employee.years_working
        from company
        left join isincompany
        on company.company_id = isincompany.company_id
        left join employee
        on employee.emp_id = isincompany.emp_id
        '''
    else:
        company_name = st.selectbox("Choose company",(cmp_df))

        Highest_ed_level = st.selectbox("Education level",("Bachelor's Degree", "Master's Degree", "PhD", "Some College"))
        Total_years = st.selectbox("Number of years working", (1,2,3,4,5,6,7,8,9,10))
        title = st.selectbox("Job title",(r))

        query = '''select company.company_name, employee.name, employee.gender, employee.level, employee.title, employee.base_salary, employee.stock, employee.bonus, employee.highest_ed_level, employee.years_working
        from company
        left join isincompany
        on company.company_id = isincompany.company_id
        left join employee
        on employee.emp_id = isincompany.emp_id
        where company.company_name = "''' + company_name + "\" and (employee.highest_ed_level = \"" + str(Highest_ed_level) + "\") and employee.years_working <= " + str(Total_years) + " and employee.title = \"" + str(title) + "\""


    df = pd.read_sql(query, conn)
    pd.set_option("display.max_rows", None, "display.max_columns", None)
        
    
    
        

    


    

    


    


    st.table(df)




