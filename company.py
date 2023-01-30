# importing libs
import pandas as pd
from numpy import inner
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
from folium.vector_layers import Popup
import folium




#importing datasets
url = 'https://raw.githubusercontent.com/franciscofijamo/0-to-DS/master/train%20(2).csv'
df= pd.read_csv(url)


#data cleasing
df1 = df.copy()
# convering Delivery_person_Age
line_nan = (df1['Delivery_person_Age'] != 'NaN ') 
df1 = df1.loc[line_nan, :].copy()


line_nan = (df1['Road_traffic_density'] != 'NaN ') 
df1 = df1.loc[line_nan, :].copy()

line_nan = (df1['City'] != 'NaN ') 
df1 = df1.loc[line_nan, :].copy()

line_nan = (df1['Festival'] != 'NaN ') 
df1 = df1.loc[line_nan, :].copy()
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

# convering Delivery_person_Ratings
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

# converting Order_Date 
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

# convertig multiple_deliveries
aux = (df1['multiple_deliveries']!= 'NaN ')
df1 = df1.loc[aux, :].copy()

df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

# removing spaces in strings or objects
#df1 = df1.reset_index(drop = True)
#for i in range(len(df1)):
#   df1.loc[i,'ID'] = df1.loc[i, 'ID'].strip()

df1.loc[:,'ID']=df1.loc[:,'ID'].str.strip()
df1.loc[:,'Delivery_person_ID']=df1.loc[:,'Delivery_person_ID'].str.strip()
df1.loc[:,'Type_of_order']=df1.loc[:,'Type_of_order'].str.strip()
df1.loc[:,'Road_traffic_density']=df1.loc[:,'Road_traffic_density'].str.strip()
df1.loc[:,'Type_of_vehicle']=df1.loc[:,'Type_of_vehicle'].str.strip()
df1.loc[:,'Festival']=df1.loc[:,'Festival'].str.strip()
df1.loc[:,'City']=df1.loc[:,'City'].str.strip()

df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min)')[1])
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

# company vision
cols = ['ID', 'Order_Date']
df_aux = df1.loc[:, cols].groupby(['Order_Date']).count().reset_index()

px.bar(df_aux, x ='Order_Date', y = 'ID')


print("Im here")

# =========================================================
# Layout Streamlit

# =========================================================


import streamlit as st

st.header('This is a header')
