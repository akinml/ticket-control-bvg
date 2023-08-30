import streamlit as st
import pandas as pd
import time
import plotly.express as px
from modules.rand_data import generate_random_coordinates_list
from modules.telegramm_update import get_update


# Define a CSS class for custom styling
def main():
    lat_list, lon_list = generate_random_coordinates_list()
    data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    df = pd.DataFrame(data)
    datetimenow = time.strftime("%H:%M:%S")
    st.title(f"BVG Controllers Berlin - {datetimenow}")

    px.set_mapbox_access_token(open("access.mapbox_token").read())
    fig = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=10,
    )

    st.plotly_chart(fig, use_container_width=False, width=800)
    st.table(df.style.set_table_attributes('class="custom-table"'))

    output = st.empty()

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)


if __name__ == "__main__":
    main()
