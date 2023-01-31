# importing libs
import pandas as pd
from numpy import inner
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
from folium.vector_layers import Popup
import folium
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
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


# =========================================================
# Sidebar bar Streamlit
# =========================================================
path = '/Users/franciscocaetano/Documents/Comunidade DS/data_analysis/image/logo-valuuArtboard 2.png'
image = Image.open(path)
st.sidebar.image(image, width=120)
st.header('Marketplace - Client')
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Devilvery in Town')
st.sidebar.markdown("""-------------------------""")


st.sidebar.markdown('### Select a range date')
date_slider = st.sidebar.slider(
    'Limit value',
    value = pd.datetime(2022,4,13),
    min_value = pd.datetime(2022,2,11),
    max_value = pd.datetime(2022,4,6),
    format='DD-MM-YYYY'
)
st.sidebar.markdown("""-------------------------""")

trafic_options = st.sidebar.multiselect(
    "Select Condition of Tradic",
    ['Low', 'Medium', 'High', 'Jam'],
    default='Low'
)

st.sidebar.markdown("""-------------------------""")
st.sidebar.markdown('##### Powered by Francisco Caetano')

# Date filters 
selected_lines = df1['Order_Date'] < date_slider
df1 = df1.loc[selected_lines, :]


# Date trafic options 
selected_lines = df1['Road_traffic_density'].isin(trafic_options)
df1 = df1.loc[selected_lines, :]
#st.dataframe(df1)

# =========================================================
# Layout Streamlit
# =========================================================
tab1, tab2, tab3 = st.tabs(['Management', 'Tactic','Geographic'])

with tab1:
    st.markdown('# Orders by Day')
    # Order Metric
    cols = ['ID', 'Order_Date']
    df_aux = df1.loc[:, cols].groupby(['Order_Date']).count().reset_index()

    #Ploting with plotly
    fig =  px.bar(df_aux, x ='Order_Date', y = 'ID')
    st.plotly_chart(fig, use_container_width=True) # responsive on the space

    # creating 2 columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('## Traffic order share')
        df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
        df_aux = df_aux.loc[df_aux['Road_traffic_density']!= 'NaN', :]
        df_aux['%_delivery'] = df_aux['ID'] / df_aux['ID'].sum()

        #df_aux
        fig = px.pie(df_aux, values = '%_delivery', names = 'Road_traffic_density')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('## Traffic Order City')
        df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
        df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
        df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

        #df_aux
        fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():

        st.markdown('# Order by week')
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
        df_aux = df1.loc[:,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()

        fig = px.line(df_aux, x= 'week_of_year', y = 'ID')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('# Order share by week')
        # quantidad de pedidos por semana/numero unico de entregadores por semana
        df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

        df_aux = pd.merge(df_aux1,df_aux2, how = 'inner', on= 'week_of_year' )
        df_aux['order_by_delivey'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        #
        fig = px.line(df_aux, x = 'week_of_year', y = 'order_by_delivey')
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('# Country Maps')
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude','Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                 location_info['Delivery_location_longitude']],
                 popup= location_info[['City', 'Road_traffic_density']]).add_to(map)
  
    folium_static(map, width = 1024, height = 600)