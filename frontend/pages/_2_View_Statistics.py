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
from ticket_control.model_preprocessing import *

st_path_to_data = st.secrets.get('PATH_TO_DATA', None)

if st_path_to_data is not None:
    path_to_data = st_path_to_data

# setting config to "wide" so that charts and other elements are properly displayed
st.set_page_config(layout="wide")

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

    st.title("Welcome to BVG Controls:wave:")

    # Streamlit app headline as a combination of 1) title and 2) train animation
    left_column, right_column = st.columns([5, 1])
    with left_column:
        st.header("Statistics:mag_right:", divider='rainbow')
        st.write("DISCLAIMER: given statistics are based on the user inputs of Telegram Channel and might not represent the actual controls")
    with right_column:
        st_lottie(train_animation, height=100, key='train_animation')

    # Creating min & max dates that are important for the filtering logic
    min_date = df.index[0]
    max_date = df.index[-1]

    # applying the filter logic to the dataframe based on selected dates by user
    df = df.loc[user_date_ranges[0]:user_date_ranges[1]]

    # Showing areas, stations and lines
    #st.subheader("Most controlled Areas :tram:") ## too much text

    col1, col2 = st.columns([1, 1])

    # Calculate area frequencies using data ranges selected by user
    # Figure for Bezike >>>
    df_for_bezirk = get_bezirke(df)
    bezirke_counts = df_for_bezirk["bezirk"].value_counts()
    fig9 = px.pie(
        df_for_bezirk,
        values=bezirke_counts.values,
        names=bezirke_counts.index,
        title='Most controlled Districts')
    st.plotly_chart(fig9, use_container_width=True)

    # Figure for areas >>>
    area_counts = df["area"].value_counts()
    # Create a plotly map
    fig1 = px.treemap(
        names=area_counts.index,
        parents=[""] * len(area_counts),
        values=area_counts.values,
        title='Most controlled Areas'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Creating the exploratory chart of Berlin map
    st.subheader("Counts of control per station")
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
            ],
        ))


    # Calculate station frequencies
    station_counts = df["station name"].value_counts()
    # Create a plotly map
    fig2 = px.treemap(
        names=station_counts.index,
        parents=[""] * len(station_counts),
        values=station_counts.values,
        title='Most controlled Stations'
    )
    # Display the figure
    st.plotly_chart(fig2, use_container_width=True)

    # Calculate lines frequencies, but separating "joined" U&Sbahns to count them individually again
    lines_counts = df["lines"].str.split(', ').explode().value_counts()

    # Create a plotly map
    fig3 = px.treemap(
        names=lines_counts.index,
        parents=[""] * len(lines_counts),
        values=lines_counts.values,
        title='Most controlled Lines'
    )
    # Display the figure
    #st.plotly_chart(fig3)

    fig10 = px.pie(
        values=lines_counts.values,
        names=lines_counts.index,
        title='Most controlled Lines')
    st.plotly_chart(fig10, use_container_width=True)

    #day = df.resample('d')['station_key'].count()
    #st.write("Controls across Berlin per Day")
    #st.line_chart(day, color="#4048BF")
    week = df.resample('w')['station_key'].count()
    st.write("Controls across Berlin per Week")
    st.line_chart(week, color="#4048BF", use_container_width=True)

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

    fig6 = px.histogram(df, x="weekday", color_discrete_sequence=['#4048BF'],
                        opacity=1, category_orders={"weekday": weekday_order}, title="Most controlled Days of the Week")
    st.plotly_chart(fig6, use_container_width=True)

    fig5 = px.histogram(df, x="month_name", color_discrete_sequence=['#4048BF'],
                        opacity=1, category_orders={"month_name": month_order}, title="Most controlled Months")
    st.plotly_chart(fig5, use_container_width=True)


    fig7 = px.histogram(df, x="hour", color_discrete_sequence=['#4048BF'],
                        opacity=1, title="Most controlled Hour")
    st.plotly_chart(fig7, use_container_width=True)

### Yearly Distribution >>> ### rather reflects the yerly activity on tg
    fig4 = px.histogram(df, x="year", color_discrete_sequence=['#4048BF'],
                        opacity=1)
    #st.plotly_chart(fig4, use_container_width=False)


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
