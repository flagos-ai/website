#!/usr/bin/env python3
"""
Automatically fetch the list of all models for the FlagRelease organization via the ModelScope official API.
Version: 2.1 (Enhanced detection, compatible with both dictionary and list types for the Model field)
"""

import requests
import json
import time
import os
from collections import Counter

def fetch_all_models():
    url = "https://modelscope.cn/api/v1/dolphin/models"
    all_models = []
    page = 1
    page_size = 20
    
    payload_template = {
        "PageSize": page_size,
        "PageNumber": 1,
        "SortBy": "GmtModified",
        "Name": "",
        "IncludePrePublish": True,
        "Criterion": [{"category": "organizations", "predicate": "contains", "values": ["FlagRelease"]}]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://modelscope.cn/organization/FlagRelease?tab=model',
        'Origin': 'https://modelscope.cn',
    }
    
    print(f"Starting to fetch model list ({page_size} per page)...")
    
    while page <= 50: # Safety upper limit
        payload_template["PageNumber"] = page
        try:
            print(f"  Fetching page {page}...")
            resp = requests.put(url, headers=headers, data=json.dumps(payload_template), timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            # 1. Check basic response structure
            if data.get('Code') not in [200, '200']:
                print(f"    Abnormal response code: {data.get('Code')} - {data.get('Message')}")
                break
            
            data_field = data.get('Data', {})
            if not isinstance(data_field, dict):
                print(f"    The 'Data' field is not a dictionary: {type(data_field)}")
                break
            
            # 2. Core: Intelligently parse the 'Model' field
            model_container = data_field.get('Model')
            items_to_process = []
            
            if isinstance(model_container, list):
                print(f"    The 'Model' field is a list, length: {len(model_container)}")
                items_to_process = model_container
            elif isinstance(model_container, dict):
                print(f"    The 'Model' field is a dictionary, its keys: {list(model_container.keys())}")
                # Try to find a list within this dictionary
                possible_list_keys = ['Items', 'Models', 'List', 'records', 'data', 'hits']
                found = False
                for key in possible_list_keys:
                    if key in model_container and isinstance(model_container[key], list):
                        items_to_process = model_container[key]
                        print(f"      Found a list in Model['{key}'], length: {len(items_to_process)}")
                        found = True
                        break
                if not found:
                    print("      Warning: No common list field found in the Model dictionary.")
            else:
                print(f"    Unexpected type for 'Model' field: {type(model_container)}")
            
            # 3. Process the found model entries
            current_page_count = 0
            if items_to_process:
                for item in items_to_process:
                    model_id = None
                    if isinstance(item, dict):
                        # Try multiple possible field names
                        model_id = item.get('model_id') or item.get('ModelId') or item.get('id')
                        if not model_id and item.get('Name'):
                            org = item.get('Organization', {}).get('Name', 'FlagRelease')
                            model_id = f"{org}/{item['Name']}"
                    
                    if model_id:
                        if not model_id.startswith('FlagRelease/'):
                            model_id = f"FlagRelease/{model_id}"
                        if model_id not in all_models:
                            all_models.append(model_id)
                            current_page_count += 1
                            if current_page_count <= 3: # Print only the first 3 per page to avoid clutter
                                print(f"      Found: {model_id}")
                print(f"    Page {page} extracted {current_page_count} new models.")
            else:
                print(f"    Page {page} has no processable model entries.")
            
            # 4. Pagination judgment
            if current_page_count < page_size:
                print(f"    Reached the last page (items on this page {current_page_count} < {page_size}), stopping pagination.")
                break
                
            page += 1
            time.sleep(0.3)
            
        except Exception as e:
            print(f"  Error processing page {page}: {type(e).__name__}: {e}")
            break
    
    return all_models

if __name__ == '__main__':
    print("=" * 60)
    print("FlagRelease Organization Model List Fetcher v2.1 (Enhanced Detection)")
    print("=" * 60)
    models = fetch_all_models()
    
    if not models:
        print("\nWarning: Failed to fetch models. Please run diagnostics or check network.")
    else:
        unique_models = sorted(set(models))
        print(f"\nSuccessfully fetched {len(unique_models)} unique models.")
        
        # Save the file (adjust the path according to your project structure)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.normpath(os.path.join(script_dir, '..', 'flagrelease_en', 'model_list.txt'))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for model in unique_models:
                f.write(f"{model}\n")
        print(f"List saved to: {output_path}")
        
        # Simple statistics
        series_counter = Counter()
        for model in unique_models:
            short_name = model.replace('FlagRelease/', '')
            series = short_name.split('-')[0] if '-' in short_name else short_name[:10]
            series_counter[series] += 1
        print(f"Total of {len(series_counter)} different model series.")
