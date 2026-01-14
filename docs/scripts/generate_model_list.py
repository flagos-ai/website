#!/usr/bin/env python3
"""
Automatically generate model list for the FlagRelease organization.
"""

import os
import requests
import json

def get_flagrelease_models():
    """Fetch all models under the FlagRelease organization from ModelScope."""
    organization = "FlagRelease"
    models = []
    page = 1
    page_size = 100

    print(f"Fetching model list for organization: {organization}...")

    while True:
        # API for the organization page on ModelScope (unofficial API, but usually stable)
        url = f"https://modelscope.cn/api/v1/organization/{organization}/models"
        params = {
            "PageSize": page_size,
            "PageNumber": page
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if not data.get("Data"):
                break

            # Extract model IDs
            for item in data["Data"]:
                model_id = item.get("Name")  # Format like "FlagRelease/ModelName"
                if model_id:
                    models.append(model_id)
                    print(f"  Found: {model_id}")

            # Check if there are more pages
            total = data.get("Total", 0)
            print(f"  Page {page}, found {len(models)}/{total} models in total")

            if len(models) >= total or len(data["Data"]) < page_size:
                break

            page += 1

        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            break

    return models

def main():
    # 1. Fetch all models
    models = get_flagrelease_models()

    if not models:
        print("⚠️  No models found, keeping existing list.")
        return

    print(f"\n Found {len(models)} models in total.")

    # 2. Sort and deduplicate
    models = sorted(set(models))

    # 3. Write to file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    list_file = os.path.join(script_dir, '..', 'flagrelease_en', 'model_list.txt')

    with open(list_file, 'w', encoding='utf-8') as f:
        for model in models:
            f.write(f"{model}\n")

    print(f"📁 Model list updated to: {list_file}")

    # 4. Display statistics
    print("\n Statistics:")
    print(f"  Total models: {len(models)}")

    # Group statistics by prefix
    prefix_count = {}
    for model in models:
        # Extract the part after the organization name
        parts = model.split('/')
        if len(parts) > 1:
            prefix = parts[1].split('-')[0] if '-' in parts[1] else parts[1][:10]
            prefix_count[prefix] = prefix_count.get(prefix, 0) + 1

    print(f"  Model series: {len(prefix_count)} different series")
    for prefix, count in sorted(prefix_count.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    - {prefix}: {count} models")

if __name__ == "__main__":
    main()
