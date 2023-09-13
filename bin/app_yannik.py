# import streamlit as st
# import pandas as pd
# import time
# import random
# import calendar
# from datetime import datetime, timedelta, date
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# from ticket_control.params import path_to_data
# import requests
# from streamlit_lottie import st_lottie
# import plotly.figure_factory as ff
# import pydeck as pdk



# # Optional change Mapbox map to plotly Map. https://plotly.com/python/scattermapbox/
# def generate_random_coordinates():
#     min_lat, max_lat = 52.392166, 52.639004
#     min_lon, max_lon = 13.215260, 13.770269
#     random_lat = random.uniform(min_lat, max_lat)
#     random_lon = random.uniform(min_lon, max_lon)
#     return random_lat, random_lon


# def generate_random_coordinates_list(num_samples=100):
#     lat_list = []
#     lon_list = []
#     for x in range(num_samples):
#         random_lat, random_lon = generate_random_coordinates()
#         lat_list.append(random_lat)
#         lon_list.append(random_lon)
#     return lat_list, lon_list

# public_stations = pd.read_csv(str(path_to_data) + "/datanew_map2.csv")
# data1 = pd.read_csv(
#     str(path_to_data) + "/s_u_stations_fixed_with_keys_20230830.csv"
# )
# st.set_page_config(layout="wide")

# # Page 1 landing page
# def page_1_landing_page():
#     lat_list, lon_list = generate_random_coordinates_list()
#     data = {"Location": ["Berlin"] * 100, "LAT": lat_list, "LON": lon_list}
#     berlin_df = pd.DataFrame(data)
#     datetimenow = time.strftime("%H:%M:%S")
#     st.title("Welcome to BVG Controls👋")
#     st.map(data=public_stations, zoom=10, color="color", size=50)

#     # Select Stations
#     selected_options = st.multiselect("Select station(s):", data1["station name"])
#     st.write("You selected:", selected_options)

#     # Add a refresh button
#     st.table(berlin_df)
#     output = st.empty()

# # Load your existing database into a DataFrame
# data = pd.read_csv(
#     str(path_to_data) + "/preprocessed_database_telegram.csv"
# )  # Replace with the path to your database file
# # Notice the .copy() to copy the values
# df = data.copy()
# df["date"] = pd.to_datetime(df["date"])

# # Page 2: Control Statistics
# def page_2_control_statistics():
#     # Streamlit app
#     st.title("View statistics:mag_right:")

#     # description
#     min_date = df["date"].iloc[0]

#     max_date = df["date"].iloc[-1]

#     def load_animation(url):
#         r = requests.get(url)
#         if r.status_code != 200:
#             return None
#         return r.json()

#     train_animation = load_animation("https://lottie.host/aec64339-af7e-4713-95ad-2c11b57a4bc5/UdfXkvXrvL.json")


#     left_column, right_column = st.columns(2)

#     with left_column:
#         user_date_ranges = st.date_input(
#         "Enter a range of two dates or leave blank",
#         (min_date, max_date),
#         min_value=min_date,
#         max_value=max_date,
#     )

#         # User input for number of top items to display
#         top_n_areas = st.selectbox("Select the number of areas to display:", [10, 25, 50])
#         top_n_stations = st.selectbox(
#             "Select the number of station names to display:", [10, 25, 50]
#         )
#         top_n_lines = st.selectbox("Select the number of lines to display:", [10,15,25])

#     with right_column:
#         st_lottie(train_animation, height=300, key='train_animation')

#     # Arrange tables side by side
#     st.write("Control Statistics:")
#     col1, col2, col3 = st.columns([0.33, 0.33, 0.33], gap='small')
#     with col1:
#         st.write(f"{top_n_areas} Most controlled areas:")
#         area_counts = df[
#             (df["date"] >= pd.to_datetime(user_date_ranges[0]))
#             & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
#         ]["area"].value_counts()
#         st.write(area_counts.head(top_n_areas))

#     with col2:
#         st.write(f"{top_n_stations} Most controlled stations:")
#         station_counts = df[
#             (df["date"] >= pd.to_datetime(user_date_ranges[0]))
#             & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
#         ]["station name"].value_counts()
#         st.write(station_counts.head(top_n_stations))

#     with col3:
#         st.write(f"{top_n_lines} Most controlled lines:")
#         lines_counts = df[
#             (df["date"] >= pd.to_datetime(user_date_ranges[0]))
#             & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
#         ]["lines"].str.split(', ').explode().value_counts()
#         st.write(lines_counts.head(top_n_lines))

#     st.write("---")

#     # Areas
#     st.title("Areas, stations & lines visualization:tram:" )

#     st.write('Areas visualization')

#     # Calculate area frequencies using data ranges selected by user
#     area_counts = df[
#         (df["date"] >= pd.to_datetime(user_date_ranges[0]))
#         & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
#     ]["area"].value_counts()

#     # Create a plotly map
#     fig1 = px.treemap(
#         names=area_counts.index,
#         parents=[""] * len(area_counts),
#         values=area_counts.values
#     )

