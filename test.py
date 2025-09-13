from core import normalize_json, normalize_nulls

sample_obj ={
    "id": 1,
    "genres": [],
    "production_companies": [{"id": 101, "name": "Company A"}, {"id": 102, "name": "Company B"}],
  }

data = normalize_json(sample_obj, output_format="dataframe", null_value="N/A", extract_relations=True)
print(data)
