<h1>Weather Data Pipeline using <a href="https://openweathermap.org/">OpenWeatherMapAPI</a>, Airflow, and load Postgres</h1>

<h2>Description</h2>
This project automates the process of collecting 5-day weather forecasts, scheduling, and storing weather data. It demonstrates a ETL (Extract, Transform, Load) pipeline by leveraging the <a href="https://openweathermap.org/">openweathermapAPI</a>, scheduling with Apache Airflow running daily, then loading the transformed data into a PostgreSQL database.
<br />

<h2>Languages and Utilities Used</h2>

- <b>python</b>
- <b>web scrapping</b>
- <b>requests</b>
- <b><a href="https://openweathermap.org/">openweathermapAPI</a></b>
- <b>ETL</b>
- <b>pandas</b>
- <b><a href="https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html">Airflow</a></b>
- <b>docker</b>
- <b>postgres</b>
- <b>PgAdmin</b>
- <b>sql</b>

<h2>Pipeline Design</h2>

<p align="center">
<br />
<img src="https://i.imgur.com/hZIbCSg.png" height="60%" width="60%" alt="Pipeline Design"/>
<br />

<h2>How to obtain API Key:</h2>

<p align="center">
<br />
You have to sign in to <a href="https://openweathermap.org/">openweathermapAPI</a>, then navigate to My API Keys<br/>
<img src="https://i.imgur.com/WGDsGwV.jpeg" height="60%" width="60%" alt="MyAPIKeys"/>
<br />
<br />
Copy the API Key<br/>
<img src="https://i.imgur.com/b0ullLH.jpeg" height="60%" width="60%" alt="CopytheAPIKey"/>
<br />
<br />
Paste to the api_key in weather_data_pipeline.py. Enter the name of the city whose weather data you want to obtain. example: "london"<br/>
<img src="https://i.imgur.com/J0LKeBT.jpeg" height="60%" width="60%" alt="Pasteapi_key"/>
<br />

<h2>Airflow dags and Output Table in PgAdmin</h2>

<p align="center">
<br />
Airflow<br/>
<img src="https://i.imgur.com/jHjFWoU.jpeg" height="60%" width="60%" alt="Airflow"/>
<br />
<br />
Output Table in PgAdmin<br/>
<img src="https://i.imgur.com/nta4P6U.jpeg" height="60%" width="60%" alt="PgAdmin"/>
<br />
</p>

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
