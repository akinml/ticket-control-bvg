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
    data = pd.read_csv("data/preprocessed_database_telegram_git.csv")  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    # Streamlit app
    st.title("Data Analysis")
    df = data.copy()
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index)

    day = df.resample('d')['station_key'].count()
    st.line_chart(day)

    week = df.resample('w')['station_key'].count()
    st.line_chart(week)

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


if __name__ == "__main__":
    main()





"""

def main():
    # Load your existing database into a DataFrame
    data = pd.read_csv("data/preprocessed_database_telegram.csv")  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    df = data.copy()
    # Streamlit app
    st.title("Data Analysis")

    day = df.resample('d')['station_key'].count()
    n = pd.to_datetime(df.index)

    df_test = get_line_chart_data()
    st.line_chart(df_test)

if __name__ == "__main__":
    main()"""
