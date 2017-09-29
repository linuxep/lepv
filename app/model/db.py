from influxdb import InfluxDBClient

DBclient = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')
DBclient.create_database('mydb')

if(__name__ == '__main__'):
    json_body = [
        {
            "measurement": "cpu_load_short",
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
    DBclient.write_points(json_body)
    result = DBclient.query('select value from cpu_load_short;')
    print("Result: {0}".format(result))
