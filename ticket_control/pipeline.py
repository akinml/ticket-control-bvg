from ticket_control.data_preprocessing import data_preprocessing
from ticket_control.fuzz_flow import *
import pandas as pd
from params import path_to_data

df_station_mapping = pd.read_csv(
    str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv"
)

# 1. Step in our preprocessing: Cleaning the Strings
raw_data = pd.read_csv("data/database_telegram.csv")
df_for_fuzzy_matching = data_preprocessing(raw_data)

# 2. Step in our preprocessing Doing the Fuzzy Matching with the output of Step 1 and the station mapping df
df_station_mapping = create_station_to_line_df(df_station_mapping=df_station_mapping)
output_df = fuzz_flow(
    df_for_fuzzy_matching=df_for_fuzzy_matching, df_station_mapping=df_station_mapping
)

output_df.to_csv(str(path_to_data) + "/preprocessed_database_telegram.csv")
