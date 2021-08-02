import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
def app():
    st.title('Community Mapping')

    mapbox_access_token = "pk.eyJ1IjoiZXR5bGVyIiwiYSI6ImNrcnM2YjVmdjFhOWEydW8xdm1ueXI5ZDkifQ.3viiGdmyBZhOadQChg4CAQ"

    fig = go.Figure(go.Scattermapbox(
            lat=[37.0488, 37.5269, 36.6024],
            lon=[-120.6355, -121.0113, -119.9040],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=['Dos Palos Y', 'Monterey Park Tract', 'Raisin City'],
        ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
           accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=37.0488,
                lon=-120.6355
            ),
            pitch=0,
            zoom=7
        ),
    )

    st.plotly_chart(fig)




