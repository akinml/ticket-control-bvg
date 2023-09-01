import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


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


#public_stations = pd.read_csv("datanew_map2.csv")
#data1 = pd.read_csv('home/yannik/ticket-control-bvg/data/s_u_stations_fixed_with_keys_20230830.csv')




def main():
    # lat_list, lon_list = generate_random_coordinates_list()
    # data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    # berlin_df = pd.DataFrame(data)
    # datetimenow = time.strftime("%H:%M:%S")
    # st.title(f"Welcome to BVG Controllers Berlin 👋")
    # st.map(data=public_stations, zoom=10, color="color", size=50)

#     #Minutes slider
#     st.slider('Minutes', 0, 60, 0)

#     #Select day of week
#     option = st.selectbox(
#     'Day of week',
#     ('None', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', "Sunday"))
#     st.write('You selected:', option)


#     #Select month
#     option1 = st.selectbox(
#     'Month',
#     ('None', 'January', 'February', 'March', 'April', 'June', 'July', "August",'September','October', 'November', 'December'))
#     st.write('You selected:', option1)


#     #Date range
#     five_years_ago = datetime.today() - timedelta(days=5*365)

#     date_range = st.date_input(
#     "Select your date range:",
#     value=(datetime.today(), datetime.today() + timedelta(days=0)),
#     min_value=five_years_ago,
#     max_value=datetime.today()
# )

#     st.write("Your date range is:", date_range)

#     #Select Stations
#     #selected_options = st.multiselect("Select Station(s):", data1["station name"])
#     st.write("You selected:", selected_options)

#     # Add a refresh button
#     #st.table(berlin_df)
#     output = st.empty()



    # Load your existing database into a DataFrame
    data = pd.read_csv('/home/yannik/ticket-control-bvg/data/data20230831.csv')  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    df = data.copy()

    # Streamlit app
    st.title("Control Statistics")

    # User input for number of top items to display
    top_n_areas = st.selectbox("Select the number of areas to display:", [10, 25, 50])
    top_n_stations = st.selectbox("Select the number of station names to display:", [10, 25, 50])
    top_n_lines = st.selectbox("Select the number of lines to display:", [5, 10, 20])


    # Arrange tables side by side
    st.write("Control Statistics:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"{top_n_areas} Most controlled areas:")
        area_counts = df['area'].value_counts()
        st.write(area_counts.head(top_n_areas))

    with col2:
        st.write(f"{top_n_stations} Most controlled stations:")
        station_counts = df['station name'].value_counts()
        st.write(station_counts.head(top_n_stations))

    with col3:
        st.write(f"{top_n_lines} Most controlled lines:")
        line_counts = df['lines'].value_counts()
        st.write(line_counts.head(top_n_lines))


    # Areas
    st.title("Control Statistics")

    # Calculate area frequencies
    area_counts = df['area'].value_counts()

    # Create a plotly map
    fig1 = px.treemap(
        names=area_counts.index,
        parents=[''] * len(area_counts),
        values=area_counts.values,
        title="Area Visualization"
    )

    # Display the Plotly figure using Streamlit's Plotly support
    st.plotly_chart(fig1)

    # Calculate area frequencies
    station_counts = df['station name'].value_counts()

    # Create a plotly map
    fig2 = px.treemap(
        names=station_counts.index,
        parents=[''] * len(station_counts),
        values=station_counts.values,
        title="Station Visualization"
    )

    # Display the Plotly figure using Streamlit's Plotly support
    st.plotly_chart(fig2)

    # Calculate area frequencies
    lines_counts = df['lines'].value_counts()

    # Create a Plotly Treemap
    fig3 = px.treemap(
        names=lines_counts.index,
        parents=[''] * len(lines_counts),
        values=lines_counts.values,
        title="Lines Visualization"
    )

    # Display the Plotly figure using Streamlit's Plotly support
    st.plotly_chart(fig3)



    # while True:
    #     current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    #     output.text(f"Last Update: {current_time}")
    #     time.sleep(10)


if __name__ == "__main__":
    main()
