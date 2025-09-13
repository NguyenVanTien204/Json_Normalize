import pandas as pd
from core.transformer import normalize_json
from pymongo import MongoClient

# Test the normalization with relational output
client = MongoClient("mongodb://localhost:27017/")
db = client["tmdb_data"]
collection = db["raw_movies"]

# Get one document
document = collection.find_one()

print("=== TESTING RELATIONAL NORMALIZATION ===")
data = normalize_json(document, output_format="relational")

print(f"Main records: {len(data['main'])}")
print(f"Relation tables: {len(data['relations'])}")

# Show summary of each relation table
for table_name, records in data["relations"].items():
    print(f"\n{table_name}: {len(records)} records")
    if records:
        print(f"Sample record keys: {list(records[0].keys())}")

print("\n=== TESTING LIST OUTPUT (DEFAULT) ===")
data_list = normalize_json(document, output_format="list")
print(f"Records: {len(data_list)}")
if data_list:
    print(f"Sample record keys: {list(data_list[0].keys())}")

print("\n=== TESTING DATAFRAME OUTPUT ===")
try:
    data_df = normalize_json(document, output_format="dataframe")
    print(f"DataFrame shape: {data_df.shape}")
    print(f"Columns: {list(data_df.columns)}")
except Exception as e:
    print(f"DataFrame error: {e}")

print("\n=== TESTING WITHOUT RELATION EXTRACTION ===")
data_no_rel = normalize_json(document, extract_relations=False)
print(f"Records without relations: {len(data_no_rel)}")
if data_no_rel:
    print(f"Sample record keys: {list(data_no_rel[0].keys())}")
    # Check if nested arrays are still present
    nested_fields = []
    for key, value in data_no_rel[0].items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            nested_fields.append(key)
    print(f"Nested array fields: {nested_fields}")
