import streamlit as st
import pandas as pd
import time
import random
import calendar
from datetime import datetime, timedelta, date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from ticket_control.params import path_to_data
import requests
from streamlit_lottie import st_lottie
import plotly.figure_factory as ff
import pydeck as pdk

# Load your existing database into a DataFrame
data = pd.read_csv(
    str(path_to_data) + "/preprocessed_database_telegram.csv"
)  # Replace with the path to your database file
# Notice the .copy() to copy the values
df = data.copy()
df["date"] = pd.to_datetime(df["date"])

# Page 2: Control Statistics
def page_2_control_statistics(df, user_date_ranges):

    # function to load the "train" animation
    def load_animation(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    train_animation = load_animation("https://lottie.host/aec64339-af7e-4713-95ad-2c11b57a4bc5/UdfXkvXrvL.json")

    # Streamlit app headline as a combination of 1) title and 2) train animation
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Control stats:mag_right:")
    with right_column:
        st_lottie(train_animation, height=300, key='train_animation')

    # Creating min & max dates that are important for the filtering logic
    min_date = df.index[0]
    max_date = df.index[-1]

    # applying the filter logic to the dataframe based on selected dates by user
    df = df.loc[user_date_ranges[0]:user_date_ranges[1]]
    st.write("---")

    # Showing areas, stations and lines
    st.title("Areas, stations & lines visualization:tram:" )
    st.write('Areas visualization')

    # Calculate area frequencies using data ranges selected by user
    area_counts = df["area"].value_counts()
    # Create a plotly map
    fig1 = px.treemap(
        names=area_counts.index,
        parents=[""] * len(area_counts),
        values=area_counts.values
    )
    # Display the figure
    st.plotly_chart(fig1)
    st.write('Stations visualization')

    # Calculate station frequencies
    station_counts = df["station name"].value_counts()
    # Create a plotly map
    fig2 = px.treemap(
        names=station_counts.index,
        parents=[""] * len(station_counts),
        values=station_counts.values
    )
    # Display the figure
    st.plotly_chart(fig2)
    st.write('Lines visualization')

    # Calculate lines frequencies, but separating "joined" U&Sbahns to count them individually again
    lines_counts = df["lines"].str.split(', ').explode().value_counts()
    # Create a plotly mapp
    fig3 = px.treemap(
        names=lines_counts.index,
        parents=[""] * len(lines_counts),
        values=lines_counts.values
    )
    # Display the figure
    st.plotly_chart(fig3)
    st.write("---")
    st.title("Time statistics:hourglass:")

    # Creating time columns for the differenct categories year, month, weekday, hour
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.weekday
    df['hour'] = df.index.hour
    # Naming the weekdays
    weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    # Applying the naming
    df["weekday"] = df['day'].map(weekdays)
    # Doing the same for months
    months = {1: 'Jan',
              2: 'Feb',
              3: 'Mar',
              4: 'Apr',
              5: 'May',
              6: 'Jun',
              7: 'Jul',
              8: 'Aug',
              9: 'Sep',
              10: 'Okt',
              11: 'Nov',
              12: 'Dec'}

    df["month_name"] = df['month'].map(months)
    # Setting the correct order for the charts below
    weekday_order = ["Mon",
                     "Tue",
                     "Wed",
                     "Thu",
                     "Fri",
                     "Sat",
                     "Sun"]

    month_order = ["Jan",
                   "Feb",
                   "Mar",
                   "Apr",
                   "May",
                   "Jun",
                   "Jul",
                   "Aug",
                   "Sep",
                   "Okt",
                   "Nov",
                   "Dec"]

    st.write('Distribution of annual controls')
    fig4 = px.histogram(df, x="year", color_discrete_sequence=['#4048BF'],
                        opacity=1)
    st.plotly_chart(fig4, use_container_width=False)
    st.write('Distribution of monthly controls')
    fig5 = px.histogram(df, x="month_name", color_discrete_sequence=['#4048BF'],
                        opacity=1, category_orders={"month_name": month_order})
    st.plotly_chart(fig5, use_container_width=False)

    st.write('Distribution of daily controls')
    fig6 = px.histogram(df, x="weekday", color_discrete_sequence=['#4048BF'],
                        opacity=1, category_orders={"weekday": weekday_order})
    st.plotly_chart(fig6, use_container_width=False)

    st.write('Distribution of hourly controls')
    fig7 = px.histogram(df, x="hour", color_discrete_sequence=['#4048BF'],
                        opacity=1)
    st.plotly_chart(fig7, use_container_width=False)

    # CHECK IF THIS WORKS!!!! IF YES DELETE'
    # CHECK IF THIS WORKS!!!! IF YES DELETE'
    # CHECK IF THIS WORKS!!!! IF YES DELETE'
    # CHECK IF THIS WORKS!!!! IF YES DELETE'
    # # Load your existing database into a DataFrame
    # data = pd.read_csv("data/preprocessed_database_telegram.csv")  # Replace with the path to your database file

    st.title("Time Series")
    day = df.resample('d')['station_key'].count()
    st.write("Timeseries of daily controls")
    st.line_chart(day, color="#4048BF")
    week = df.resample('w')['station_key'].count()
    st.write("Timeseries of weekly controls")
    st.line_chart(week, color="#4048BF", use_container_width=True)

    # Creating the exploratory chart of Berlin map
    st.title("Explore Berlin")
    st.write("Controls across Berlin")
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

# Main app
def main():
    # Load your existing database into a DataFrame
    data = pd.read_csv(
        str(path_to_data) + "/preprocessed_database_telegram.csv"
    )  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    df = data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df = df.sort_index()

    st.sidebar.title("Filter the data")
    min_date = df.index[0]
    max_date = df.index[-1]
    user_date_ranges = st.sidebar.date_input("Enter a range of 2 dates to filter the data",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date)
    page_2_control_statistics(df, user_date_ranges)

if __name__ == "__main__":
    main()
