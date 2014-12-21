from influxdb import InfluxDBClient
from influxdb import DataFrameClient

host = "cbe"
port = 49157
user = 'root'
password = 'root'
dbname = 'Airfare'

def get_client():
    return InfluxDBClient(host, port, user, password, dbname)

def get_df_client():
    return DataFrameClient(host, port, user, password, dbname)

def init():
    client = get_client()
    client.delete_database(dbname)
    print("Create database: " + dbname)
    client.create_database(dbname)