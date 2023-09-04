import streamlit as st
import pandas as pd
import time
import requests
from pipeline import pipeline
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    print("Receiving a new Alarm!🚨")
    report_station = report_station
    report_datetime = pd.Timestamp.now()
    report_dict = {
        "sender": str(report_datetime)[0:19],
        "group": "website",
        "text": report_station,
        "date": str(report_datetime)[0:19],
    }
    return report_dict


# DEFINING THE APP INTERFACE AND ANALYSIS
def main():
    # LOADING DATAFRAMES FOR APP
    data1 = pd.read_csv("data/s_u_stations_fixed_with_keys_20230830.csv")
    reports = pd.read_csv(
        str(path_to_main) + "/data/preprocessed_database_telegram.csv"
    )
    stations = pd.read_csv(str(path_to_main) + "/data/datanew_map2.csv")

    # Call Function to show Map with alerts:
    df_filtered_map = update_station_colors(
        from_date="2023-08-28 12:28:00",  # Insert Sliders Dates here!
        to_date="2023-10-29 10:28:00",  # Insert Sliders Dates here!
    )

    # MAP WITH TIME
    datetimenow = time.strftime("%H:%M:%S")
    st.title(f"BVG Controllers Berlin - {datetimenow}")
    selected_station_report = st.selectbox("Select Station(s):", data1["station name"])
    # CODE BLOCK REPORT
    if st.button("Report BVG Controller. 👮"):
        response = requests.get(
            f"http://0.0.0.0:8000/report?report_station={selected_station_report}"
        )

        if response.status_code == 200:
            st.write("Report Sent!👌❤️😍")
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
            st.write("Failed to send the report. 🚨")

    else:
        st.write("Awaiting Report. 🚨")

    st.map(data=df_filtered_map, zoom=10, color="color", size=50)

    start_color, end_color = st.select_slider(
        "Select a range of color wavelength",
        options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
        value=("red", "blue"),
    )

    # Minutes slider
    # st.slider('Minutes', 0, 60, 0)

    # Select day of week
    option = st.selectbox(
        "Day of week",
        (
            "None",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ),
    )
    st.write("You selected:", option)

    # Select month
    option1 = st.selectbox(
        "Month",
        (
            "None",
            "January",
            "Febraury",
            "March",
            "April",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ),
    )
    st.write("You selected:", option1)

    # Date range
    five_years_ago = datetime.today() - timedelta(days=5 * 365)

    date_range = st.date_input(
        "Select your date range:",
        value=(datetime.today(), datetime.today() + timedelta(days=0)),
        min_value=five_years_ago,
        max_value=datetime.today(),
    )

    st.write("Your date range is:", date_range)

    # Select Stations
    selected_options = st.multiselect("Select Station(s):", data1["station name"])
    st.write("You selected:", selected_options)

    # Add a refresh button
    st.table(berlin_df)
    output = st.empty()

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)


if __name__ == "__main__":
    main()
