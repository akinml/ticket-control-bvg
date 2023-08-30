import streamlit as st
import pandas as pd
import time
import random
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

public_stations = pd.read_csv('datanew_map2.csv')







def main():
    lat_list, lon_list = generate_random_coordinates_list()
    data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    berlin_df = pd.DataFrame(data)
    datetimenow = time.strftime("%H:%M:%S")
    st.title(f"BVG Controllers Berlin - {datetimenow}")
    st.map(data= public_stations,zoom=10, color="color", size=50)

    # Add a refresh button
    st.table(berlin_df)
    output = st.empty()

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)




if __name__ == "__main__":
    main()
