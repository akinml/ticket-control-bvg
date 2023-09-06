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
from ticket_control.big_query_upload_raw import upload_big_query_raw
from ticket_control.params import path_to_data
from streamlit_lottie import st_lottie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
<<<<<<< HEAD
from ticket_control.pipeline import pipeline
=======
from pipeline import pipeline
>>>>>>> eb2c52c76584342a1dcb0df220d9d436d0a98cd0
from pathlib import Path
from ticket_control.model_preprocessing import *
from ticket_control.big_query_download_processed import download_big_query_processed
from ticket_control.big_query_upload_processed import upload_big_query_processed

path_to_main = Path(__file__).parent
public_stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")
data1 = pd.read_csv(str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv")
# processed_data = download_big_query_processed()
stations = pd.read_csv(str(path_to_main) + "/data/datanew_map2.csv")


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
    report_datetime = pd.Timestamp.now()
    report_dict = {
        "sender": report_datetime,
        "group": "website",
        "text": report_station,
        "date": report_datetime,
    }
    report_df = pd.DataFrame([report_dict])
    upload_big_query_raw(report_df)
    return report_df


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
