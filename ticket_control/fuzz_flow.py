import pandas as pd
import numpy as np
from datetime import timedelta
from thefuzz import process
from thefuzz import fuzz
import re
from ticket_control.data_preprocessing import data_preprocessing
from ticket_control.params import path_to_data
import matplotlib.pyplot as plt


# Chris Notes: Name your variables after the type of the variable and their purpose in the pipeline.
df_station_mapping = pd.read_csv(
    str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv"
)  # Replace with the path to your database file


# Christ Notes: Better to define the function outside of the function. We want to create individual units of code that are testable and serve a single purpose.
def create_station_to_line_df(df_station_mapping: pd.DataFrame):
    # df = pd.read_csv('s_u_stations_fixed_with_keys_20230830.csv')  # Replace with the path to your database file
    df = df_station_mapping.copy()

    # create a dictionary where U/S bahn line names are the keys and the respective stations are the values incl. lat & lon
    output = {"station_key": [], "line": []}
    for idx, row in df.iterrows():
        line_split = row["lines"].split(", ")
        for i in line_split:
            output["station_key"].append(row["keys"])
            output["line"].append(i)
    station_to_line = pd.DataFrame(output)
    station_to_line = station_to_line.drop_duplicates()
    return station_to_line


def fuzz_flow(df_for_fuzzy_matching: pd.DataFrame, station_to_line: pd.DataFrame):
    # Chris Notes: Always write a short Docstring for your function, describe what it does and what is input and outputs are.
    """Docstring for this function, This function does x,y,z..."""
    # Chris Notes: We want to separate the individual cleaning steps into different functions and states. This makes it easier to track down errors.
    # Better to take the input from yannik and use it as a direct input into your function than to call his function agian.
    data3 = df_for_fuzzy_matching
    data3 = data3.copy()

    # Load STATIONS DATAFRAME
    station_to_line = station_to_line.copy()

    df = pd.read_csv(str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv")

    lines_un = list(station_to_line["line"].unique())
    stations_full = list(df["keys"].values)

    # Chris Notes: Better to be defined outside of function.
    def identify_station_precise(
        some_string, confidence_first=80, confidence_second=90
    ):
        res1 = None
        res2 = None
        if some_string[1][1] > confidence_second:
            res1 = some_string[1][0]
            return some_string[0][0], some_string[1][0]
        elif (
            some_string[0][1] > confidence_first
        ):  # try 79 or 89 and other, better less lines but better quality
            return some_string[0][0]
        return None

    # Chris Notes: Better to be defined outside of function.
    def station_finder(some_string):
        for line in lines_un:
            matches = re.search(r"{line}[^0-9]".format(line=line.lower()), some_string)
            if matches is not None:
                stations = list(
                    station_to_line[station_to_line["line"] == line]["station_key"]
                )
                out = process.extract(
                    some_string, stations, limit=2, scorer=fuzz.partial_ratio
                )
                return identify_station_precise(out, 70, 70)
        out = process.extract(
            some_string, stations_full, limit=2, scorer=fuzz.partial_ratio
        )
        return identify_station_precise(out)

    df_chat = data3[["date"]]

    df_chat["station_key"] = data3["text"].map(station_finder)
    df_chat["text"] = data3["text"]
    df_chat.dropna(subset="station_key", inplace=True)
    full_df = df_chat.merge(df, left_on="station_key", right_on="keys")
    full_df.drop(columns="Unnamed: 0", inplace=True)
    full_df.drop(columns="keys", inplace=True)
    full_df = full_df.sort_index(ascending=True)
    return full_df
