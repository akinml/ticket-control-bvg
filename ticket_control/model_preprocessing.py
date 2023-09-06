import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import holidays
from utils import bezirke


def get_data():
    data = pd.read_csv("../data/preprocessed_database_telegram_git.csv")
    data = data.copy()
    # Fixing date to Datetime and setting it as an index
    data["date"] = pd.to_datetime(data["date"])
    data = data.set_index("date")
    data = get_time(data)
    data = cyclic_features(data)
    data = add_holiday(data)
    data = covid(data)
    data = get_bins(data)
    data = get_bezirke(data)
    # Splitting the test and train data
    train_size = 0.7
    index = round(train_size * data.shape[0])
    data_train = data.iloc[:index]
    data_test = data.iloc[index:]
    # Applying the count matrix
    data_train = count_matrix(data_train)
    data_test = count_matrix(data_test)
    # OneHotEncoding Bezirke
    encoder = OneHotEncoder(sparse=False)
    encoder.fit(data_train[["bezirk"]])
    data_train[encoder.get_feature_names_out()] = encoder.transform(
        data_train[["bezirk"]]
    )
    data_test[encoder.get_feature_names_out()] = encoder.transform(
        data_test[["bezirk"]]
    )
    # drop duplicates
    data_train = data_train.drop_duplicates(subset=["bezirk", "bins"])
    data_test = data_test.drop_duplicates(subset=["bezirk", "bins"])
    # encode_target
    X_train = data_train.drop(
        columns=[
            "station_key",
            "text",
            "station name",
            "lines",
            "area",
            "target",
            "bins",
            "bezirk",
            "month",
            "weekday",
            "hour",
        ]
    )
    y_train = data_train["target"].map(encode_target)
    X_test = data_test.drop(
        columns=[
            "station_key",
            "text",
            "station name",
            "lines",
            "area",
            "target",
            "bins",
            "bezirk",
            "month",
            "weekday",
            "hour",
        ]
    )
    y_test = data_test["target"].map(encode_target)
    # end
    return X_train, y_train, X_test, y_test


def get_time(data):
    # Year
    # Creating a Year column
    data["year"] = data.index
    data["year"] = pd.to_datetime(data["year"])
    data["year"] = data["year"].dt.year
    # Months
    # Creating a Month column
    data["month"] = data.index
    data["month"] = pd.to_datetime(data["month"])
    data["month"] = data["month"].dt.month
    # Weekdays
    # Creating a Weekday column
    data["weekday"] = data.index
    data["weekday"] = pd.to_datetime(data["weekday"])
    data["weekday"] = data["weekday"].dt.weekday
    # Hours of the day
    data["hour"] = data.index
    data["hour"] = pd.to_datetime(data["hour"])
    data["hour"] = data["hour"].dt.hour
    return data


def cyclic_features(data):
    ### Encoding Cyclical Features
    data["hour_sin"] = np.sin(2 * np.pi * data["hour"] / 24.0)
    data["hour_cos"] = np.cos(2 * np.pi * data["hour"] / 24.0)

    data["weekday_sin"] = np.sin(2 * np.pi * data["weekday"] / 7.0)
    data["weekday_cos"] = np.cos(2 * np.pi * data["weekday"] / 7.0)

    data["month_sin"] = np.sin(2 * np.pi * data["month"] / 12.0)
    data["month_cos"] = np.cos(2 * np.pi * data["month"] / 12.0)
    return data


def add_holiday(data):
    # Adding Holidays
    de_holiday_list = []
    for holiday in holidays.Germany(
        years=[2018, 2019, 2020, 2021, 2022, 2023, 2024]
    ).items():
        de_holiday_list.append(holiday)
    de_holidays_df = pd.DataFrame(de_holiday_list, columns=["date", "holiday"])
    de_holidays_df["date"] = pd.to_datetime(de_holidays_df["date"])
    de_holidays_df["date"].dt.date
    holiday_str = list(map(str, list(de_holidays_df["date"].dt.date)))

    def find_holiday(date: dt.datetime):
        date_str = str(date.date())
        if date_str in holiday_str:
            return 1
        else:
            return 0

    data["holiday"] = data.index.map(find_holiday)
    return data


def covid(data):
    covid_lockdown1_start = dt.date(2020, 3, 23)
    covid_lockdown1_end = dt.date(2020, 6, 15)

    covid_lockdown2_start = dt.date(2020, 10, 2)
    covid_lockdown2_end = dt.date(2021, 4, 27)
    data["covid"] = data.index.date

    def covid_lockdown(some_day):
        if (some_day >= covid_lockdown1_start) & (some_day <= covid_lockdown1_end):
            return 1
        elif (some_day >= covid_lockdown2_start) & (some_day <= covid_lockdown2_end):
            return 1
        return 0

    data["covid"] = data["covid"].map(covid_lockdown)

    return data


def get_bins(data):
    n_bin = data.resample("h").count().shape[0]
    data["bins"] = pd.cut(data.index, bins=n_bin).astype("str")
    return data


def get_bezirke(data):
    def area_to_bezirk(some_area):
        for key, values in bezirke.items():
            if some_area in values:
                return key
        return "Brandenburg"

    data["bezirk"] = data["area"].map(area_to_bezirk)
    return data


def count_matrix(data):
    count_matrix = (
        data.groupby(["bezirk", "bins"])["station_key"].count().unstack().fillna(0)
    )

    def get_cluster_count(bezirk, time_bin, timestep_shift, count_matrix):
        return count_matrix.shift(periods=timestep_shift, axis=1)[time_bin][bezirk]

    def add_clusters_count(df, count_matrix):
        df["target"] = df.apply(
            lambda df: get_cluster_count(df["bezirk"], df["bins"], -1, count_matrix),
            axis=1,
        )
        df["local_0"] = df.apply(
            lambda df: get_cluster_count(df["bezirk"], df["bins"], 0, count_matrix),
            axis=1,
        )
        df["local_1"] = df.apply(
            lambda df: get_cluster_count(df["bezirk"], df["bins"], 1, count_matrix),
            axis=1,
        )
        df["local_2"] = df.apply(
            lambda df: get_cluster_count(df["bezirk"], df["bins"], 2, count_matrix),
            axis=1,
        )
        return df

    df = add_clusters_count(data, count_matrix).dropna()
    return df


def encode_target(some_y):
    if some_y == 0:
        return 0
    return 1


def get_station_latlon(station):
    data = pd.read_csv("../data/s_u_stations_fixed_with_keys_20230830.csv")
    data = data.copy()
    row = data[data["station name"] == station]
    return row[["area", "latitude", "longitude"]].values


def preprocess_input(station):
    X_pred = pd.DataFrame({"date": [dt.datetime.now()], "station name": [station]})
    X_pred = X_pred.set_index("date")
    X_pred[["area", "latitude", "longitude"]] = get_station_latlon(station)
    X_pred = get_time(X_pred)
    X_pred = cyclic_features(X_pred)
    X_pred = add_holiday(X_pred)
    X_pred = covid(X_pred)
    X_pred = get_bezirke(X_pred)
    # OneHotEncoding Bezirke
    encoder = OneHotEncoder(sparse=False, categories=[list(bezirke.keys())])
    X_pred[encoder.get_feature_names_out()] = encoder.fit_transform(X_pred[["bezirk"]])
    X_pred[
        ["local_0", "local_1", "local_2"]
    ] = 5  ### TODO: this is dummy, use actual values
    # drpping columns
    X_pred = X_pred.drop(
        columns=["station name", "area", "bezirk", "month", "weekday", "hour"]
    )
    return X_pred
