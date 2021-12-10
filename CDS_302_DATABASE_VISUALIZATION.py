# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 21:50:06 2021

@author: davis
"""

import streamlit as st
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go





def app():
    
    path = "Levels_FYI.db"
    conn = sql.connect(path)
    comp_query = "select company_name from company"
    cmp_df = pd.read_sql(comp_query, conn)
    comp_name = st.selectbox("Choose company",(cmp_df))
    query = '''select company.company_name, employee.name, employee.gender, employee.level, employee.title, employee.base_salary, employee.stock, employee.bonus, employee.highest_ed_level, employee.years_working
        from company
        left join isincompany
        on company.company_id = isincompany.company_id
        left join employee
        on employee.emp_id = isincompany.emp_id
        where company.company_name = "''' + comp_name + "\""
        
    map_query = '''select location.lat, location.lon
        from company
        left join isincompany
        on isincompany.company_id = company.company_id
        left join location
        on isincompany.city_id = location.city_id
        where company.company_name = "''' + comp_name + "\""
   
    df = pd.read_sql_query(query, conn)
    st.header("Data Visualization")
    education_level = ["Bachelor's Degree", "Master's Degree", "PhD"]
    
    
    ge = df.groupby(["company_name","highest_ed_level"]) 
    es = []
    for i in education_level:
        try:
           df2 = ge.get_group((comp_name,i))
        except KeyError as e:
            b_mean = 0
            es.append(0)
        else:
            df2 = ge.get_group((comp_name,i))
            b_mean = df2["base_salary"].mean()
            es.append(b_mean)
        
    gp = df.groupby(["company_name","title"])
    ps = []
    titles = df["title"].unique().tolist()
    for i in titles:
        try:
            df3 = gp.get_group((comp_name,i))
        except KeyError as e:
            b1_mean = 0
            ps.append(0)
            df3 = gp.get_group((comp_name,i))
        else:
            df3 = gp.get_group((comp_name,i))
            b1_mean = df3["base_salary"].mean()
            ps.append(b1_mean)
            



    
    

    fig1 = px.bar(df2,x=education_level, y=es, color=es,title="Mean salary per education level at " + comp_name)
    fig1.update_layout(width=800)
    

    fig2 = px.bar(df3, x=titles, y=ps, color=ps,title="Mean salaries for different job titles at " + comp_name)
    fig2.update_layout(width=800)
    
    dups = dict(df["gender"].value_counts())
    l = list(dups.keys())
    u = list(dups.values())
    l = l[0:3]
    u = u[0:3]
    print(l)
    print(u)

    data = pd.DataFrame(list(zip(l,u)))
    data.columns = ["Gender", "Value"]
    fig3 = px.pie(data, values="Value", names="Gender", hole=0.5)
    colors = ['gold', 'mediumturquoise', 'lightgreen']
    fig3.update_traces(hoverinfo='label+percent',textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    
    fig3.update_layout(
    title_text="Gender proportions at " + comp_name,
    # Add annotations in the center of the donut pies.
    annotations=[dict(text=comp_name, x=0.50, y=0.5, font_size=20, showarrow=False)])

    
    dup = dict(df["level"].value_counts())
    l = list(dup.keys())
    u = list(dup.values())
    print(l)
    print(u)

    data1 = pd.DataFrame(list(zip(l,u)))
    data1.columns = ["Level", "Count"]
    
    newdf = data1.loc[(data1.Count > 50)]
    
    color = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    fig4 = px.pie(newdf, values="Count", names="Level", hole=0.5)
    fig4.update_traces(hoverinfo='label+percent',textfont_size=20,
                  marker=dict(colors=color,line=dict(color='#000000', width=2)))
    
    fig4.update_layout(
    title_text="Levels proportions at " + comp_name + " for levels with at least 30 employees",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text=comp_name+" work levels", x=0.50, y=0.5, font_size=20, showarrow=False)])


    map_df = pd.read_sql_query(map_query, conn)
    
    

    


    st.subheader("Mean base salary for a given education level.")
    st.write(fig1)
    st.subheader("Mean base salary for a given job title.")
    st.write(fig2)
    st.header("Gender proportions.")
    st.write(fig3)
    st.subheader("Employees level proportions.")
    st.write(fig4)
    st.caption("Proportions are for levels with at least 30 employees")
    st.caption("if plot does not appear, company has levels with less than 30 employees")
    st.subheader("Map of different locations of " + comp_name)
    st.map(map_df)

    
