import pandas as pd
import chardet

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(100000))  # Read first 100,000 bytes
        return result['encoding']

# Function to read CSV with detected encoding
def read_csv_with_encoding(file_path):
    encoding = detect_encoding(file_path)
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        print(f"❌ Encoding {encoding} failed for {file_path}, trying alternative encodings...")
        return pd.read_csv(file_path, encoding="ISO-8859-1")  # Fallback encoding

# List of datasets to process
datasets = [
    ("Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv", "DDoS"),
    ("Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv", "PortScan"),
    ("Friday-WorkingHours-Morning.pcap_ISCX.csv", "Bot"),
    ("Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv", "Infiltration"),
    ("Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv", [
        "Web Attack ñ Brute Force",
        "Web Attack ñ XSS",
        "Web Attack ñ Sql Injection"
    ]),
    ("Tuesday-WorkingHours.pcap_ISCX.csv", ["FTP-Patator", "SSH-Patator"]),
    ("Wednesday-workingHours.pcap_ISCX.csv", [  # New dataset added
        "DoS slowloris",
        "DoS Slowhttptest",
        "DoS Hulk",
        "DoS GoldenEye",
        "Heartbleed"
    ])
]

output_file = "attacker_ip.csv"
all_attacker_ips = pd.DataFrame(columns=["Source IP", "Label"])

for dataset, attack_type in datasets:
    df = read_csv_with_encoding(dataset)
    if df is None:
        print(f"Skipping {dataset} due to encoding issues.")
        continue

    # Standardize column names
    df.columns = df.columns.str.strip()

    print(f"Processing {dataset} with detected encoding. Columns: {df.columns}")  # Debugging

    if "Label" not in df.columns or "Source IP" not in df.columns:
        print(f"❌ Required columns not found in {dataset}. Skipping...")
        continue

    # Handle multiple attack types (Web Attacks, Patator Attacks, DoS Attacks)
    if isinstance(attack_type, list):
        df_filtered = df[df["Label"].isin(attack_type)]
    else:
        df_filtered = df[df["Label"] == attack_type]

    df_selected = df_filtered[["Source IP", "Label"]]
    all_attacker_ips = pd.concat([all_attacker_ips, df_selected])

# Remove duplicates based on BOTH "Source IP" and "Label"
all_attacker_ips = all_attacker_ips.drop_duplicates(subset=["Source IP", "Label"])

# Merge with existing file if it exists
try:
    existing_df = pd.read_csv(output_file, usecols=["Source IP", "Label"])
    final_df = pd.concat([existing_df, all_attacker_ips]).drop_duplicates(subset=["Source IP", "Label"])
except FileNotFoundError:
    final_df = all_attacker_ips

# Save the cleaned dataset
final_df[["Source IP", "Label"]].to_csv(output_file, index=False, encoding="utf-8")

print("✅ Updated attacker_ip.csv successfully!")
print(f"📊 Unique Attacker IPs Count: {final_df.shape[0]}")
