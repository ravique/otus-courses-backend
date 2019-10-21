from datetime import datetime

from influxdb import InfluxDBClient

from otus_django_courses.settings import env

influx_client = InfluxDBClient(
    host=env('INFLUXDB_HOST'),
    port=env('INFLUXDB_PORT'),
    database=env('INFLUXDB_DB')
)


class InfluxLogger:

    @staticmethod
    def write(measurement: str, value: int):
        return influx_client.write_points([{
            "measurement": measurement,
            "tags": {
                "host": "localhost",
            },
            "time": datetime.now(),
            "fields": {
                "value": value
            }
        }])
