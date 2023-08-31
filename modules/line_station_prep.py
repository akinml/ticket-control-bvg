### all of the imports go into requirements!!!
import pandas as pd
import numpy as np
import string
from datetime import timedelta


def line_station_prep():
    # Load your existing database into a DataFrame
    df = pd.read_csv('/home/yannik/ticket-control-bvg/data/s_u_stations_fixed_with_keys.csv')  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    df = df.copy()


    # create a dictionary where U/S bahn line names are the keys and the respective stations are the values incl. lat & lon
    output = {'station': [], 'line': [],'latitude':[], 'longitude': []}
    for idx,row in df.iterrows():
        line_split = row['lines'].split(', ')
        for i in line_split:
            output['station'].append(row['keys'])
            output['latitude'].append(row['latitude'])
            output['longitude'].append(row['longitude'])
            output['line'].append(i)
    station_to_line = pd.DataFrame(output)

    station_to_line = station_to_line.drop_duplicates()

    return station_to_line
