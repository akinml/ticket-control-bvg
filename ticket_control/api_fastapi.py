import pandas as pd
import pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
from model_preprocessing import *
from ticket_control.utils import bezirke
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# $WIPE_BEGIN
# 💡 Preload the model to accelerate the predictions
# We want to avoid loading the heavy Deep Learning model from MLflow at each `get("/predict")`
# The trick is to load the model in memory when the Uvicorn server starts
# and then store the model in an `app.state.model` global variable, accessible across all routes!
# This will prove very useful for the Demo Day
app.state.model = pickle.load(open('model.pkl', 'rb'))


# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(
        station: str
    ):      # 1

# 1. user inputs district and station
# 2. one hot encode district
# 3. station -> lat, lon
# 4. get current time -> hour, weekday, year, month
# # #  Chris (dummy for now) > 5. calculate local_0, local_1, local_2 from live data of past hours

# feature_vector
# [(ohe_district), local_0, local_1, local_2, year, weekday, month, hour, lat, lon]
# model.predict(feature_vector) -> # of controls (regression)
# model.predict(feature_vector) -> 0/1 (with probability) (classification) !!!
    X_pred=preprocess_input(station)
    model = app.state.model
    assert model is not None

    y_pred = model.predict(X_pred[model.feature_names_in_])

    # ⚠️ fastapi only accepts simple Python data types as a return value
    # among them dict, list, str, int, float, bool
    # in order to be able to convert the api response to JSON
    return dict(control=float(y_pred))


@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
