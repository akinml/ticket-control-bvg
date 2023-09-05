from prefect import flow
from ticket_control.data_preprocessing import *
from ticket_control.fuzz_flow import *
from ticket_control.params import path_to_data
import pandas as pd
from prefect_github import GitHubCredentials
from prefect.filesystems import GitHub
from prefect_github.repository import GitHubRepository
from pathlib import Path

github_repository_block = GitHubRepository.load("github-repo2")
github_block = GitHub.load("github-repo")
github_credentials_block = GitHubCredentials.load("github")

path_main = Path(__file__).parent
path_to_data = path_main / "data/"


def pipeline(raw_data):
    print("\033[1;32m 👷Pipeline Started! 👷\n")
    df_station_mapping = pd.read_csv(
        str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv"
    )
    # 1. Step in our preprocessing: Cleaning the Strings
    # Reducing the number of rows to be preprocessed significantly speeds up the process. Going from ~1:30 Minutes to below 2 secs.
    raw_data = raw_data.iloc[-1000:, :]
    df_for_fuzzy_matching = data_preprocessing(raw_data)
    # 2. Step in our preprocessing Doing the Fuzzy Matching with the output of Step 1 and the station mapping df
    df_station_mapping = create_station_to_line_df(
        df_station_mapping=df_station_mapping
    )
    update_df = fuzz_flow(
        df_for_fuzzy_matching=df_for_fuzzy_matching, station_to_line=df_station_mapping
    )
    update_df.reset_index(inplace=True)
    output_df = update_df[
        [
            "date",
            "station_key",
            "text",
            "station name",
            "lines",
            "area",
            "latitude",
            "longitude",
        ]
    ]
    print("\n 👷Pipeline Completed!👷")
    return output_df


if __name__ == "__main__":
    pipeline(raw_data)
