"""
Example: Relational Normalization with Complex JSON

This example demonstrates how to normalize complex JSON data with nested arrays
of objects, automatically extracting them into separate relational tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.transformer import normalize_json

# Complex movie data with nested arrays
movie_data = {
    "id": 550,
    "title": "Fight Club",
    "genres": [
        {"id": 18, "name": "Drama"},
        {"id": 53, "name": "Thriller"}
    ],
    "production_companies": [
        {"id": 711, "name": "Fox 2000 Pictures", "origin_country": "US"},
        {"id": 508, "name": "Regency Enterprises", "origin_country": "US"}
    ],
    "production_countries": [
        {"iso_3166_1": "DE", "name": "Germany"},
        {"iso_3166_1": "US", "name": "United States of America"}
    ],
    "spoken_languages": [
        {"english_name": "English", "iso_639_1": "en", "name": "English"}
    ],
    "videos": {
        "results": [
            {
                "id": "video1",
                "key": "trailer_key",
                "name": "Official Trailer",
                "site": "YouTube",
                "type": "Trailer"
            },
            {
                "id": "video2",
                "key": "featurette_key",
                "name": "Making Of",
                "site": "YouTube",
                "type": "Featurette"
            }
        ]
    },
    "budget": 63000000,
    "revenue": 100853753
}

def main():
    print("=== RELATIONAL NORMALIZATION EXAMPLE ===\n")

    # Normalize with relational output
    result = normalize_json(movie_data, output_format="relational")

    print("MAIN RECORD:")
    for record in result["main"]:
        for key, value in record.items():
            print(f"  {key}: {value}")
        print()

    print("EXTRACTED RELATIONS:")
    for table_name, records in result["relations"].items():
        print(f"\n{table_name} ({len(records)} records):")
        for i, record in enumerate(records):
            print(f"  Record {i+1}: {record}")

    print("\n" + "="*50)
    print("COMPARISON: WITHOUT RELATION EXTRACTION")
    print("="*50)

    # Compare with non-relational output
    simple_result = normalize_json(movie_data, extract_relations=False)
    print("\nSimple output (nested arrays preserved):")
    for record in simple_result:
        nested_fields = []
        for key, value in record.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                nested_fields.append(key)
        print(f"  Nested array fields: {nested_fields}")
        break

if __name__ == "__main__":
    main()
