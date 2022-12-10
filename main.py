import mapNodes
import pandas as pd
import matplotlib
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from db import BaseModel
from utils import Utils
from collections import Counter

if __name__ == '__main__':
    db = BaseModel()
    countries = db.getGatewaysCountry(intervalHour=24)
    print(countries)


    """
    fig, ax = plt.subplots(figsize=(8,6))
    df =  pd.DataFrame(coord,columns=['latitude','longitude'])


    fig = go.Figure(data=go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        mode = 'markers',
        ))
    
    fig.show()
    """