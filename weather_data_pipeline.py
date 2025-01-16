import json
import pandas as pd
import requests
from sqlalchemy import create_engine
from datetime import date, timedelta, datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'khairufde',
    'start_date': days_ago(0),
    'email': ['khairullahf04@gmail.com'],
}

dag = DAG(
    'get_weather_data',
    default_args=default_args,
    description='Apache Airflow Capstone py',
    schedule_interval=timedelta(days=5),
)

def get_coor():

    with open("api_key.sh", "r") as f:
        api_key = f.read().strip()

    city_name = "london"

    coor_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}'

    coor_req = requests.get(coor_url)
    coor_data = coor_req.json()

    if coor_data:
        lat = str(coor_data[0]['lat'])
        lon = str(coor_data[0]['lon'])
        return lat, lon, api_key
    else:
        print("No data found")
        exit()

def get_weather_data(lat, lon, api_key):

    fore_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'

    fore_req = requests.get(fore_url)
    fore_data = fore_req.json()

    forecast_list = fore_data.get("list", [])

    weatherData_df = pd.json_normalize(
        forecast_list,
        sep="_",
        record_path=["weather"],
        meta=[
            "dt",
            "dt_txt",
            ["main", "temp"],
            ["main", "feels_like"],
            ["main", "temp_min"],
            ["main", "temp_max"],
            ["main", "pressure"],
            ["main", "humidity"],
            ["wind", "speed"],
            ["wind", "deg"],
            ["wind", "gust"],
            "visibility",
            "pop",
            ["clouds", "all"],
            ["sys", "pod"],
        ]
    )

    weatherData_df.rename(
        columns={
            "id": "weather_id",
            "main": "weather_main",
            "description": "weather_description",
            "icon": "weather_icon",
            "main_temp": "temperature",
            "main_feels_like": "feels_like",
            "main_temp_min": "temp_min",
            "main_temp_max": "temp_max",
            "main_pressure": "pressure",
            "main_humidity": "humidity",
            "wind_speed": "wind_speed",
            "wind_deg": "wind_direction",
            "wind_gust": "wind_gust",
            "clouds_all": "cloud_coverage",
            "sys_pod": "time_of_day",
        },
        inplace=True,
    )

    return weatherData_df

def load_to_mysql(weatherData_df):

    host="localhost",       # Replace with your MySQL host
    user="your_username",   # Replace with your MySQL username
    password="your_password",  # Replace with your MySQL password
    database="weather_data"  # Replace with your database name

    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

    weatherData_df.to_sql("weather", con=engine, if_exists="append", index=False)

# Define the tasks
get_coor = PythonOperator(
    task_id='extract_data',
    python_callable=get_coor,
    dag=dag,
)

get_weather_data = PythonOperator(
    task_id='filter_out',
    python_callable=get_weather_data,
    dag=dag,
)

load_to_mysql = PythonOperator(
    task_id='load_data_tar',
    python_callable=load_to_mysql,
    dag=dag,
)

# Set the task dependencies
get_coor >> get_weather_data >> load_to_mysql