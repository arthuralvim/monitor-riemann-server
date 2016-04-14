# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from decouple import config
import random
import datetime

random.seed(100)


class InfluxDBPayload(object):

    HOST = config('INFLUXDB_HOST', default='localhost')
    PORT = config('INFLUXDB_PORT', default=8086, cast=int)

    ADMIN_USER = config('INFLUXDB_ADMIN_USER', default='root')
    ADMIN_PASSWORD = config('INFLUXDB_ADMIN_PASSWORD', default='root')

    DB_USER = config('INFLUXDB_DB_USER', default='influxdb_user')
    DB_PASSWORD = config('INFLUXDB_DB_PASSWORD', default='influxdb_password')
    DB_NAME = config('INFLUXDB_DB_NAME', default='exemplo')

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = InfluxDBClient(
                self.HOST, self.PORT, self.ADMIN_USER, self.ADMIN_PASSWORD,
                self.DB_NAME)
        return self._client

    def demo(self):
        npoints = 10000

        for point in xrange(npoints):
            measure = random.randint(1, 10)
            host = random.randint(1, 10)
            json_body = [
                {
                    "measurement": "mea-{0}".format(str(measure)),
                    "tags": {
                        "host": "server-{0}".format(str(host)),
                        "region": "us-west"
                    },
                    "time": datetime.datetime.isoformat(
                        datetime.datetime.utcnow()),
                    "fields": {
                        "value": random.random()
                    }
                }
            ]

            self.client.write_points(json_body)

if __name__ == '__main__':
    ifdb = InfluxDBPayload()

    query = 'SELECT value FROM mea;'

    json_body = [
        {
            "measurement": "mea",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": 0.64
            }
        }
    ]

    try:
        print("Create database: " + ifdb.DB_NAME)
        ifdb.client.create_database(ifdb.DB_NAME)
    except InfluxDBClientError:
        pass

    try:
        print("Create a retention policy")
        ifdb.client.create_retention_policy('awesome_policy', '3d', 3,
                                            default=True)
    except InfluxDBClientError:
        pass

    print("Switch user: " + ifdb.DB_USER)
    ifdb.client.switch_user(ifdb.DB_USER, ifdb.DB_PASSWORD)

    print("Write points: {0}".format(json_body))
    ifdb.client.write_points(json_body)

    ifdb.demo()

    print("Queying data: " + query)
    result = ifdb.client.query(query)

    print("Result: {0}".format(result))

    print("Switch user: " + ifdb.ADMIN_USER)
    ifdb.client.switch_user(ifdb.ADMIN_USER, ifdb.ADMIN_PASSWORD)

    if config('DROP_DATABASE', default=False, cast=bool):
        print("Drop database: " + ifdb.DB_NAME)
        ifdb.client.drop_database(ifdb.DB_NAME)
