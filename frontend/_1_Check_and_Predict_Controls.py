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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ticket_control.pipeline import pipeline
from pathlib import Path
from pages._2_View_Statistics import page_2_control_statistics

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
data1 = pd.read_csv(str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv")


path_to_main = Path(__file__).parent


def update_station_colors(from_date: str, to_date: str) -> pd.DataFrame:
    """This functions returns the Dataframe for the Map of the Streamlit App.
    It takes the input preprocessed Database that is filtered on user input date
    range and returns the reports form the relevant time period.
    All reported stations will appear red on the Map.
    The from and to dateformat ,e.g., from_date='2023-08-30 11:55:00'
    to_date='2023-08-30 12:01:00'."""
    # Read data from CSV files
    reports = pd.read_csv(
        str(path_to_data) + "/preprocessed_database_telegram.csv"
    )
    stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")
    # Filter reports based on date
    reports = reports.copy()
    stations = stations.copy()
    reports_filtered = reports[
        (reports["date"] >= from_date) & (reports["date"] <= to_date)
    ]
    # Loop through unique station names in the filtered reports
    for report_station in reports_filtered["station name"].unique():
        # Update the 'color' column for matching stations to '#FF0000'
        stations.loc[stations["station name"] == report_station, "color"] = "#FF0000"
    return stations


# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
# Api for reporting Data to Backend
app = FastAPI()
# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# If someone sends a report through our streamlit app, this API will save it to our preprocessed dataframe


@app.get("/report")
def save_report(report_station: str):
    print("Receiving a new Alarm!:rotating_light:")
    report_station = report_station
    report_datetime = pd.Timestamp.now()
    report_dict = {
        "sender": str(report_datetime)[0:19],
        "group": "website",
        "text": report_station,
        "date": str(report_datetime)[0:19],
    }
    return report_dict

# setting config to "wide" so that charts and other elements are properly displayed
st.set_page_config(layout="wide")

# DEFINING THE APP INTERFACE AND ANALYSIS
def page_1_landing_page():
    # LOADING DATAFRAMES FOR APP
    data1 = pd.read_csv(str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv")
    reports = pd.read_csv(
        str(path_to_data) + "/preprocessed_database_telegram.csv"
    )
    stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")

    st.title("Welcome to BVG Controls:wave:")

    # Streamlit app
    st.title("Predict controls")

    # Select Stations
    selected_options = st.selectbox("Select station:", data1["station name"])

    # Create a slider widget and store the selected value in a variable
    min_minutes, max_minutes = st.select_slider(
        "Select a time range in minutes",
        options=list(range(0, 61)),  # List of options from 0 to 60 minutes
        value=(0, 30),  # Default selected range from 0 to 60 minutes
    )
    min_timedelta = timedelta(minutes=min_minutes)
    max_timedelta = timedelta(minutes=max_minutes)

    selected_station_report = st.selectbox("Select Station:", data1["station name"])

    # CODE BLOCK REPORT
    if st.button("Report BVG Controller. :cop:"):
        response = requests.get(
            f"http://0.0.0.0:8000/report?report_station={selected_station_report}"
        )

        if response.status_code == 200:
            st.write("Report Sent!:ok_hand::heart::heart_eyes:")
            # Concatenate the report data with preprocessed_database_telegram
            report_data = response.json()
            report_df = pd.DataFrame([report_data])
            database_telegram = pd.read_csv(str(path_to_data) + "/database_telegram.csv")
            database_telegram = pd.concat([database_telegram, report_df])
            database_telegram[["group", "sender", "text", "date"]].to_csv(
                "data/database_telegram.csv"
            )
            pipeline()
            df_filtered_map = update_station_colors(
                from_date="2023-08-28 12:28:00",  # Insert Sliders Dates here!
                to_date="2023-10-29 10:28:00",  # Insert Sliders Dates here!
            )
        else:
            st.write("Failed to send the report. :rotating_light:")

    else:
        st.write("Awaiting Report. :rotating_light:")

    datetimenow = time.strftime("%H:%M:%S")

    # st.map(data=public_stations, zoom=10, color="color", size=50)

    # Call Function to show Map with alerts:
    df_filtered_map = update_station_colors(
        from_date=(datetime.now() - max_timedelta).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Insert Sliders Dates here!
        to_date=(datetime.now() - min_timedelta).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Insert Sliders Dates here!
    )

    st.map(data=df_filtered_map, zoom=10, color="color", size=50)
    image = Image.open(str(path_to_data) + "/Screenshot 2023-09-04 at 5.07.42 PM.png")
    st.image(image, caption="Legend", width=700)

    # MAP WITH TIME
    datetimenow = time.strftime("%H:%M:%S")


page_1_landing_page()