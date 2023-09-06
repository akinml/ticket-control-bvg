import streamlit as st
import pandas as pd
import time
import random
import calendar
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
import plotly.figure_factory as ff
import pydeck as pdk

from datetime import datetime, timedelta, date
from ticket_control.params import path_to_data
from streamlit_lottie import st_lottie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ticket_control.pipeline import pipeline
from pathlib import Path
from ticket_control.model_preprocessing import *
from ticket_control.utils import bezirke
from sklearn.ensemble import RandomForestClassifier


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
        str(path_to_main) + "/data/preprocessed_database_telegram.csv"
    )
    stations = pd.read_csv(str(path_to_main) + "/data/datanew_map2.csv")
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


app.state.model = pickle.load(open("model.pkl", "rb"))


@app.get("/predict")
def predict(station: str):  # 1
    X_pred = preprocess_input(station)
    model = app.state.model
    assert model is not None

    y_pred = model.predict(X_pred[model.feature_names_in_])

    # ⚠️ fastapi only accepts simple Python data types as a return value
    # among them dict, list, str, int, float, bool
    # in order to be able to convert the api response to JSON
    return dict(control=float(y_pred))


# DEFINING THE APP INTERFACE AND ANALYSIS
def page_1_landing_page():
    # LOADING DATAFRAMES FOR APP
    data1 = pd.read_csv("data/s_u_stations_fixed_with_keys_20230830.csv")
    reports = pd.read_csv(
        str(path_to_main) + "/data/preprocessed_database_telegram.csv"
    )
    stations = pd.read_csv(str(path_to_main) + "/data/datanew_map2.csv")

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
            database_telegram = pd.read_csv("data/database_telegram.csv")
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
    # st.title(f"BVG Controllers Berlin - {datetimenow}")


# Load your existing database into a DataFrame
data = pd.read_csv(
    str(path_to_data) + "/preprocessed_database_telegram.csv"
)  # Replace with the path to your database file
# Notice the .copy() to copy the values
df = data.copy()
df["date"] = pd.to_datetime(df["date"])


# Page 2: Control Statistics
def page_2_control_prediction():
    # Load your existing database into a DataFrame
    data = pd.read_csv(
        "data/preprocessed_database_telegram.csv"
    )  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    # Streamlit app
    st.title("Data Analysis")
    df = data.copy()
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index)

    day = df.resample("d")["station_key"].count()

    st.write("Timeseries of daily controls")
    st.line_chart(day, color="#4048BF")

    week = df.resample("w")["station_key"].count()

    st.write("Timeseries of weekly controls")
    st.line_chart(week, color="#4048BF", use_container_width=True)

    # Streamlit app
    st.title("Data Analysis")

    st.write("Controls across Berlin")
    chart_data = df
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=52.507222,
                longitude=13.332500,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=chart_data,
                    get_position="[longitude, latitude]",
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position="[longitude, latitude]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )


# Page 3: Control Statistics
def page_3_control_statistics():
    # Streamlit app
    st.title("View statistics:mag_right:")

    # description
    min_date = df["date"].iloc[0]

    max_date = df["date"].iloc[-1]

    def load_animation(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    train_animation = load_animation(
        "https://lottie.host/aec64339-af7e-4713-95ad-2c11b57a4bc5/UdfXkvXrvL.json"
    )

    left_column, right_column = st.columns(2)

    with left_column:
        user_date_ranges = st.date_input(
            "Enter a range of two dates or leave blank",
            (min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        # User input for number of top items to display
        top_n_areas = st.selectbox(
            "Select the number of areas to display:", [10, 25, 50]
        )
        top_n_stations = st.selectbox(
            "Select the number of station names to display:", [10, 25, 50]
        )
        top_n_lines = st.selectbox(
            "Select the number of lines to display:", [10, 15, 25]
        )

    with right_column:
        st_lottie(train_animation, height=300, key="train_animation")

    # Arrange tables side by side
    st.write("Control Statistics:")
    col1, col2, col3 = st.columns([0.4, 0.5, 0.33], gap="medium")
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
        lines_counts = (
            df[
                (df["date"] >= pd.to_datetime(user_date_ranges[0]))
                & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
            ]["lines"]
            .str.split(", ")
            .explode()
            .value_counts()
        )
        st.write(lines_counts.head(top_n_lines))

    st.write("---")

    # Areas
    st.title("Areas, stations & lines visualization:tram:")

    st.write("Areas visualization")

    # Calculate area frequencies using data ranges selected by user
    area_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["area"].value_counts()

    # Create a plotly map
    fig1 = px.treemap(
        names=area_counts.index,
        parents=[""] * len(area_counts),
        values=area_counts.values,
    )

    # Display the figure
    st.plotly_chart(fig1)

    st.write("Stations visualization")

    # Calculate station frequencies
    station_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["station name"].value_counts()
    # Create a plotly map
    fig2 = px.treemap(
        names=station_counts.index,
        parents=[""] * len(station_counts),
        values=station_counts.values,
    )

    # Display the figure
    st.plotly_chart(fig2)

    st.write("Lines visualization")
    # Calculate lines frequencies
    lines_counts = (
        df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["lines"]
        .str.split(", ")
        .explode()
        .value_counts()
    )
    # Create a plotly mapp
    fig3 = px.treemap(
        names=lines_counts.index,
        parents=[""] * len(lines_counts),
        values=lines_counts.values,
    )

    # Display the figure
    st.plotly_chart(fig3)

    st.write("---")

    st.title("Time statistics:hourglass:")

    # Creating time columns for the differenct categories year, month, weekday, hour
    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["month"] = pd.DatetimeIndex(df["date"]).month
    df["day"] = pd.DatetimeIndex(df["date"]).weekday
    df["hour"] = df["date"].dt.hour

    # Naming the weekdays
    weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    # Applying the naming
    df["weekday"] = df["day"].map(weekdays)
    # Doing the same for months
    months = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Okt",
        11: "Nov",
        12: "Dec",
    }
    df["month_name"] = df["month"].map(months)

    weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    month_order = [
        "Jan",
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
        "Dec",
    ]

    st.write("Distribution of annual controls")
    fig4 = px.histogram(df, x="year", color_discrete_sequence=["#4048BF"], opacity=1)

    st.plotly_chart(fig4, use_container_width=False)

    st.write("Distribution of monthly controls")
    fig5 = px.histogram(
        df,
        x="month_name",
        color_discrete_sequence=["#4048BF"],
        opacity=1,
        category_orders={"month_name": month_order},
    )

    st.plotly_chart(fig5, use_container_width=False)

    st.write("Distribution of daily controls")
    fig6 = px.histogram(
        df,
        x="weekday",
        color_discrete_sequence=["#4048BF"],
        opacity=1,
        category_orders={"weekday": weekday_order},
    )

    st.plotly_chart(fig6, use_container_width=False)

    st.write("Distribution of hourly controls")
    fig7 = px.histogram(df, x="hour", color_discrete_sequence=["#4048BF"], opacity=1)

    st.plotly_chart(fig7, use_container_width=False)


# Main app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        (":one: Check Controls", ":two: Predict Controls", ":three: View Statistics"),
    )

    if page == ":one: Check Controls":
        page_1_landing_page()
    elif page == ":two: Predict Controls":
        page_2_control_prediction()
    elif page == ":three: View Statistics":
        page_3_control_statistics()


if __name__ == "__main__":
    main()
