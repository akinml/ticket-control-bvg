import streamlit as st
import pandas as pd
import time
import random
import calendar
from datetime import datetime, timedelta, date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Optional change Mapbox map to plotly Map. https://plotly.com/python/scattermapbox/
def generate_random_coordinates():
    min_lat, max_lat = 52.392166, 52.639004
    min_lon, max_lon = 13.215260, 13.770269
    random_lat = random.uniform(min_lat, max_lat)
    random_lon = random.uniform(min_lon, max_lon)
    return random_lat, random_lon


def generate_random_coordinates_list(num_samples=100):
    lat_list = []
    lon_list = []
    for x in range(num_samples):
        random_lat, random_lon = generate_random_coordinates()
        lat_list.append(random_lat)
        lon_list.append(random_lon)
    return lat_list, lon_list


public_stations = pd.read_csv("/home/yannik/ticket-control-bvg/data/datanew_map2.csv")
data1 = pd.read_csv(
    "/home/yannik/ticket-control-bvg/data/s_u_stations_fixed_with_keys_20230830.csv"
)


# Page 1 landing page
def page_1_landing_page():
    lat_list, lon_list = generate_random_coordinates_list()
    data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
    berlin_df = pd.DataFrame(data)
    datetimenow = time.strftime("%H:%M:%S")
    st.title(
        f"Welcome to BVG Controllers BER 👋",
    )
    st.map(data=public_stations, zoom=10, color="color", size=50)

    # Select Stations
    selected_options = st.multiselect("Select Station(s):", data1["station name"])
    st.write("You selected:", selected_options)

    # Add a refresh button
    st.table(berlin_df)
    output = st.empty()

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        output.text(f"Last Update: {current_time}")
        time.sleep(10)


# Load your existing database into a DataFrame
data = pd.read_csv(
    "/home/yannik/ticket-control-bvg/data/preprocessed_database_telegram.csv"
)  # Replace with the path to your database file
# Notice the .copy() to copy the values
df = data.copy()
df["date"] = pd.to_datetime(df["date"])


