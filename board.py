from numpy import timedelta64
import pandas as pd
import plotly.express as px
import streamlit as st


sheet_id = '1MPswF1BgvMhIpYLjbuSbwweszx7Vx_fs3YonLkRXK5k/'
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}export?format=csv", header=None, sep='\r')
df = df[0].str.split(',', expand=True)
df.columns = df.iloc[0]
df.drop(0, inplace=True)
df['Food in Milliliter'] = df['Food in Milliliter'].astype('int')
df['Defecation_'] = df['Defecation'].map({'Yes':1, 'No':0})
df['Vitamins_'] = df['Vitamins'].map({'Yes':1, 'No':0})
df['Vomiting_'] = df['Vomiting'].map({'Yes':1, 'No':0})
df['Full Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.sort_values(by= 'Full Time',inplace=True)
df.replace('', 'No', inplace=True)
df['TimeDiff'] = round(df['Full Time'].astype('datetime64[ns]').diff()/timedelta64(1, 'h'),3)
recent = df[['Full Time', 'Food in Milliliter','TimeDiff', 'Defecation', 'Vitamins', 'Vomiting']].tail()

def highlight_late(s):
    return ['background-color: #95F738' if s_=='Yes' else 'background-color: None' for s_ in s]


head = st.container()
recentMeals = st.container()
charts = st.container()

with head:
    st.title('The Erez Mazor Feeding Board !')
    st.text('Starring...Erez Mazor (aka OJ)')
    
with recentMeals:
    st.text('')
    st.text('')
    st.header('Recent Meals:')
    st.write(recent.style.apply(highlight_late))
    st.text('Review all Records:')
    st.markdown('https://docs.google.com/spreadsheets/d/1MPswF1BgvMhIpYLjbuSbwweszx7Vx_fs3YonLkRXK5k/edit?usp=sharing')


df['Date'] = pd.to_datetime(df['Date'])

group = df.groupby('Date', as_index=False, dropna=False).agg(
    Mean=('Food in Milliliter', 'mean'),
    Count=('Food in Milliliter', 'count'), 
    TimeDiffMean=('TimeDiff','mean')).sort_values('Date')

with charts:
    st.text('')
    st.header('Averege Food Per-Day (in Milliliter)')
    fig1 = px.line(group, x="Date", y="Mean", width=1250).update_traces(line=dict(color="Green", width=7))
    st.write(fig1)
    
    st.text('')
    st.header('Count of Meals Per-Day')
    fig2 = px.bar(group, x="Date", y="Count", width=1250).update_traces(marker_color='orange') 
    st.write(fig2)
    
    st.text('')
    st.header('Averege of Time Between Meals Per-Day (in Hours)')
    fig3 = px.line(group, x="Date", y="TimeDiffMean", width=1250).update_traces(line=dict(color="Blue", width=7))
    st.write(fig3)