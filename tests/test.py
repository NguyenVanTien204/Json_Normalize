import pandas as pd
from core.transformer import normalize_json
from pymongo import MongoClient


# Kết nối tới MongoDB (thay connection string nếu cần)
client = MongoClient("mongodb://localhost:27017/")

# Chọn database và collection
db = client["tmdb_data"]
collection = db["raw_movies"]

# Lấy ra một bản ghi bất kỳ
document = collection.find_one() # Giống file test.json

data = normalize_json(document, output_format="relational")
print("Main record:")
print(data["main"])
print("\nRelations:")
for table_name, records in data["relations"].items():
    print(f"\n{table_name}:")
    for record in records[:3]:  # Show first 3 records
        print(record)
