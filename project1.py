import pandas as pd
import nycflights13 as flights
import numpy as np
# 항공편 데이터 (main dataset)
df_flights = flights.flights
df_airlines = flights.airlines
df_airports = flights.airports
df_planes = flights.planes
df_weather = flights.weather

df_flights.info()
df_airlines

df_weather['humid'].min()
df_weather['humid'].max()

# 예시: 항공편 데이터 확인
print(df_flights.head())

np.unique(df_weather['precip'])

df_weather['precip'][df_weather['precip'] > 0]

df_flights.loc[np.where(df_weather['precip'] > 0)[0], :]['arr_delay'].mean()
np.unique(df_flights['origin'])


df_airlines

flight, counts = np.unique(df_flights['carrier'], return_counts= True)
flight
counts
np.unique(df_planes['seats'])


df_planes

import pandas as 