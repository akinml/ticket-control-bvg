from prefect import flow
import streamlit as st
import pandas as pd
from prefect import flow

# Just add more points to the Dictionary to show more points:


@st.cache_data
@flow
def get_new_df():
    print("New Data loaded✅")


data = {"Location": ["Berlin"], "LAT": [52.5200], "LON": [13.4050]}
berlin_df = pd.DataFrame(data)
st.map(berlin_df, zoom=10)
st.table(berlin_df.head())

if __name__ == "__main__":
    get_new_df()
