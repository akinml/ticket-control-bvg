import pandas as pd
from pathlib import Path

path_to_main = Path(__file__).parent.parent

<<<<<<< HEAD

def update_station_colors(reports, stations, from_date, to_date):
    # Read data from CSV files
    reports = str(path_to_main) + "data/preprocessed_database_telegram.csv"
    stations = str(path_to_main) + "data/station_bahn1.csv"
    # Filter reports based on date
    reports_filtered = reports[
        (reports["date"] >= from_date) & (reports["date"] <= to_date)
    ]
    # Loop through unique station names in the filtered reports
    for report_station in reports_filtered["station name"].unique():
        # Update the 'color' column for matching stations to '#FF0000'
        stations.loc[stations["station name"] == report_station, "color"] = "#FF0000"
=======
def update_station_colors(reports, stations, from_date, to_date):
    # Read data from CSV files
    reports = str(path_to_main) + 'data/preprocessed_database_telegram.csv'
    stations = str(path_to_main) + 'data/station_bahn1.csv'




    # Filter reports based on date
    reports_filtered = reports[(reports['date'] >= from_date) & (reports['date'] <= to_date)]

    # Loop through unique station names in the filtered reports
    for report_station in reports_filtered['station name'].unique():
        # Update the 'color' column for matching stations to '#FF0000'
        stations.loc[stations['station name'] == report_station, 'color'] = '#FF0000'
>>>>>>> cee7723 (Tried to create a legend for streamlit but it's not very pretty)

    return stations
