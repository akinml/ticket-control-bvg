import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


def main():
    # Load your existing database into a DataFrame
    data = pd.read_csv("data/preprocessed_database_telegram.csv")  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    df = data.copy()

    # Streamlit app
    st.title("Data Analysis")

    chart_data = df
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=52.507222,
            longitude=13.332500,
            zoom=11,
            pitch=50,
            ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                get_position='[longitude, latitude]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
                ),
            ],
        ))


    st.map(df, size=20, color='#0044ff')
    st.map(df,
        latitude='latitude',
        longitude='longitude',
        size='col3',
        color='col4')



if __name__ == "__main__":
    main()
