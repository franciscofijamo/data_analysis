
#importing libs
import pandas as pd
from numpy import inner
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
from folium.vector_layers import Popup
import folium


#importing datasets
url = 'https://raw.githubusercontent.com/franciscofijamo/0-to-DS/master/train%20(1).csv'
df= pd.read_csv(url)
print(df.head())
