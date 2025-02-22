#this code is making a table based off json data. 
#you run influxd in your file path to the download area of influxdb
# then you go to http://localhost:8086, Data Explorer
# be on script editor, then click paramters you want to see on the table, choose simple table, and also raw data
# the issue is i does not format the data correct 
# it also does each individual query as a column, instead of one per chase, u need SQL to fix that, and it hasn't been working for me


import os
import time
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

# Load environment variables from .env file (ensure INFLUXDB_TOKEN is set)
load_dotenv()

# Environment and connection settings
token = os.getenv("INFLUXDB_TOKEN")
org = "Q-Safe"
url = "http://localhost:8086"
bucket = "TestingHardCodedData"

# Create the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Delete and recreate the bucket to start fresh
buckets_api = client.buckets_api()
try:
    bucket_obj = buckets_api.find_bucket_by_name(bucket)
    bucket_id = bucket_obj.id
    buckets_api.delete_bucket(bucket_id)
    print(f"Deleted existing bucket: {bucket}")
except Exception as e:
    print(f"Bucket {bucket} not found or already deleted. Error: {e}")

buckets_api.create_bucket(bucket_name=bucket, org=org)
print(f"Created new bucket: {bucket}")

# Create write and delete APIs
write_api = client.write_api(write_options=SYNCHRONOUS)
delete_api = client.delete_api()

# Delete any prior data for measurement "cybersec_data" (if needed)
delete_api.delete(
    start="1970-01-01T00:00:00Z",
    stop="2025-01-01T00:00:00Z",
    predicate='_measurement="cybersec_data"',
    bucket=bucket,
    org=org
)

# Hardcoded JSON data (each dictionary represents one row)
hardcoded_data = [
    {
        "session_id": "session_1",
        "network_packet_size": 1200,
        "protocol_type": "TCP",
        "login_attempts": 2,
        "session_duration": 75.5,
        "encryption_used": 1,           # 1 means True
        "ip_reputation_score": 85.0,
        "failed_logins": 0,
        "browser_type": "Chrome",
        "unusual_time_access": 0,       # 0 means False
        "attack_detected": 0            
    },
    {
        "session_id": "session_2",
        "network_packet_size": 1500,
        "protocol_type": "UDP",
        "login_attempts": 1,
        "session_duration": 60.0,
        "encryption_used": 0,
        "ip_reputation_score": 90.0,
        "failed_logins": 1,
        "browser_type": "Firefox",
        "unusual_time_access": 1,
        "attack_detected": 1
    },
    {
        "session_id": "session_3",
        "network_packet_size": 2000,
        "protocol_type": "TCP",
        "login_attempts": 3,
        "session_duration": 90.0,
        "encryption_used": 1,
        "ip_reputation_score": 70.5,
        "failed_logins": 2,
        "browser_type": "Edge",
        "unusual_time_access": 0,
        "attack_detected": 1
    }
]

# Print the hardcoded JSON data (for verification)
print("Hardcoded JSON Data:")
print(json.dumps(hardcoded_data, indent=2))

# Write each data point into InfluxDB.
# Use tags for session_id, protocol_type, and browser_type and fields for the stats.
for row in hardcoded_data:
    point = (
        Point("cybersec_data")
        .tag("session_id", row["session_id"])
        .tag("protocol_type", row["protocol_type"])
        .tag("browser_type", row["browser_type"])
        .field("network_packet_size", row["network_packet_size"])
        .field("login_attempts", row["login_attempts"])
        .field("session_duration", row["session_duration"])
        .field("encryption_used", row["encryption_used"])
        .field("ip_reputation_score", row["ip_reputation_score"])
        .field("failed_logins", row["failed_logins"])
        .field("unusual_time_access", row["unusual_time_access"])
        .field("attack_detected", row["attack_detected"])
    )
    try:
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Written data for session: {row['session_id']}")
    except Exception as e:
        print(f"Error writing data for session: {row['session_id']} - {e}")
    time.sleep(1)  # Optional: Delay to ensure proper write ordering

# Now run a Flux query to pivot the data into a wide table with exactly 11 columns.
query_api = client.query_api()

# This Flux query does the following:
#   1. Selects data from the "cybersec_data" measurement.
#   2. Pivots the tall _field/_value data into a wide format.
#   3. Renames columns to exactly match your desired output.
#   4. Keeps only the 11 columns (in your chosen order).
flux_query = f'''
from(bucket: "{bucket}")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "cybersec_data")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> rename(columns: {{
      "session_id": "id",
      "network_packet_size": "network_packet",
      "encryption_used": "encryption",
      "ip_reputation_score": "ip reputation score",
      "failed_logins": "failed logins",
      "unusual_time_access": "unusual time access",
      "attack_detected": "attack detected"
  }})
  |> keep(columns: [
      "id",
      "network_packet",
      "protocol_type",
      "login_attempts",
      "session_duration",
      "encryption",
      "ip reputation score",
      "failed logins",
      "browser_type",
      "unusual time access",
      "attack detected"
  ])
  |> rename(columns: {{
      "browser_type": "browser"  // Rename browser_type to browser in the final output
  }})
'''

print("\nPivoted Wide Table Results:")
try:
    tables = query_api.query(flux_query, org=org)
    # Loop through each record and print its values
    for table in tables:
        for record in table.records:
            # The record.values dictionary should now contain exactly 11 keys.
            print(record.values)
except Exception as e:
    print(f"Error querying data: {e}")

# Optionally, use Pandas to load the data into a DataFrame for a prettier display.
try:
    import pandas as pd
    df = query_api.query_data_frame(query=flux_query, org=org)
    print("\nDataFrame Output:")
    print(df)
except ImportError:
    print("Pandas is not installed. Install it with 'pip install pandas' if needed.")
except Exception as e:
    print(f"Error loading data into DataFrame: {e}")
