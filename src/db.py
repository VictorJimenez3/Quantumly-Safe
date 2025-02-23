import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient
import os
from dotenv import load_dotenv
import json
import uuid

class DB:    
    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    #maybe serialize json so strings and boolean dont mess up the DB, or just have clean data
    def add_interactions(self, data: dict):
        #measurement name for each column, add later when data is finalized
        
        id_ = str(uuid.uuid4())
        data = json.dumps(data)
        #print(data, type(data))
        p = influxdb_client.Point(id_).field("interactionData", data)

        self.write_api.write(bucket="Interactions", org=org, record=p)
        
    
    def add_user_record(self, username:str, password:str, ip:str, domain:str, user_agent:str):
        self.add_interactions({
            "total_log_in_count":0,
            "failed_log_in_count": 0,
            "ip":ip,
            "domain":domain,
            "username":username,
            "password":password,
            "user_agent":user_agent
        })
    
    def aggregate_user_signin(ip:str, domain:str, username:str, failed_log_in_count:int, total_log_in_count:int):
        #Find the input with ip, domain, & username equal to parameters
        #
        #Add failed and total login count to existing record
        


        for row in range(8): #moving through dictionary? lowk confused myself with the local non local shi ask
            if row["ip"] == ip and row["domain"] == domain and row[username] == "username":
                row["failed_log_in_count"] += 1
                row["total_log_in_count"] += 1

        
    

    '''
    def add_activity(self, data: dict):
        """
        activities will have similar and often time identical interactionID's (uid)
        any activity will have it's own unique id attr in the data dict however

        indexing by uid will help to make searching faster for IP's on certain servers
        """
        id_ = data["id"]

        data = json.dumps(data)
        p = influxdb_client.Point(id_).field("interactiondata", data)


        self.write_api.write(bucket="activites", org=org, record=p)
        
        return True
        
    '''

org = "Q-Safe"

load_dotenv()

# Environment and connection settings
token = os.getenv("INFLUXDB_TOKEN")

url="http://localhost:8086"

bucket1 = "Interactions"
db = DB()

client = InfluxDBClient(url=url, token=token, org=org)

def initilize_bucket(bucket:str):
    #this is for testing, it makes the current data dissapear for the new data, remove in final version

    buckets_api = client.buckets_api()
    try:
        bucket_obj = buckets_api.find_bucket_by_name(bucket)
        bucket_id = bucket_obj.id
        buckets_api.delete_bucket(bucket_id)
        print(f"Deleted existing bucket: {bucket}")
    except Exception as e:
        print(f"Bucket {bucket} not found or already deleted. Error: {e}")
        
    retval = buckets_api.create_bucket(bucket_name=bucket, org=org)
    print(f"Created new bucket: {bucket} {retval}")



initilize_bucket(bucket1)

person = {
    #id is randomly generated
    "total_log_in_count":"6",
    "failed_log_in_count": "23",
    "ip":"1.255.453",
    "domain":"apple.com",
    "username":"Stebe Jobs",
    "password":"password",
    "user_agent":"firefox"
}


db.add_interactions(person)


