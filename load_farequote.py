import csv
import time
import calendar

from influxdb import InfluxDBClient

def main(host='localhost', port=8086):
    user = 'root'
    password = 'root'
    dbname = 'Airfare'
    airline_data = load();
    json_body = get_data()
    client = InfluxDBClient(host, port, user, password, dbname)

    client.delete_database(dbname)
    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Writing data")
    client.write_points(json_body)

def load():
  with open('farequote.csv', 'rb') as csvfile:
    farequotes = csv.reader(csvfile, delimiter=',')
    list1 = []
    i = 1
    for row in farequotes:
        if i==0: 
            row[0] = row[0].replace("Z","")
            row[0] = calendar.timegm(time.strptime(row[0], "%Y-%m-%d %H:%M:%S"));
        i=0;
        list1.append(row)
    return list1

def get_data():
    airline_data = load();
    fields = airline_data[0];
    json_body = [{
        "points": airline_data[1 : len(airline_data)],
        "name": "metrics",
        "columns": fields
    }]
    json1_body = [{
        "points": [
	   ["2014-06-27 17:39:52Z", 20]
        ],
        "name": "foo",
        "columns": ["time", "column_two"]
    }]
    return json_body


if __name__ == '__main__':
  main()
