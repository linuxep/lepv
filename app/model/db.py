from influxdb import InfluxDBClient

DBclient = InfluxDBClient('db', 8086, 'root', 'root123', 'mydb')
DBclient.create_database('mydb')

#  INSERT memory,host=127.0.0.0 total=1000,free=865,buffers=78,caches=69
#  INSERT memory,host=127.0.0.0 total=1000,free=875,buffers=78,caches=96

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
    result = DBclient.query('select * from memory;')
    print("Result: {0}".format(result))
