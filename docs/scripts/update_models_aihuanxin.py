#!/usr/bin/env python3
"""
Script to update model list from aihuanxin and compare with existing file
"""

import requests
import json
import os
import sys
from typing import List, Dict, Tuple, Set
from datetime import datetime
import hashlib

# Add project root directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

def get_flagos_models() -> List[Dict]:
    """
    Get all models of the 众智FlagOS organization
    """
    url = "https://aihuanxin.cn/qdlake/web-pub/aiconflux/v1/model/list"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "aihuanxin.cn",
        "Origin": "https://aihuanxin.cn",
        "Referer": "https://aihuanxin.cn/qdlake/qdh-web/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    }
    
    all_flagos_models = []
    page = 1
    page_size = 100
    max_pages = 10  # Limit to 10 pages to avoid excessive requests
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Retrieving 众智FlagOS models...")
    
    while page <= max_pages:
        payload = {"pageNum": page, "pageSize": page_size}
        
        try:
            print(f"  Fetching page {page}...")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                print(f"    Error: HTTP {response.status_code}")
                break
            
            data = response.json()
            if data.get("code") != 0:
                print(f"    API error: {data.get('msg', 'Unknown error')}")
                break
            
            models = data.get("data", {}).get("data", [])
            total_models = data.get("data", {}).get("total", 0)
            
            if not models:
                print("    No more models found")
                break
            
            # Filter for 众智FlagOS models
            page_flagos_count = 0
            for model in models:
                name = model.get("name", "")
                if "众智FlagOS/" in name:
                    all_flagos_models.append(model)
                    page_flagos_count += 1
            
            print(f"    Found {page_flagos_count} 众智FlagOS models on this page")
            
            # Check if we should continue to next page
            if len(models) < page_size or page * page_size >= total_models:
                print(f"    Reached end of list (total: {total_models} models)")
                break
                
            page += 1
            
        except requests.exceptions.Timeout:
            print(f"    Timeout on page {page}")
            break
        except Exception as e:
            print(f"    Request error on page {page}: {e}")
            break
    
    # Remove duplicates (based on ID)
    seen_ids = set()
    unique_models = []
    for model in all_flagos_models:
        model_id = model.get("id")
        if model_id and model_id not in seen_ids:
            seen_ids.add(model_id)
            unique_models.append(model)
    
    print(f"  Total unique 众智FlagOS models found: {len(unique_models)}")
    return unique_models

def generate_model_url(model_id: str) -> str:
    """
    Generate the model detail page URL based on model ID
    """
    return f"https://aihuanxin.cn/#/model?path=/model/detail/{model_id}"

def extract_model_names_from_markdown(filename: str) -> Set[str]:
    """
    Extract model names from existing Markdown file (first column)
    """
    model_names = set()
    
    if not os.path.exists(filename):
        print(f"  No existing file found: {filename}")
        return model_names
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header lines and table separator lines
        in_table = False
        for line in lines:
            line = line.strip()
            
            # Check if entering table section
            if line.startswith('| Model Name |'):
                in_table = True
                continue
            
            # If it's a table separator line, skip
            if in_table and line.startswith('|---'):
                continue
            
            # Process table rows
            if in_table and line.startswith('|'):
                # Split the line and get model name (second column, index 1)
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 3:  # At least have Model Name and Website columns
                    model_name = parts[1]
                    if model_name and not model_name.startswith('---'):
                        model_names.add(model_name)
        
        print(f"  Extracted {len(model_names)} model names from existing file")
        return model_names
        
    except Exception as e:
        print(f"  Error reading existing file: {e}")
        import traceback
        traceback.print_exc()
        return set()

def create_markdown_table(models: List[Dict]) -> Tuple[str, Set[str]]:
    """
    Create a Markdown table, sorted alphabetically
    Returns: (markdown_content, set_of_model_names)
    """
    # Process model data: extract name (remove prefix) and URL
    model_data = []
    for model in models:
        full_name = model.get("name", "")
        model_id = model.get("id", "")
        
        # Remove "众智FlagOS/" prefix
        if full_name.startswith("众智FlagOS/"):
            short_name = full_name[len("众智FlagOS/"):]
        else:
            short_name = full_name
        
        model_url = generate_model_url(model_id)
        model_data.append((short_name, model_url, model_id))
    
    # Sort by model name alphabetically (case-insensitive)
    model_data.sort(key=lambda x: x[0].lower())
    
    # Create Markdown table
    markdown = f"# Models on AI Huanxin\n\n"
    markdown += "| Model Name | Website |\n"
    markdown += "|------------|---------|\n"
    
    model_names = set()
    for short_name, model_url, model_id in model_data:
        markdown += f"| {short_name} | <{model_url}> |\n"
        model_names.add(short_name)
    
    return markdown, model_names

def compare_model_lists(current_names: Set[str], new_names: Set[str]) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Compare current and new model names
    Returns: (added_models, removed_models, unchanged_models)
    """
    added = new_names - current_names
    removed = current_names - new_names
    unchanged = current_names & new_names
    
    return added, removed, unchanged

def get_file_hash(filename: str) -> str:
    """Get MD5 hash of a file"""
    if not os.path.exists(filename):
        return ""
    
    with open(filename, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    
    return file_hash

def main():
    print(f"\n{'='*60}")
    print("Model List Update Script")
    print(f"{'='*60}")
    
    # Configuration - adjust according to your directory structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.join(script_dir, '../..')
    output_filename = os.path.join(repo_root, "docs/flagrelease_en/modle_list/model-list-aihuanxin.md")
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_filename)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get existing model names
    print(f"\n1. Reading existing model list from: {output_filename}")
    existing_names = extract_model_names_from_markdown(output_filename)
    old_hash = get_file_hash(output_filename)
    
    # Get current models from API
    print("\n2. Fetching current models from aihuanxin...")
    models = get_flagos_models()
    
    if not models:
        print("\n❌ No models retrieved from API")
        # If the API fails but we need to continue, we can use the existing file
        if os.path.exists(output_filename):
            print("  Using existing file as fallback")
            with open(output_filename, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            # Exit code 1 means no changes
            exit(1)
        else:
            exit(2)  # Exit code 2 means API failure and no existing file
    
    # Create new markdown table
    print("\n3. Creating new markdown table...")
    new_markdown, new_names = create_markdown_table(models)
    
    # Compare model lists
    print("\n4. Comparing model lists...")
    added, removed, unchanged = compare_model_lists(existing_names, new_names)
    
    print(f"   Current models: {len(existing_names)}")
    print(f"   New models: {len(new_names)}")
    print(f"   Added: {len(added)} models")
    print(f"   Removed: {len(removed)} models")
    print(f"   Unchanged: {len(unchanged)} models")
    
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
        
        # Write new file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_markdown)
        
        print(f"   ✓ File updated successfully")
        
        # Create change log file
        summary_filename = os.path.join(script_dir, "model-update-summary.txt")
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(f"Model List Update Summary\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total models: {len(new_names)}\n")
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
        
        # Exit with code 0 indicating changes
        exit(0)
    else:
        print(f"\n5. No changes detected. File {output_filename} is up to date.")
        
        # Exit with code 1 indicating no changes
        exit(1)

if __name__ == "__main__":
    main()
