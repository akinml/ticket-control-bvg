import pandas as pd
from ticket_control.data_preprocessing import data_preprocessing
from ticket_control.fuzz_flow import fuzz_flow

df = fuzz_flow(
    data_preprocessing(pd.read_csv("data/database_telegram.csv").iloc[0:1000])
)
print(df)
