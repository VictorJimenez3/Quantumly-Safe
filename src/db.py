import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from app import User
import os

bucket = "users"
org = "Q-Safe"
token = os.environ.get("INFLUX_TOKEN", "")

url="http://localhost:8086"

"""
User Bucket:
id[INDEX]: composite(ip,"@",domain) 
domain: string,
ip: string,
unm: U(nullable, string),
hpw: U(nullable, string),
"""

class DB:    
    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def add_user(self, ip: str, domain: str, username: str, password: str):
        id_ = ip + "@" + domain
        p = influxdb_client.Point(id_).tag("IP", ip).field("userdata", {
            "ID" : id_,
            "IP" : ip,
            "DOMAIN" : domain,
            "USERNAME" : username if username else "",
            "PASSWORD" : password if password else "",
        })

        self.write_api.write(bucket="users", org=org, record=p)
        
        return True

    def add_activity(self, user_id, time_active, session_login_attempts, session_login_failures):
        query = f'from(bucket: "activities") |> count()'
        result = self.client.query_api().query(query, org=org)
        document_count = sum([len(table.records) for table in result])

        p = influxdb_client.Point(document_count + 1).tag("UID", user_id).field("userdata", {
            "ID" : user_id,
            "TIME_ACTIVE" : time_active,
            "SESSION_LOGIN_ATTEMPTS" : session_login_attempts,
            "SESSION_LOGIN_FAILURES" : session_login_failures
        })

        self.write_api.write(bucket="activites", org=org, record=p)
        
        return True

    def get_user(self, username):
        return User.query.filter_by(username=username).first()