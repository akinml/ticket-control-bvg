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
from pathlib import Path

st_path_to_data = st.secrets.get('PATH_TO_DATA', None)
st.write(st_path_to_data)
if st_path_to_data is not None:
    path_to_data = st_path_to_data
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
#st.set_page_config(layout="wide")

# DEFINING THE APP INTERFACE AND ANALYSIS
def page_1_landing_page():
    # LOADING DATAFRAMES FOR APP
    data1 = pd.read_csv(str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv")
    reports = pd.read_csv(
        str(path_to_data) + "/preprocessed_database_telegram.csv"
    )
    stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")

    st.title("Welcome to BVG Controls:wave:")

    # ###
    # Prediction: RandomForestClassifier, output 0 or 1 > control / no control
    st.header("Predict controls", divider='rainbow')

    # Select Stations
    station = st.selectbox("Select station:", data1["station name"])

    # Output of the model:
    if st.button("Predict", type="primary"):
        response = requests.get(
            f"https://api-fjupsu3szq-lz.a.run.app/predict?station={station}"
        )
        reply = response.json()

        # TODO: add probability of prediction
        #proba = reply["Probability"]
        if reply["control"] == 1:
            st.error('Control is predicted for the selected station in the next hour')
            #st.caption('probability of this prediction is: ', proba)
        else:
            st.success('No control predicted for the selected station in the next hour')
            #st.caption('probability of this prediction is: ', proba)

   # ###
    # Report control
    st.header("Report control", divider='rainbow')

    selected_station_report = st.selectbox("Select Station:", data1["station name"])

    # CODE BLOCK REPORT
    if st.button("Report BVG Controller. :cop:"):
        response = requests.get(
            f"https://api-fjupsu3szq-lz.a.run.app/report?report_station={selected_station_report}"
        )

        if response.status_code == 200:
            st.write("Report Sent!:ok_hand::heart::heart_eyes:")
        else:
            st.write("Failed to send the report. :rotating_light:")

    else:
        st.write("Awaiting Report. :rotating_light:")

    datetimenow = time.strftime("%H:%M:%S")

    # st.map(data=public_stations, zoom=10, color="color", size=50)


    # Ticket controllers detected in last hour
    st.header("Latest update on ticket controls in Berlin", divider='rainbow')
    # Create a slider widget and store the selected value in a variable
    min_minutes, max_minutes = st.select_slider(
        "Select a time range in minutes",
        options=list(range(0, 61)),  # List of options from 0 to 60 minutes
        value=(0, 30),  # Default selected range from 0 to 60 minutes
    )
    min_timedelta = timedelta(minutes=min_minutes)
    max_timedelta = timedelta(minutes=max_minutes)

    #selected_station_report = st.selectbox("Select Station:", data1["station name"])



    # Call Function to show Map with alerts:
    df_filtered_map = update_station_colors(
        from_date=(datetime.now() - max_timedelta).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Insert Sliders Dates here!
        to_date=(datetime.now() - min_timedelta).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Insert Sliders Dates here!
    )



    #Legend

    column1, column2 = st.columns([8.5, 0.5])
    with column1:
        st.map(data=df_filtered_map, zoom=10, color="color", size=50)

    with column2:
        S41 = Image.open('../data/imgs/s41.png')
        st.image(S41, width=30)
        S5 = Image.open('../data/imgs/s5.png')
        st.image(S5, width=30)
        S7 = Image.open('../data/imgs/s7.png')
        st.image(S7, width=30)
        S8 = Image.open('../data/imgs/s8.png')
        st.image(S8, width=30)
        S9 = Image.open('../data/imgs/s9.png')
        st.image(S9, width=30)
        S25 = Image.open('../data/imgs/s25.png')
        st.image(S25, width=30)
        S47 = Image.open('../data/imgs/s47.png')
        st.image(S47, width=30)
        S75 = Image.open('../data/imgs/s75.png')
        st.image(S75, width=30)
        U1 = Image.open('../data/imgs/U1.png')
        st.image(U1, width=30)
        U2 = Image.open('../data/imgs/U2.png')
        st.image(U2, width=30)
        U3 = Image.open('../data/imgs/U3.png')
        st.image(U3, width=30)
        U4 = Image.open('../data/imgs/U4.png')
        st.image(U4, width=30)
        U5 = Image.open('../data/imgs/U5.png')
        st.image(U5, width=30)
        U6 = Image.open('../data/imgs/U6.png')
        st.image(U1, width=30)
        U7 = Image.open('../data/imgs/U7.png')
        st.image(U7, width=30)
        U8 = Image.open('../data/imgs/U8.png')
        st.image(U8, width=30)
        U9 = Image.open('../data/imgs/U9.png')
        st.image(U9, width=30)

    col0, col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1, 1])
    with col1:
        reported_station = Image.open('../data/imgs/red_dot.png')
        st.image(reported_station, width=60)
        st.write("Reported Station")
    with col2:
        u_bahn_hub = Image.open('../data/imgs/green_dot.png')
        st.image(u_bahn_hub, width=60)
        st.write("U-Bahn Intersection")
    with col3:
        s_bahn_hub = Image.open('../data/imgs/teal_dot.png')
        st.image(s_bahn_hub, width=60)
        st.write("S-Bahn Intersection")
    with col4:
        u_and_s_bahn_hub = Image.open('../data/imgs/yellow_dot.png')
        st.image(u_and_s_bahn_hub, width=60)
        st.write("S- and U-Bahn Intersection")
    hide_img_fs = '''
            <style>
            button[title="View fullscreen"]{
            visibility: hidden;}
            </style>
            '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)













    #image = Image.open(str(path_to_data) + "/Screenshot 2023-09-04 at 5.07.42 PM.png")
    #st.image(image, caption="Legend", width=700)

    # MAP WITH TIME
    datetimenow = time.strftime("%H:%M:%S")


page_1_landing_page()
