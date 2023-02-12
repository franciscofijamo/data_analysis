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
path = '/Users/franciscocaetano/Documents/Comunidade DS/data_analysis/image/Asset 1trabsparent.png'
image = Image.open(path)
st.sidebar.image(image, width=50)
st.header('Marketplace - Delivery')
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('### Fastest Devilvery in Town')
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
tab1, tab2, tab3 = st.tabs(['Management', '_','_'])

with tab1:

    with st.container():
        
        st.markdown('##### Overall Metrics')
        col1, col2,col3,col4 = st.columns(4, gap = 'large')
        with col1:
            max_age = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Max age', max_age )
        with col2:
            min_age =  df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Min age', min_age )
        with col3:
            better_condition = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Better Condition', better_condition )
        with col4:
            worse_condition =  df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Better Condition', worse_condition )
    with st.container():
        st.markdown("""---""")
        st.title('Avaliations')


        col1,col2 = st.columns(2)
        with col1:
            st .markdown('##### Average rate per delivery')
            df_average_rating_per_deliver = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                            .groupby(['Delivery_person_ID'])
                                            .mean()
                                            .reset_index())
            st.dataframe(df_average_rating_per_deliver)
        with col2:
            st.markdown('##### Average rate per traffic')
            #using one line
            #df_average_rating_by_trafic = df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]].groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings':['mean','std']})

            #using two lines
            df_avg_std_by_trafic = (df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]]
                                        .groupby(['Road_traffic_density'])
                                        .agg({'Delivery_person_Ratings':['mean','std']}))

            #df_std_rating_by_trafic = df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]].groupby(['Road_traffic_density']).std().reset_index()
            # Manipulation dataframe column name
            df_avg_std_by_trafic.columns = ['delivery_mean', 'delivery_std']
            # Manipulation dataframe format

            df_avg_std_by_trafic=df_avg_std_by_trafic.reset_index()
            st.dataframe(df_avg_std_by_trafic)


            st.markdown('##### Average rate per weather')
                        #using one line
            #df_average_rating_by_trafic = df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]].groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings':['mean','std']})

            #using two lines
            df_avg_std_by_trafic = (df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]]
                                        .groupby(['Road_traffic_density'])
                                        .agg({'Delivery_person_Ratings':['mean','std']}))

            #df_std_rating_by_trafic = df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]].groupby(['Road_traffic_density']).std().reset_index()

            # Manipulation dataframe column name
            df_avg_std_by_trafic.columns = ['delivery_mean', 'delivery_std']
            # Manipulation dataframe format

            st.dataframe(df_avg_std_by_trafic)
    

    with st.container():
        st.markdown("""---""")
        st.title('Velocity of delivery')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top Fastest Deliverys')
            df2 = (df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City']]
                    .groupby(['City', 'Delivery_person_ID'])
                    .median()
                    .sort_values(['Time_taken(min)', 'City'], ascending = False).reset_index())

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', : ].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', : ].head(10)
            df_aux03  = df2.loc[df2['City'] == 'Semi-Urban', : ].head(10)

            df3 = pd.concat([df_aux01,df_aux02,df_aux03]).reset_index(drop = True)
            st.dataframe(df3)

        
        with col2:
            st.markdown('##### Slower Deliverys')
            df2 = (df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City']]
                    .groupby(['City', 'Delivery_person_ID'])
                    .mean()
                    .sort_values(['Time_taken(min)', 'City'], ascending = True).reset_index())

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', : ].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', : ].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', : ].head(10)

            df3 = pd.concat([df_aux01,df_aux02,df_aux03]).reset_index(drop = True)
            st.dataframe(df3)



