import streamlit as st
import pandas as pd
import time
from modules.rand_data import generate_random_coordinates_list
from modules.telegramm_update import get_update

# Optional change Mapbox map to plotly Map. https://plotly.com/python/scattermapbox/

df_dummy = get_update()
output_df = preprocess(df_dummy)


def main():
    lat_list, lon_list = generate_random_coordinates_list()
    data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    berlin_df = pd.DataFrame(data)
    datetimenow = time.strftime("%H:%M:%S")
    st.title(f"BVG Controllers Berlin - {datetimenow}")
    st.map(berlin_df, zoom=10, color="#ffaa0088", size=50)
    # Add a refresh button
    st.table(berlin_df)
    output = st.empty()

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)


if __name__ == "__main__":
    main()
