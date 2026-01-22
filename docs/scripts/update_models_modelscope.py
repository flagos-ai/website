#!/usr/bin/env python3
"""
Automatically fetch the list of all models for the FlagRelease organization via the ModelScope official API.
Generate a markdown table with model names and URLs.
"""

import requests
import json
import time
import os
import hashlib
from typing import List, Set, Dict
from datetime import datetime
from collections import Counter

def fetch_all_models() -> List[str]:
    """
    Fetch all models for the FlagRelease organization from ModelScope
    Returns a list of model IDs (with FlagRelease/ prefix)
    """
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
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting to fetch model list from ModelScope...")
    
    while page <= 50:  # Safety upper limit
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
                            if current_page_count <= 3:  # Print only the first 3 per page to avoid clutter
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

def generate_model_url(model_id: str) -> str:
    """
    Generate the model detail page URL based on model ID
    ModelScope URL format: https://modelscope.cn/models/{model_id}
    """
    return f"https://modelscope.cn/models/{model_id}"

def extract_model_names_from_markdown(filename: str) -> Set[str]:
    """
    Extract model names from existing Markdown file (first column)
    """
    model_names = set()
    
    if not os.path.exists(filename):
        return model_names
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header lines
        for line in lines:
            line = line.strip()
            if line.startswith('|') and '---' not in line and 'Website' not in line:
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 2:
                    model_name = parts[1]
                    if model_name:
                        model_names.add(model_name)
        
        return model_names
        
    except Exception:
        return set()

def create_markdown_table(models: List[str]) -> str:
    """
    Create a Markdown table, sorted alphabetically
    Returns: markdown_content
    """
    # Process model data: remove "FlagRelease/" prefix and generate URL
    model_data = []
    for model_id in models:
        # Remove "FlagRelease/" prefix
        if model_id.startswith('FlagRelease/'):
            short_name = model_id[len('FlagRelease/'):]
        else:
            short_name = model_id
        
        model_url = generate_model_url(model_id)
        model_data.append((short_name, model_url))
    
    # Sort by model name alphabetically (case-insensitive)
    model_data.sort(key=lambda x: x[0].lower())
    
    # Create Markdown table
    markdown = f"# Models on ModelScope\n\n"
    markdown += "| Model Name | Website |\n"
    markdown += "|------------|---------|\n"
    
    for short_name, model_url in model_data:
        markdown += f"| {short_name} | <{model_url}> |\n"
    
    return markdown

def get_file_hash(filename: str) -> str:
    """Get MD5 hash of a file"""
    if not os.path.exists(filename):
        return ""
    
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    """
    Main function to update model list from ModelScope
    """
    print(f"\n{'='*60}")
    print("ModelScope Model List Update Script")
    print(f"{'='*60}")
    
    # Configuration - output file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, '../flagrelease_en/modle_list/model-list-modelscope.md')
    
    # Get existing model names
    print(f"\n1. Reading existing model list from: {output_filename}")
    existing_names = extract_model_names_from_markdown(output_filename)
    old_hash = get_file_hash(output_filename)
    
    # Get current models from ModelScope API
    print("\n2. Fetching current models from ModelScope...")
    models = fetch_all_models()
    
    if not models:
        print("\n❌ No models retrieved from ModelScope API")
        # If API fails but we have an existing file, we can use it
        if os.path.exists(output_filename):
            print("  Using existing file as fallback")
            exit(1)  # Exit code 1 means no changes (API failed but file exists)
        else:
            exit(2)  # Exit code 2 means API failure and no existing file
    
    # Create new markdown table
    print("\n3. Creating new markdown table...")
    new_markdown = create_markdown_table(models)
    
    # Get model names from new markdown
    new_names = extract_model_names_from_markdown(output_filename)
    
    # Compare model lists
    print("\n4. Comparing model lists...")
    added = new_names - existing_names
    removed = existing_names - new_names
    
    print(f"   Current models: {len(existing_names)}")
    print(f"   New models: {len(new_names)}")
    print(f"   Added: {len(added)} models")
    print(f"   Removed: {len(removed)} models")
    
    if added:
        print(f"\n   New models detected:")
        for i, model in enumerate(sorted(added), 1):
            print(f"     {i:2d}. {model}")
    
    if removed:
        print(f"\n   Removed models:")
        for i, model in enumerate(sorted(removed), 1):
            print(f"     {i:2d}. {model}")
    
    # Check if we need to update the file
    new_hash = hashlib.md5(new_markdown.encode('utf-8')).hexdigest()
    
    if old_hash != new_hash:
        print(f"\n5. Changes detected. Updating {output_filename}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        # Write new file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_markdown)
        
        print(f"   ✓ File updated successfully")
        
        # Create a summary file
        summary_filename = os.path.join(script_dir, "modelscope-update-summary.txt")
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(f"ModelScope Model List Update Summary\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total models: {len(models)}\n")
            f.write(f"New models added: {len(added)}\n")
            f.write(f"Models removed: {len(removed)}\n\n")
            
            if added:
                f.write("New Models:\n")
                for model in sorted(added):
                    f.write(f"- {model}\n")
                f.write("\n")
            
            if removed:
                f.write("Removed Models:\n")
                for model in sorted(removed):
                    f.write(f"- {model}\n")
        
        print(f"   Summary written to {summary_filename}")
        
        # Simple statistics
        unique_models = sorted(set(models))
        series_counter = Counter()
        for model in unique_models:
            short_name = model.replace('FlagRelease/', '')
            series = short_name.split('-')[0] if '-' in short_name else short_name[:10]
            series_counter[series] += 1
        
        print(f"\n6. Statistics:")
        print(f"   Total of {len(series_counter)} different model series.")
        
        # Exit with code 0 indicating changes
        exit(0)
    else:
        print(f"\n5. No changes detected. File {output_filename} is up to date.")
        
        # Exit with code 1 indicating no changes
        exit(1)

if __name__ == "__main__":
    main()
