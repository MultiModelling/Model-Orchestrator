from influxdb import InfluxDBClient
from locale import atof
import urllib.parse
import glob, os
import codecs
import csv
import re


class InfluxInterface:

    def __init__(self, api_addr, config=None, logger=None):

        # Configurable API Specification
        self.api_addr = api_addr
        self.config = config

        # Airflow Params
        self.logger = logger

    def init(self):
        client = self.connect_database()

        for filename in glob.glob("./data/*.csv"):
            self.process_profiles_csv(client, filename)

    def connect_database(self):

        endpoint = self.urlparse(self.api_addr)

        client = InfluxDBClient(host=endpoint.hostname,
                                port=endpoint.port,
                                database=self.config['db_name'],
                                ssl=self.config['use_ssl'])

        if self.config['db_name'] not in client.get_list_database():
            client.create_database(self.config['db_name'])

        return client

    def urlparse(self,addr):
        if not re.search(r'^[A-Za-z0-9+.\-]+://', addr):
            addr = 'http://{0}'.format(addr)
        return urllib.parse.urlparse(addr, 'http')

    def format_datetime(self,dt):
        date, time = dt.split(" ")
        day, month, year = date.split("-")
        ndate = year + "-" + month + "-" + day
        ntime = time + ":00+0000"
        return ndate + "T" + ntime

    def process_profiles_csv(self,client, file_path):
        path_parts = os.path.split(file_path)
        file_name = path_parts[-1]
        measurement = os.path.splitext(file_name)[0]

        with codecs.open(file_path, encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')

            column_names = next(reader)
            print(column_names)

            num_fields = len(column_names)
            json_body = []

            for row in reader:
                fields = {}
                for i in range(1, num_fields):
                    if row[i]:
                        fields[column_names[i]] = atof(row[i])

                json_body.append({
                    "measurement": measurement,
                    "time": self.format_datetime(row[0]),
                    "fields": fields
                })

            client.write_points(points=json_body, database=self.config['db_name'], batch_size=100)