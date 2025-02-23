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
            "total_log_in_count": 0,
            "failed_log_in_count": 0,
            "ip": ip,
            "domain": domain,
            "username": username,
            "password": password,
            "user_agent": user_agent
        })
    


def get_data_by_domain(self, domain: str):
    #lord knows, i dont
    #it returns a list of the rows with the same domain name, gives the entire row data per each element in the list
    rows = self.query_api.query_stream(
        f'from(bucket: "{bucket_name}") |> range(start: -inf)'  # Stream all rows
    )

    results = []

    try:
        for row in rows:
            row_data = dict(json.loads(row.get_value()))
            row_data.update({"timestamp" : row.get_time().timestamp()})  # parse jason
            if row_data.get("domain", None) == domain:  # domain matches?
                results.append(row_data)# do str(row_data) if he doesnt want the list to have json in it

    except Exception as e:
        print(f"Error retrieving data for domain '{domain}': {e}")

    return results  # Return list of json, idk if he wants strings tho


def grab_domain_values(self):
    domains = set()
    try:
        rows = self.query_api.query_stream(
            f'from(bucket: "{bucket_name}") |> range(start: -inf)'  # Stream all rows
        )
        fullrows = [dict(json.loads(x)) for x in rows]

    except Exception as e:
        print(f"uh oh: {e}")
        return list()

    [domains.add(x.get("domain")) for x in rows]
    
    return domains
    # domain_counts = {}

    # try:
    #     for row in rows:
    #         try:
    #             row_data = json.loads(row.get_value()) if isinstance(row.get_value(), str) else row.get_value()
                
    #             domain_name = row_data.get("domain")
    #             if domain_name:  # Ensure domain_name is valid
    #                 if domain_name in domain_counts:
    #                     domain_counts[domain_name] += 1
    #                 else:
    #                     domain_counts[domain_name] = 1
    #         except (json.JSONDecodeError, TypeError) as parse_error:
    #             print(f"Skipping row due to parsing error: {parse_error}")

    # except Exception as e:
    #     print(f"Error retrieving data for domain: {e}")

    # domain_list = []
    # count = 0
    # for key,tree in domain_counts:
    #     domain_list[count] = key
    #     count += 1
    # print(domain_list) # for me to check

    # return domain_list




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
            "total_log_in_count": int(data.get("total_log_in_count", 0)) + total_log_in_count,
            "failed_log_in_count": int(data.get("failed_log_in_count", 0)) + failed_log_in_count,
            "ip": ip,
            "domain": domain,
            "username": username,
            "password": data.get("password", None),  # Retain existing password if needed
            "user_agent": data.get("user_agent", None)  # Retain existing user agent if needed
        }

        p = influxdb_client.Point(measurement).field("interactionData", json.dumps(updated_data))

        # Write the updated point back to the InfluxDB
        self.write_api.write(bucket=bucket_name, org=org, record=p)

        return True

    def grab_rows(self, start="-inf"):
        rows = self.query_api.query_stream( #row iterable of all rows in table
                f'from(bucket: "{bucket_name}") |> range(start: {start})'
        )

        try:
            return sorted([(x.get_time().timestamp(), dict(json.loads(x.get_value()))) for x in rows], key=lambda x: x[0]) #exhaust rows from generator
        except Exception as e:
            print(f"data improperly formatted in influx, please fix: {e}")

    def get_users_by_username(self, domain: str, username: str):
        return tuple(filter(
            lambda x: (x[1].get("domain", None) == domain and
                       x[1].get("username", None) == username
        ), self.grab_rows()))
    
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

initilize_bucket(bucket_name)

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

db.aggregate_user_signin(
    ip="1.255.453",
    domain="apple.com",
    username="Stebe Jobs",
    failed_log_in_count= 5,
    total_log_in_count = 7,
)



pprint(db.grab_rows())




