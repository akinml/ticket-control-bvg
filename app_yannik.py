import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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


public_stations = pd.read_csv("datanew_map2.csv")
data1 = pd.read_csv('data/s_u_stations_fixed.csv')




def main():
    lat_list, lon_list = generate_random_coordinates_list()
    data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    berlin_df = pd.DataFrame(data)
    datetimenow = time.strftime("%H:%M:%S")
    st.title(f"Welcome to BVG Controllers Berlin 👋")
    st.map(data=public_stations, zoom=10, color="color", size=50)

    #Minutes slider
    st.slider('Minutes', 0, 60, 0)

    #Select day of week
    option = st.selectbox(
    'Day of week',
    ('None', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', "Sunday"))
    st.write('You selected:', option)


    #Select month
    option1 = st.selectbox(
    'Month',
    ('None', 'January', 'Febraury', 'March', 'April', 'June', 'July', "August",'September','October', 'November', 'December'))
    st.write('You selected:', option1)


    #Date range
    five_years_ago = datetime.today() - timedelta(days=5*365)

    date_range = st.date_input(
    "Select your datet range:",
    value=(datetime.today(), datetime.today() + timedelta(days=0)),
    min_value=five_years_ago,
    max_value=datetime.today()
)

    st.write("Your date range is:", date_range)

    #Select Stations
    selected_options = st.multiselect("Select Station(s):", data1["station name"])
    st.write("You selected:", selected_options)

    # Add a refresh button
    st.table(berlin_df)
    output = st.empty()



    # Load your existing database into a DataFrame
    data = pd.read_csv('/home/yannik/ticket-control-bvg/data/data20230831.csv')  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    df = data.copy()

    # Count occurrences of areas
    area_counts = df['area'].value_counts()

    # Streamlit app
    st.title("Area Occurrences")

    st.write("Area Counts:")
    st.write(area_counts)

    # Plot using Streamlit and Matplotlib
    st.write("Area Occurrences:")
    plt.figure(figsize=(8, 6))
    sns.barplot(x=area_counts.index, y=area_counts.values)
    plt.xlabel("Area")
    plt.ylabel("Count")
    plt.title("Area Occurrences")
    st.pyplot(plt)



    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)


if __name__ == "__main__":
    main()
