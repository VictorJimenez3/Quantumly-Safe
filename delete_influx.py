#influxdb does not support None/null values
import influxdb_client, os, time
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

token = os.getenv("INFLUXDB_TOKEN")

org = "Q-Safe"
url = "http://localhost:8086"
bucket="Bucket"


write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
  #all data per column
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="Q-Safe", record=point) #add to bucket
  time.sleep(5) # separate points by 1 second

query_api = write_client.query_api()

query = """from(bucket: "Bucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")
 |> filter(fn: (r) => r._field == "field1")
"""
tables = query_api.query(query, org="Q-Safe")

for table in tables:
    for record in table.records:
        print(f"📌 Time: {record.get_time()}, Value: {record.get_value()}")


query_api = write_client.query_api()

query = """from(bucket: "Bucket")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> filter(fn: (r) => r._field == "field1")
  |> mean()
"""
tables = query_api.query(query, org="Q-Safe")

for table in tables:
    for record in table.records:
        print(record)
