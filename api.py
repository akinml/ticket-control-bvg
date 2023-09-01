import streamlit as st
import pandas as pd
import requests
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
        "sender": "unknown",
        "group": "website",
        "text": report_station,
        "date": report_datetime,
    }
    return report_dict


data1 = pd.read_csv("data/s_u_stations_fixed_with_keys_20230830.csv")
database_telegram = pd.read_csv("data/database_telegram.csv")


def main():
    data1 = pd.read_csv("data/s_u_stations_fixed_with_keys_20230830.csv")
    database_telegram = pd.read_csv("data/database_telegram.csv")

    selected_option = st.selectbox("Select Station(s):", data1["station name"])
    if st.button("Report BVG Controller. 👮"):
        response = requests.get(
            f"http://0.0.0.0:8000/report?report_station={selected_option}"
        )

        if response.status_code == 200:
            st.write("Report Sent!👌❤️😍")
            # Concatenate the report data with preprocessed_database_telegram
            report_data = response.json()
            report_df = pd.DataFrame([report_data])
            database_telegram = pd.concat([database_telegram, report_df])
            print(database_telegram)
            database_telegram.to_csv("data/database_telegram.csv")
        else:
            st.write("Failed to send the report. 🚨")

    else:
        st.write("Awaiting Report. 🚨")


if __name__ == "__main__":
    main()
