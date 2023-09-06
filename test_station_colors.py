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
from pipeline import pipeline
from pathlib import Path
from ticket_control.model_preprocessing import *
from ticket_control.big_query_download_processed import download_big_query_processed
from ticket_control.big_query_upload_processed import upload_big_query_processed

path_to_main = Path(__file__).parent
public_stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")
data1 = pd.read_csv(str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv")
stations = pd.read_csv(str(path_to_main) + "/data/datanew_map2.csv")


def update_station_colors(from_date: str, to_date: str) -> pd.DataFrame:
    """This functions returns the Dataframe for the Map of the Streamlit App.
    It takes the input preprocessed Database that is filtered on user input date
    range and returns the reports form the relevant time period.
    All reported stations will appear red on the Map.
    The from and to dateformat ,e.g., from_date='2023-08-30 11:55:00'
    to_date='2023-08-30 12:01:00'."""
    # Read data from CSV files
    reports = download_big_query_processed()
    stations = pd.read_csv(str(path_to_main) + "/data/final_map.csv")
    # Filter reports based on date
    reports = reports.copy()
    stations = stations.copy()
    reports["date"] = reports["date"].astype(str).str.strip("+00:00").str[0:16]
    reports["date"] = pd.to_datetime(reports["date"], errors="coerce")

    reports_filtered = reports[
        (reports["date"] >= from_date) & (reports["date"] <= to_date)
    ]
    print(f"reports filtered: {reports_filtered}")
    # Loop through unique station names in the filtered reports
    for report_station in reports_filtered["station_key"].unique():
        print(report_station)
        # Update the 'color' column for matching stations to '#FF0000'
        stations.loc[stations["keys"] == report_station, "color"] = "#FF0000"
    print(stations[stations["color"] == "#FF0000"])
    return stations


if __name__ == "__main__":
    update_station_colors("2010-08-28 12:28:00", "2028-08-28 12:28:00")
