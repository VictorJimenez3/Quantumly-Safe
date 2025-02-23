import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

import os

org = "Q-Safe"
token = os.environ.get("INFLUX_TOKEN", "")

url="http://localhost:8086"

class DB:    
    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def add_user(self, data: dict):
        p = influxdb_client.Point(data["id"]).field("userdata", data)

        self.write_api.write(bucket="users", org=org, record=p)
        
        return True

    def add_activity(self, data: dict):
        """
        activities will have similar and often time identical userID's (uid)
        any activity will have it's own unique id attr in the data dict however

        indexing by uid will help to make searching faster for IP's on certain servers
        """

        p = influxdb_client.Point(data["id"]).tag("UID", data["uid"]).field("activitydata", data)

        self.write_api.write(bucket="activites", org=org, record=p)
        
        return True