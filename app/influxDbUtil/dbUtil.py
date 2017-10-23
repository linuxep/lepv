
__author__    = "李旭升 <programmerli@foxmail.com>"


from influxdb import InfluxDBClient

class myInfluxDbClient:
    def __init__(self):
        self._client=InfluxDBClient('localhost',8086,'root',",","test")
    def write_points(self,data):
        json_body = [
            {
                "measurement": "cpuAvgLoad",
                "tags": {
                    "requestId": "s123"
                },
                # "time": "2017-03-12T22:00:00Z",
                "fields": {
                    "data": data
                }
            }
        ]
        if self._client.write_points(json_body):
            return True
        else:
            return False




