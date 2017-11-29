import argparse

from  influxdb import InfluxDBClient

def main(host='localhost',port=8086):
    user = 'root'
    password = 'root'
    dbname = 'example'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select value from cpu_load_short;'
    json_body = [{
        "measurement": "cpu_load_short",
        "tags":{
            "host":"server01",
            "region":"us-west"
        },
        "time":"2009-11-10T23:00:00Z",
        "fields":{
            "value":0.64
        }
    }]


    client = InfluxDBClient(host,port,user,password,dbname)
    client.create_database(dbname)
    client.create_retention_policy('awesome_policy','3d',3,default=True)
    client.switch_user(dbuser, dbuser_password)
    client.write_points(json_body)
    result = client.query(query)
    print(result)
    client.switch_user(user,password)
    #client.drop_database(dbname)
def parse_args():
    parser = argparse.ArgumentParser(description='exmple code to play with InfluxDB')
    parser.add_argument('--host',type=str,required = False,default='localhost',
                        help='hostnameof InfluxDB http Api')
    parser.add_argument('--port',type=int ,required=False,default=8086,
                        help='port of InfluxDb http Api')
    return parser.parse_args()

# if __name__ == '__main__':
#     args = parse_args()
#     main(host=args.host,port=args.port)