# imports
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# constants
BASE_URL = os.getenv('BASE_URL')

PG_USER=os.getenv('PG_USER')
PG_PASSWORD=os.getenv('PG_PASSWORD')
PG_HOST=os.getenv('PG_HOST')
PG_BASE=os.getenv('PG_BASE')
PG_PORT=5432

NY_TAXI_TABLE='yellow_taxi_data'
YEAR=2021
MONTH_NUM=1

url = f"{BASE_URL}yellow_tripdata_{YEAR}-{MONTH_NUM:02d}.csv.gz"
df = pd.read_csv(url)

# df.head()
# df.dtypes
# df.shape

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates
)

engine = create_engine(f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_BASE}')

# print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

df.head(n=0).to_sql(name=NY_TAXI_TABLE, con=engine, if_exists='replace', index=False)


df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
)

for df_chunk in tqdm(df_iter):
    print(len(df_chunk))


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name=NY_TAXI_TABLE, con=engine, if_exists='append', index=False)

