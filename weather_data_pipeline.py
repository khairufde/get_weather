import pandas as pd
import requests
import json
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.dates import days_ago


def get_weatherData(ti):

    city_name = # <'INPUT_CITY_NAME'>
    api_key = # <'YOUR_API_KEY'>

    coor_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}'
    coor_req = requests.get(coor_url)
    coor_req.raise_for_status()
    coor_data = coor_req.json()

    if coor_data:
        lat = str(coor_data[0]['lat'])
        lon = str(coor_data[0]['lon'])
    else:
        print("No data found")
        exit()

    fore_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    fore_req = requests.get(fore_url)
    json_data = json.loads(fore_req.text)

    # Access the forecast list
    forecast_list = json_data.get('list', [])
    weather_data = []

    for forecast in forecast_list:
        # Extract relevant data
        dt = pd.to_datetime(forecast['dt_txt'])
        weather = forecast['weather'][0]  # Get first weather entry
        main = forecast['main']
        wind = forecast['wind']
        
        # Collect data
        weather_data.append({
            'date': dt.date(),
            'time': dt.strftime('%H:%M:%S'),
            'weather': weather['main'],
            'weather_desc': weather['description'],
            'temp': main['temp'],
            'feels_like': main['feels_like'],
            'temp_min': main['temp_min'],
            'temp_max': main['temp_max'],
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'wind_speed': wind['speed'],
            'wind_deg': wind['deg'],
            'wind_gust': wind.get('gust', None)  # gust might not always be present
        })

    weather_df = pd.DataFrame(weather_data)

    weather_df[['year', 'month', 'day']] = weather_df['date'].astype(str).str.split('-', expand=True)
    weather_df.drop(columns=['date'], inplace=True)

    cols = ['year', 'month', 'day'] + [col for col in weather_df.columns if col not in ['year', 'month', 'day']]
    weather_df = weather_df[cols]

    # Push the transformed data to XCom
    ti.xcom_push(key='transformed_data', value=weather_df.to_dict('records'))

def load_to_postgres(ti):

    transformed_data = ti.xcom_pull(key='transformed_data', task_ids='fetch_weather_data')
    if not transformed_data:
        raise ValueError('No data found')

    postgres_hook = PostgresHook(postgres_conn_id="weather_connection")
    insert_query = """
                    INSERT INTO weather 
                    (
                    "year",
                    "month",
                    "day",
                    "time",
                    "weather",
                    "weather_desc",
                    "temp",
                    "feels_like",
                    "temp_min",
                    "temp_max",
                    "pressure",
                    "humidity",
                    "wind_speed",
                    "wind_deg",
                    "wind_gust"
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (year, month, day)
                    DO NOTHING
                    ;
                    """
    
    for data in transformed_data:
        postgres_hook.run(insert_query,
                           parameters= (
                                        data["year"],
                                        data["month"],
                                        data["day"],
                                        data["time"],
                                        data["weather"],
                                        data["weather_desc"],
                                        data["temp"],
                                        data["feels_like"],
                                        data["temp_min"],
                                        data["temp_max"],
                                        data["pressure"],
                                        data["humidity"],
                                        data["wind_speed"],
                                        data["wind_deg"],
                                        data["wind_gust"]
                                        )
                            )

default_args = {
    'owner': 'khairufde',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email': ['khairullahf04@gmail.com']
}

dag = DAG(
    'get_weather_data',
    default_args=default_args,
    description='Extract weather data with API per days',
    schedule_interval=timedelta(days=1)
)

# Airflow Task Definitions
fetch_weather_data = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=get_weatherData,
    dag=dag,
)

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='weather_connection',
    sql='''CREATE TABLE IF NOT EXISTS weather (
            year CHAR(4),
            month CHAR(2),
            day CHAR(2),
            time TIME,
            weather VARCHAR(50),
            weather_desc VARCHAR(30),
            temp FLOAT,
            feels_like FLOAT,
            temp_min FLOAT,
            temp_max FLOAT,
            pressure INT,
            humidity INT,
            wind_speed FLOAT,
            wind_deg INT,
            wind_gust FLOAT,
            PRIMARY KEY (year, month, day)
            );''',
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag,
)

# Task Dependencies
fetch_weather_data >> create_table >> load_data