#     # Display the figure
#     st.plotly_chart(fig1)

#     st.write('Stations visualization')

#     # Calculate station frequencies
#     station_counts = df[
#         (df["date"] >= pd.to_datetime(user_date_ranges[0]))
#         & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
#     ]["station name"].value_counts()
#     # Create a plotly map
#     fig2 = px.treemap(
#         names=station_counts.index,
#         parents=[""] * len(station_counts),
#         values=station_counts.values
#     )

#     # Display the figure
#     st.plotly_chart(fig2)

#     st.write('Lines visualization')
#     # Calculate lines frequencies
#     lines_counts = df[
#         (df["date"] >= pd.to_datetime(user_date_ranges[0]))
#         & (df["date"] <= pd.to_datetime(user_date_ranges[1]))
#     ]["lines"].str.split(', ').explode().value_counts()
#     # Create a plotly mapp
#     fig3 = px.treemap(
#         names=lines_counts.index,
#         parents=[""] * len(lines_counts),
#         values=lines_counts.values
#     )

#     # Display the figure
#     st.plotly_chart(fig3)

#     st.write("---")

#     st.title("Time statistics:hourglass:")

#     # reating time columns for the differenct categories year, month, weekday, hour
#     df['year'] = pd.DatetimeIndex(df['date']).year
#     df['month'] = pd.DatetimeIndex(df['date']).month
#     df['day'] = pd.DatetimeIndex(df['date']).weekday
#     df['hour'] = df['date'].dt.hour

#     # Naming the weekdays
#     weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
#     # Applying the naming
#     df["weekday"] = df['day'].map(weekdays)
#     # Doing the same for months
#     months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Dec'}
#     df["month_name"] = df['month'].map(months)

#     weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
#     month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]


#     st.write('Distribution of annual controls')
#     fig4 = px.histogram(df, x="year", color_discrete_sequence=['#4048BF'],
#                         opacity=1)

#     st.plotly_chart(fig4, use_container_width=False)

#     st.write('Distribution of monthly controls')
#     fig5 = px.histogram(df, x="month_name", color_discrete_sequence=['#4048BF'],
#                         opacity=1, category_orders={"month_name": month_order})

#     st.plotly_chart(fig5, use_container_width=False)


#     st.write('Distribution of daily controls')
#     fig6 = px.histogram(df, x="weekday", color_discrete_sequence=['#4048BF'],
#                         opacity=1, category_orders={"weekday": weekday_order})

#     st.plotly_chart(fig6, use_container_width=False)


#     st.write('Distribution of hourly controls')
#     fig7 = px.histogram(df, x="hour", color_discrete_sequence=['#4048BF'],
#                         opacity=1)

#     st.plotly_chart(fig7, use_container_width=False)

#     # Load your existing database into a DataFrame
#     data = pd.read_csv("data/preprocessed_database_telegram.csv")  # Replace with the path to your database file
#     # Notice the .copy() to copy the values
#     # Streamlit app
#     st.title("Time Series")
#     df2 = data.copy()
#     df3= df2.copy()
#     df2 = df2.set_index("date")
#     df3["date"] = pd.to_datetime(df3["date"])
#     df2.index = pd.to_datetime(df2.index)

#     day = df2.resample('d')['station_key'].count()

#     st.write("Timeseries of daily controls")
#     st.line_chart(day, color="#4048BF")

#     week = df2.resample('w')['station_key'].count()

#     st.write("Timeseries of weekly controls")
#     st.line_chart(week, color="#4048BF", use_container_width=True)

#     # Streamlit app
#     st.title("Explore Berlin")

#     st.write("Controls across Berlin")
#     chart_data = df3.loc[user_date_ranges[0]:user_date_ranges[1] , "station name"].value_counts()
#     st.pydeck_chart(pdk.Deck(
#         map_style=None,
#         initial_view_state=pdk.ViewState(
#             latitude=52.507222,
#             longitude=13.332500,
#             zoom=11,
#             pitch=50,
#             ),
#         layers=[
#             pdk.Layer(
#                 'HexagonLayer',
#                 data=chart_data,
#                 get_position='[longitude, latitude]',
#                 radius=200,
#                 elevation_scale=4,
#                 elevation_range=[0, 1000],
#                 pickable=True,
#                 extruded=True,
#                 ),
#             pdk.Layer(
#                 'ScatterplotLayer',
#                 data=chart_data,
#                 get_position='[longitude, latitude]',
#                 get_color='[200, 30, 0, 160]',
#                 get_radius=200,
#                 ),
#             ],
#         ))

# # Main app
# def main():
#     st.sidebar.title("Navigation")
#     page = st.sidebar.radio(
#         "Go to:", (":one: Check & Predict Controls", ":two: View Statistics")
#     )

#     if page == ":one: Check & Predict Controls":
#         page_1_landing_page()
#     elif page == ":two: View Statistics":
#         page_2_control_statistics()


# if __name__ == "__main__":
#     main()
