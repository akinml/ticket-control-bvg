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



# Optional change Mapbox map to plotly Map. https://plotly.com/python/scattermapbox/
def generate_random_coordinates():
    min_lat, max_lat = 52.392166, 52.639004
    min_lon, max_lon = 13.215260, 13.770269
    random_lat = random.uniform(min_lat, max_lat)
    random_lon = random.uniform(min_lon, max_lon)
    return random_lat, random_lon


def generate_random_coordinates_list(num_samples=100):
    lat_list = []
    lon_list = []
    for x in range(num_samples):
        random_lat, random_lon = generate_random_coordinates()
        lat_list.append(random_lat)
        lon_list.append(random_lon)
    return lat_list, lon_list

public_stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")
data1 = pd.read_csv(
    str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv"
)


# Page 1 landing page
def page_1_landing_page():
    lat_list, lon_list = generate_random_coordinates_list()
    data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    berlin_df = pd.DataFrame(data)
    datetimenow = time.strftime("%H:%M:%S")
    st.title("Welcome to BVG Controllers BER 👋")
    st.map(data=public_stations, zoom=10, color="color", size=50)

    # Select Stations
    selected_options = st.multiselect("Select station(s):", data1["station name"])
    st.write("You selected:", selected_options)

    # Add a refresh button
    st.table(berlin_df)
    output = st.empty()



    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)


# Load your existing database into a DataFrame
data = pd.read_csv(
    str(path_to_data) + "/preprocessed_database_telegram.csv"
)  # Replace with the path to your database file
# Notice the .copy() to copy the values
df = data.copy()
df["date"] = pd.to_datetime(df["date"])

# Page 2: Control Statistics
def page_2_control_prediction():
    # Streamlit app
    st.title("Predict controls")

    # Select Stations
    selected_options = st.multiselect("Select station(s):", data1["station name"])
    st.write("You selected:", selected_options)


    def load_animation(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    ticket_animation = load_animation("https://lottie.host/22c81fab-c863-457a-ae03-67719eef76e0/T31UETDsXa.json")

    st_lottie(ticket_animation, height=300, key='ticket_animation')


# Page 3: Control Statistics
def page_3_control_statistics():
    # Streamlit app
    st.title("View statistics")

    # description
    min_date = df["date"].iloc[0]

    max_date = df["date"].iloc[-1]

    def load_animation(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    train_animation = load_animation("https://lottie.host/aec64339-af7e-4713-95ad-2c11b57a4bc5/UdfXkvXrvL.json")


    left_column, right_column = st.columns(2)

    with left_column:
        user_date_ranges = st.date_input(
        "Enter a range of two dates or leave blank",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

        # User input for number of top items to display
        top_n_areas = st.selectbox("Select the number of areas to display:", [10, 25, 50])
        top_n_stations = st.selectbox(
            "Select the number of station names to display:", [10, 25, 50]
        )
        top_n_lines = st.selectbox("Select the number of lines to display:", [5, 10, 20])

    with right_column:
        st_lottie(train_animation, height=300, key='train_animation')

    # Arrange tables side by side
    st.write("Control Statistics:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"{top_n_areas} Most controlled areas:")
        area_counts = df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["area"].value_counts()
        st.write(area_counts.head(top_n_areas))

    with col2:
        st.write(f"{top_n_stations} Most controlled stations:")
        station_counts = df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["station name"].value_counts()
        st.write(station_counts.head(top_n_stations))

    with col3:
        st.write(f"{top_n_lines} Most controlled lines:")
        lines_counts = df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["lines"].value_counts()
        st.write(lines_counts.head(top_n_lines))

    st.write("---")

    # Areas
    st.title("Areas, stations & lines visualization")

    st.write('Areas visualization')

    # Calculate area frequencies using data ranges selected by user
    area_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["area"].value_counts()

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
    station_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["station name"].value_counts()
    # Create a plotly map
    fig2 = px.treemap(
        names=station_counts.index,
        parents=[""] * len(station_counts),
        values=station_counts.values
    )

    # Display the figure
    st.plotly_chart(fig2)

    st.write('Lines visualization')
    # Calculate lines frequencies
    lines_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["lines"].value_counts()
    # Create a plotly mapp
    fig3 = px.treemap(
        names=lines_counts.index,
        parents=[""] * len(lines_counts),
        values=lines_counts.values
    )

    # Display the figure
    st.plotly_chart(fig3)

    st.write("---")

    st.title("Time statistics")

    # creating time columns for the differenct categories year, month, weekday, hour
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['day'] = pd.DatetimeIndex(df['date']).weekday
    df['hour'] = df['date'].dt.hour

    # Naming the weekdays
    weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    # Applying the naming
    df["weekday"] = df['day'].map(weekdays)
    # Doing the same for months
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Dec'}
    df["month_name"] = df['month'].map(months)

    # Option 1: Seaborn

    st.write('Distribution of annual controls')
    fig4 = px.histogram(df, x="year", color_discrete_sequence=['#4048BF'],
                        opacity=1)

    st.plotly_chart(fig4, use_container_width=False)

    st.write('Distribution of monthly controls')
    fig4 = px.histogram(df, x="month_name", color_discrete_sequence=['#4048BF'],
                        opacity=1)

    st.plotly_chart(fig4, use_container_width=False)


    st.write('Distribution of daily controls')
    fig4 = px.histogram(df, x="weekday", color_discrete_sequence=['#4048BF'],
                        opacity=1)

    st.plotly_chart(fig4, use_container_width=False)


    st.write('Distribution of hourly controls')
    fig4 = px.histogram(df, x="hour", color_discrete_sequence=['#4048BF'],
                        opacity=1)

    st.plotly_chart(fig4, use_container_width=False)




    # Option 2: Plotly
    # fig = px.histogram(df, x="weekday")
    # fig.show()

# Main app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:", ("Check Controls :rainbow:", "Predict Controls :1234:", "View Statistics :dart:")
    )

    if page == "Check Controls :rainbow:":
        page_1_landing_page()
    elif page == "Predict Controls :1234:":
        page_2_control_prediction()
    elif page == "View Statistics :dart:":
        page_3_control_statistics()


if __name__ == "__main__":
    main()