# Page 2: Control Statistics
def page_2_control_statistics():
    # Streamlit app
    st.title("Control Statistics")

    # description
    min_date = df["date"].iloc[0]

    max_date = df["date"].iloc[-1]

    user_date_ranges = st.date_input(
        "Enter a range of two dates or leave default",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # year_start, year_end = int(year_start), int(year_end)
    # month_start, month_end = int(month_start), int(month_end)
    # weekday_start, weekday_end = int(weekday_start), int(weekday_end)

    # # Filter the DataFrame based on user selections
    # df['year'] = pd.DatetimeIndex(df['date']).year
    # df['month'] = pd.DatetimeIndex(df['date']).month
    # df['day'] = pd.DatetimeIndex(df['date']).day

    # filtered_data = df[
    #     (df['date']>=datetime.date(year_start,month_start, weekday_start)) &
    #     (df['date']<=datetime.date(year_end,month_end, weekday_end))
    #     ]

    # # Naming the weekdays
    # weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    # # Applying the naming
    # df["weekday"] = df["day"].map(weekdays)

    # day_labels = df['weekday'].unique()
    # day_sizes = df['day'].value_counts()

    # # Create a bar chart from the filtered data
    # range_fig, ax = plt.subplots()
    # ax.bar(filtered_data['date'], filtered_data['station name'])
    # plt.xlabel("Date")
    # plt.ylabel("Counter")
    # plt.title("Bar Chart Based on Selected Ranges")

    # # Display the bar chart
    # st.pyplot(range_fig)

    # User input for number of top items to display
    top_n_areas = st.selectbox("Select the number of areas to display:", [10, 25, 50])
    top_n_stations = st.selectbox(
        "Select the number of station names to display:", [10, 25, 50]
    )
    top_n_lines = st.selectbox("Select the number of lines to display:", [5, 10, 20])

    # Arrange tables side by side
    st.write("Control Statistics:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"{top_n_areas} Most controlled areas:")
        area_counts = df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["area"].value_counts()
        st.write(area_counts.head(top_n_areas))

    with col2:
        st.write(f"{top_n_stations} Most controlled stations:")
        station_counts = df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["station name"].value_counts()
        st.write(station_counts.head(top_n_stations))

    with col3:
        st.write(f"{top_n_lines} Most controlled lines:")
        lines_counts = df[
            (df["date"] >= pd.to_datetime(user_date_ranges[0]))
            & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
        ]["lines"].value_counts()
        st.write(lines_counts.head(top_n_lines))

    # Areas
    st.title("Areas, stations & lines visualization")

    # Calculate area frequencies using data ranges selected by user
    area_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["area"].value_counts()

    # Create a plotly map
    fig1 = px.treemap(
        names=area_counts.index,
        parents=[""] * len(area_counts),
        values=area_counts.values,
        title="Area Visualization",
    )

    # Display the figure
    st.plotly_chart(fig1)

    # Calculate station frequencies
    station_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["station name"].value_counts()
    # Create a plotly map
    fig2 = px.treemap(
        names=station_counts.index,
        parents=[""] * len(station_counts),
        values=station_counts.values,
        title="Station Visualization",
    )

    # Display the figure
    st.plotly_chart(fig2)

    # Calculate lines frequencies
    lines_counts = df[
        (df["date"] >= pd.to_datetime(user_date_ranges[0]))
        & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
    ]["lines"].value_counts()
    # Create a plotly mapp
    fig3 = px.treemap(
        names=lines_counts.index,
        parents=[""] * len(lines_counts),
        values=lines_counts.values,
        title="Lines Visualization",
    )

    # Display the figure
    st.plotly_chart(fig3)

    # Pie charts for year, month, day:

    st.title("Time visualization")

    # df['year'] = pd.DatetimeIndex(df['date']).year
    # df['month'] = pd.DatetimeIndex(df['date']).month
    # df['day'] = pd.DatetimeIndex(df['date']).day

    # # Naming the weekdays
    # weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    # # Applying the naming
    # df["weekday"] = df["day"].map(weekdays)

    # day_labels = df['weekday'].unique()
    # day_sizes = df['day'].value_counts()

    # fig4, ax4 = plt.subplots()
    # plt.title('Weekdays')
    # ax4.pie(
    #     x=day_sizes,
    #     labels=day_labels,
    #     autopct='%1.1f%%',
    #     startangle=90
    #     )
    # ax4.axis('equal')

    # st.pyplot(fig4)


# Main app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:", ("Check Controls :rainbow:", "Control Statistics :dart:")
    )

    if page == "Check Controls :rainbow:":
        page_1_landing_page()
    elif page == "Control Statistics :dart:":
        page_2_control_statistics()


if __name__ == "__main__":
    main()


# # Title and description
# st.title("Date Range Selector")
# st.write("Select a range of years, months, and weekdays using sliders:")

# # Year range selection with full range by default
# year_start, year_end = st.slider("Select the range of years:", 2018, 2023, (2018, 2023))

# # Month range selection with full range by default
# month_start, month_end = st.slider("Select the range of months:", 1, 12, (1, 12))

# # Weekday range selection with full range by default
# weekday_start, weekday_end = st.slider("Select the range of weekdays:", 0, 6, (0, 6))

# # Generate sample data for demonstration (replace with your own data)
# data = pd.DataFrame({
#     'Date': pd.date_range(start=f'{year_start}-{month_start}-01', end=f'{year_end}-{month_end}-{calendar.monthrange(year_end, month_end)[1]}'),
#     'Value': [i for i in range((year_end - year_start + 1) * (month_end - month_start + 1) * (weekday_end - weekday_start + 1))]
# })

# # Filter the DataFrame based on user selections
# filtered_data = data[
#     (data['Date'].dt.year >= year_start) & (data['Date'].dt.year <= year_end) &
#     (data['Date'].dt.month >= month_start) & (data['Date'].dt.month <= month_end) &
#     (data['Date'].dt.weekday >= weekday_start) & (data['Date'].dt.weekday <= weekday_end)
# ]

# # Create a bar chart from the filtered data
# fig, ax = plt.subplots()
# ax.bar(filtered_data['Date'], filtered_data['Value'])
# plt.xlabel("Date")
# plt.ylabel("Value")
# plt.title("Bar Chart Based on Selected Ranges")

# # Display the bar chart
# st.pyplot(fig)

# # Display selected date ranges
# st.write(f"Selected Year Range: {year_start} - {year_end}")
# st.write(f"Selected Month Range: {calendar.month_name[month_start]} - {calendar.month_name[month_end]}")
# st.write(f"Selected Weekday Range: {calendar.day_name[weekday_start]} - {calendar.day_name[weekday_end]}")
