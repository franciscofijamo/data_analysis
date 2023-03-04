# importing libs
import pandas as pd
import numpy as np
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
# df1 = df1.reset_index(drop = True)
# for i in range(len(df1)):
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
st.header('Marketplace - Restaurant')
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
        st.title("Overal Metrcis")
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Unique Delivery', delivery_unique)

        with col2:
            cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x:
                                                    haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
            avg_distance = np.round(df1['distance'].mean(), 2)
            col2.metric('AVG Delivery Distance', avg_distance)

        with col3:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = (df1.loc[:, cols]
                         .groupby('Festival')
                         .agg({'Time_taken(min)': ['mean', 'std']}))

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            df_aux = np.round(df_aux.loc[df_aux['Festival']=='Yes', 'avg_time'], 2)
            col3.metric('AVG Del/Time/Festival', df_aux)

            
        with col4:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = (df1.loc[:, cols]
                         .groupby('Festival')
                         .agg({'Time_taken(min)': ['mean', 'std']}))

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            df_aux = np.round(df_aux.loc[df_aux['Festival']=='Yes', 'std_time'], 2)
            col4.metric('STD Del/Time/Festival', df_aux)

        with col5:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = (df1.loc[:, cols]
                         .groupby('Festival')
                         .agg({'Time_taken(min)': ['mean', 'std']}))

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            df_aux = np.round(df_aux.loc[df_aux['Festival']=='No', 'avg_time'], 2)
            col5.metric('AVG Del/Time/Festiva', df_aux)

        with col6:
            cols = ['Time_taken(min)', 'Festival']
            df_aux = (df1.loc[:, cols]
                         .groupby('Festival')
                         .agg({'Time_taken(min)': ['mean', 'std']}))

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            df_aux = np.round(df_aux.loc[df_aux['Festival']=='No', 'std_time'], 2)
            col6.metric('STD Del/Time/Festival', df_aux)


    # container pizza 01
    with st.container():
        st.markdown("""-----""")
        col1, col2 = st.columns([2,1])

        with col1:
            #st.markdown('##### col1')
            df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            fig = go.Figure()
            fig.add_trace( go.Bar( name = 'Control', x = df_aux['City'], y = df_aux['avg_time'],
                            error_y=dict(type = 'data', array=df_aux['std_time'])))

            fig.update_layout(barmode = 'group')
            st.plotly_chart(fig)

        with col2:
            cols = ['City', 'Time_taken(min)', 'Type_of_order']
            df_aux = (df1.loc[:, cols]
                        .groupby(['City', 'Type_of_order'])
                        .agg({'Time_taken(min)':['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            st.dataframe(df_aux)
            
    with st.container():
        st.markdown("""-----""")
        # st.title("Time Distribution")
        col1, col2 = st.columns([2,1])

        with col1:
            #st.markdown('Average Distance')
            cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x:
                                                    haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
            fig = go.Figure( data =[ go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0.1,0])])
            st.plotly_chart(fig)

        with col2:
            #st.markdown('Time Distribution')
            cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
            df_aux = (df1.loc[:, cols]
                         .groupby( ['City', 'Road_traffic_density'])
                         .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values = 'avg_time',
                            color = 'std_time', 
                            color_continuous_midpoint=np.average(df_aux['std_time']))

            st.plotly_chart(fig)
            
        #with col2:
            # cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
            # df_aux = (df1.loc[:, cols]
            #              .groupby( ['City', 'Road_traffic_density'])
            #              .agg({'Time_taken(min)': ['mean', 'std']}))
            # df_aux.columns = ['avg_time', 'std_time']
            # df_aux = df_aux.reset_index()

            # fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values = 'avg_time',
            #                 color = 'std_time', 
            #                 color_continuous_midpoint=np.average(df_aux['std_time']))

            # st.plotly_chart(fig)
    
    # with st.container():
    #     st.markdown("""-----""")
    #     st.title("Distance Distribution")

    #     cols = ['City', 'Time_taken(min)', 'Type_of_order']
    #     df_aux = (df1.loc[:, cols]
    #                  .groupby(['City', 'Type_of_order'])
    #                  .agg({'Time_taken(min)':['mean', 'std']}))
    #     df_aux.columns = ['avg_time', 'std_time']
    #     df_aux = df_aux.reset_index()

    #     st.dataframe(df_aux)
