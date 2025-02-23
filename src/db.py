import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from dotenv import load_dotenv
from pprint import pprint
import uuid, json, os

org = "Q-Safe"

load_dotenv()

token = os.environ.get("INFLUX_TOKEN", "")

bucket_name = "Interactions"
url="http://localhost:8086"

class DB:    
    def __init__(self):
        self.client = InfluxDBClient(
            url=url,
            token=token,
            org=org
        )

        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def add_interactions(self, data: dict):
        
        id_ = str(uuid.uuid4())
        data = json.dumps(data)
        
        p = influxdb_client.Point(id_).field("interactionData", data)

        self.write_api.write(bucket = bucket_name, org = org, record = p)
        
    def add_user_record(self, username: str, password: str, ip: str, domain: str, user_agent: str):
        self.add_interactions({
            "totalAttempts": 0,
            "failedAttempts": 0,
            "ip": ip,
            "domainName": domain,
            "username": username,
            "password": password,
            "userAgent": user_agent
        })
    
    def aggregate_user_signin(self, ip: str, domain: str, username: str, failed_log_in_count: int, total_log_in_count: int):

        rows = self.query_api.query_stream( #row iterable of all rows in table
            f'from(bucket: "{bucket_name}") |> range(start: -inf)'
        )

        while (row := rows.__next__()) != None:  
            #Find the row with ip, domain, & username equal to parameters
            try:
                measurement = row.get_measurement()
                data = dict(json.loads(row.get_value()))
            except Exception as e:
                print(f"Failed to cast stringed row into dictionary: {e}")
                continue
            
            if data.get("ip", None) == ip and data.get("domain", None) and data.get("username", None) == username:
                #row found
                # Delete the existing record before updating
                self.delete_api.delete(start='1970-01-01T00:00:00Z', stop='2030-01-01T00:00:00Z', predicate=f'_measurement="{measurement}"', bucket=bucket_name, org=org)
                break
        else:
            return False
        
        #Add failed and total login count to existing record
        updated_data = {
            "totalAttempts": int(data.get("totalAttempts", 0)) + total_log_in_count,
            "failedAttempts": int(data.get("failedAttempts", 0)) + failed_log_in_count,
            "ip": ip,
            "domainName": domain,
            "username": username,
            "password": data.get("password", None),  # Retain existing password if needed
            "userAgent": data.get("userAgent", None)  # Retain existing user agent if needed
        }

        p = influxdb_client.Point(measurement).field("interactionData", json.dumps(updated_data))

        # Write the updated point back to the InfluxDB
        self.write_api.write(bucket=bucket_name, org=org, record=p)

        return True

    def grab_rows(self, start="-inf"):
        rows = self.query_api.query_stream( #row iterable of all rows in table
                f'from(bucket: "{bucket_name}") |> range(start: {start})'
        )

        retval = []
            
        try:
            for x in rows:
                y = dict(json.loads(x.get_value()))
                y.update({"timestamp" : x.get_time().timestamp()})
                retval.append(y)
            return retval #exhaust rows from generator
        except Exception as e:
            print(f"data improperly formatted in influx, please fix: {e}")

    def get_users_by_username(self, domain: str, username: str):
        return tuple([y for y in filter(
            lambda x: (x.get("domain", None) == domain and
                       x.get("username", None) == username
        ), self.grab_rows())])
    
    def get_user(self, user_uuid: str):
        rows = self.query_api.query_stream( #row iterable of all rows in table
            f'from(bucket: "{bucket_name}") |> range(start: -inf)'
        )

        try:
            for row in rows:
                if row.get_measurement() == user_uuid:
                    data = dict(json.loads(row.get_value()))
                    return data  # Return the user data if found
                
        except Exception as e:
            print(f"Error retrieving user by UUID: {e}")

        return None  # Return None if no user is found

db = DB()

client = InfluxDBClient(url=url, token=token, org=org)

def initilize_bucket(bucket:str):
    #this is for testing, it makes the current data disapear for the new data, remove in final version

    buckets_api = client.buckets_api()
    try:
        bucket_obj = buckets_api.find_bucket_by_name(bucket)
        bucket_id = bucket_obj.id
        buckets_api.delete_bucket(bucket_id)
        print(f"Deleted existing bucket: {bucket}")
    except Exception as e:
        print(f"Bucket {bucket} not found or already deleted. Error: {e}")
        
    retval = buckets_api.create_bucket(bucket_name=bucket, org=org)
    # print(f"Created new bucket: {bucket} {retval}")

# initilize_bucket(bucket_name)

# person = {
#     #id is randomly generated
#     "total_log_in_count":"6",
#     "failed_log_in_count": "23",
#     "ip":"1.255.453",
#     "domain":"apple.com",
#     "username":"Stebe Jobs",
#     "password":"password",
#     "user_agent":"firefox"
# }

# db.add_interactions(person)

# db.aggregate_user_signin(
#     ip="1.255.453",
#     domain="apple.com",
#     username="Stebe Jobs",
#     failed_log_in_count= 5,
#     total_log_in_count = 7,
# )

pprint(db.grab_rows())