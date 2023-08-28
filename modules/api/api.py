import pandas as pd
from fastapi import FastAPI
import folium

app = FastAPI()


@app.get("/alert")
def alarm(
    alert_datetime: str,
    alert_longitude: float,
    alert_latitude: float,
    alert_station: str,
    alert_direction: str,
):
    # Implement your alert functionality here
    # You should return some meaningful data as a response
    alert_info = {"message": "Alert received and processed"}
    return alert_info


@app.get("/")
def get_map():
    # Create a basic Folium map
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

    # Get the HTML representation of the map
    map_html = m.get_root().render()

    # Return the HTML directly as a response
    return map_html
