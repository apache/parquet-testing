#!/usr/bin/env python3

from datetime import date as d
from pathlib import Path
from sys import argv, exit
from urllib import request

import os

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


TOKEN_PRE_2015 = "_2014-12"
TOKEN_2015_2016 = "2015-01_2016-06"
TOKEN_2016_2018 = "2016-07_2018-12"
TOKEN_POST_2019 = "2019-01_"


COLUMNS = {
    TOKEN_PRE_2015: [
        "vendor_id",
        "pickup_at",
        "dropoff_at",
        "passenger_count",
        "trip_distance",
        "pickup_longitude",
        "pickup_latitude",
        "rate_code_id",
        "store_and_fwd_flag",
        "dropoff_longitude",
        "dropoff_latitude",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "total_amount"
    ],
    TOKEN_2015_2016: [
        "vendor_id",
        "pickup_at",
        "dropoff_at",
        "passenger_count",
        "trip_distance",
        "pickup_longitude",
        "pickup_latitude",
        "rate_code_id",
        "store_and_fwd_flag",
        "dropoff_longitude",
        "dropoff_latitude",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount"
    ],
    TOKEN_2016_2018: [
        "vendor_id",
        "pickup_at",
        "dropoff_at",
        "passenger_count",
        "trip_distance",
        "rate_code_id",
        "store_and_fwd_flag",
        "pickup_location_id",
        "dropoff_location_id",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount"
    ],
    TOKEN_POST_2019: [
        "vendor_id",
        "pickup_at",
        "dropoff_at",
        "passenger_count",
        "trip_distance",
        "rate_code_id",
        "store_and_fwd_flag",
        "pickup_location_id",
        "dropoff_location_id",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount",
        "congestion_surcharge"
    ]
}

TYPES = {
    "vendor_id": "str",
    "passenger_count": "int8",
    "trip_distance": "float32",
    "pickup_longitude": "float32",
    "pickup_latitude": "float32",
    "pickup_location_id": "int32",
    "dropoff_longitude": "float32",
    "dropoff_latitude": "float32",
    "dropoff_location_id": "int32",
    "rate_code_id": "str",
    "store_and_fwd_flag": "str",
    "payment_type": "str",
    "fare_amount": "float32",
    "extra": "float32",
    "mta_tax": "float32",
    "tip_amount": "float32",
    "tolls_amount": "float32",
    "improvement_surcharge": "float32",
    "total_amount": "float32",
    "congestion_surcharge": "float32"
}


def download_url(date):
    url = "https://s3.amazonaws.com/nyc-tlc/trip+data"
    year_month = date.strftime("%Y-%m")
    filename = f"yellow_tripdata_{year_month}.csv"
    return f"{url}/{filename}"


def download_fd(date):
    url = download_url(date)
    return request.urlopen(url)


def token(date):
    if (date < d(2015, 1, 1)):
        return TOKEN_PRE_2015
    elif d(2015, 1, 1) <= date and date < d(2016, 7, 1):
        return TOKEN_2015_2016
    elif d(2016, 7, 1) <= date and date < d(2019, 1, 1):
        return TOKEN_2016_2018
    else:
        return TOKEN_POST_2019


def parse_date(date_string):
    if date_string.count("-") == 1:
        date_string = f"{date_string}-01"
    return d.fromisoformat(date_string)


def read_csv(date, fd, **kwargs):
    columns = COLUMNS[token(date)]

    types = {k: v for k, v in TYPES.items() if k in columns}
    date_columns = [c for c in columns if c.endswith("_at")]

    return pd.read_csv(fd, header=0, names=columns,
                       # Some months have extra commas not matching the header
                       # columns' size. Passing an explicit usecols fixes this.
                       index_col=False, usecols=range(len(columns)),
                       dtype=types, parse_dates=date_columns,
                       # Ignore errors
                       error_bad_lines=False, skip_blank_lines=True,
                       **kwargs)


def output_path(date):
    year = date.strftime("%Y")
    month = date.strftime("%m")
    return f"{year}/{month}/data.parquet"


def write_parquet(table, path):
    basedir = os.path.dirname(path)
    if basedir and not os.path.exists(basedir):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    pq.write_table(table, path, row_group_size=2**16)


def usage():
    print("usage:")
    print("csv2parquet <yyyy-mm-date>")


def main():

    if len(argv) < 1:
        usage()
        exit(1)

    date = parse_date(argv[1])
    fd = download_fd(date)

    dataframe = read_csv(date, fd)
    table = pa.Table.from_pandas(dataframe)

    output = output_path(date)
    write_parquet(table, output)


if __name__ == "__main__":
    main()
