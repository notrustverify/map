import mapNodes
import pandas as pd
import matplotlib
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

if __name__ == '__main__':
    mapping = mapNodes.MapNodes()
    coord = mapping.getGateways()


    fig, ax = plt.subplots(figsize=(8,6))
    df =  pd.DataFrame(coord,columns=['latitude','longitude'])


    fig = go.Figure(data=go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        mode = 'markers',
        ))
    
    fig.show()
