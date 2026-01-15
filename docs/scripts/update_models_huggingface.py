#!/usr/bin/env python3
"""
Fetch all models from FlagRelease organization on HuggingFace and generate a markdown table.
"""

import requests
import json
import os
import hashlib
from typing import List, Set
from datetime import datetime
import time

def fetch_all_models() -> List[str]:
    """
    Fetch all models for the FlagRelease organization from HuggingFace
    Returns a list of model IDs
    """
    base_url = "https://huggingface.co/api/models"
    all_models = []
    limit = 100  # HuggingFace API每页最大限制
    offset = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://huggingface.co/FlagRelease',
    }
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting to fetch model list from HuggingFace...")
    print(f"  Organization: FlagRelease")
    
    while True:
        params = {
            'author': 'FlagRelease',
            'limit': limit,
            'offset': offset,
            'full': 'true',  # 获取完整信息
            'sort': 'downloads',  # 按下载量排序
            'direction': '-1',  # 降序
        }
        
        try:
            print(f"  Fetching batch (offset: {offset}, limit: {limit})...")
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"    HTTP Error: {response.status_code}")
                break
            
            models = response.json()
            
            if not models:
                print("    No more models found")
                break
            
            current_batch_count = 0
            for model in models:
                model_id = model.get('id')
                if model_id and model_id.startswith('FlagRelease/'):
                    all_models.append(model_id)
                    current_batch_count += 1
                    
                    if current_batch_count <= 3:  # 只打印前3个，避免输出太长
                        downloads = model.get('downloads', 0)
                        likes = model.get('likes', 0)
                        print(f"      Found: {model_id} (Downloads: {downloads}, Likes: {likes})")
            
            print(f"    Batch {offset//limit + 1} extracted {current_batch_count} models")
            
            # 检查是否还有更多数据
            if len(models) < limit:
                print(f"    Reached end of list")
                break
            
            offset += limit
            time.sleep(1)  # 避免请求过于频繁
            
        except requests.exceptions.Timeout:
            print(f"    Timeout on batch {offset//limit + 1}")
            break
        except Exception as e:
            print(f"    Error: {type(e).__name__}: {e}")
            break
    
    # 去重（虽然API返回的应该不会重复，但为了安全）
    unique_models = []
    seen = set()
    for model in all_models:
        if model not in seen:
            seen.add(model)
            unique_models.append(model)
    
    print(f"  Total unique models found: {len(unique_models)}")
    return unique_models

def fetch_all_models_alternative() -> List[str]:
    """
    备用方法：使用HuggingFace的搜索API获取模型
    这个方法可能更稳定，但需要处理分页
    """
    all_models = []
    page = 1
    page_size = 50
    
    print(f"\n  Trying alternative method...")
    
    while True:
        url = f"https://huggingface.co/api/models"
        params = {
            'search': 'FlagRelease',
            'limit': page_size,
            'skip': (page - 1) * page_size,
            'sort': 'downloads',
            'direction': '-1',
        }
        
        try:
            print(f"    Fetching page {page}...")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"      HTTP Error: {response.status_code}")
                break
            
            models = response.json()
            
            if not models:
                print("      No more models found")
                break
            
            current_page_count = 0
            for model in models:
                model_id = model.get('modelId') or model.get('id')
                if model_id and model_id.startswith('FlagRelease/'):
                    if model_id not in all_models:
                        all_models.append(model_id)
                        current_page_count += 1
            
            print(f"      Page {page} extracted {current_page_count} new models")
            
            if len(models) < page_size:
                print(f"      Reached end of list")
                break
            
            page += 1
            time.sleep(0.5)  # 礼貌延迟
            
        except Exception as e:
            print(f"      Error: {e}")
            break
    
    return all_models

def generate_model_url(model_id: str) -> str:
    """
    Generate the model detail page URL based on model ID
    HuggingFace URL format: https://huggingface.co/{model_id}
    """
    return f"https://huggingface.co/{model_id}"

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
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    markdown = f"# Model on HuggingFace\n\n"
    markdown += f"*Last updated: {current_time}*\n\n"
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

def get_model_details(model_id: str):
    """
    获取模型的详细信息（可选，用于调试）
    """
    url = f"https://huggingface.co/api/models/{model_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def main():
    """
    Main function to update model list from HuggingFace
    """
    print(f"\n{'='*60}")
    print("HuggingFace Model List Update Script")
    print(f"{'='*60}")
    
    # Configuration - output file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, '../flagrelease_en/modle-list/model-list-huggingface.md')
    
    # Get existing model names
    print(f"\n1. Reading existing model list from: {output_filename}")
    existing_names = extract_model_names_from_markdown(output_filename)
    old_hash = get_file_hash(output_filename)
    
    # Get current models from HuggingFace API
    print("\n2. Fetching current models from HuggingFace...")
    models = fetch_all_models()
    
    # 如果主方法没有获取到数据，尝试备用方法
    if not models:
        print("\n  Primary method failed, trying alternative method...")
        models = fetch_all_models_alternative()
    
    if not models:
        print("\n❌ No models retrieved from HuggingFace API")
        # 如果API失败但已有现有文件，我们可以使用它
        if os.path.exists(output_filename):
            print("  Using existing file as fallback")
            exit(1)  # 退出码1表示无变化（API失败但文件存在）
        else:
            exit(2)  # 退出码2表示API失败且无现有文件
    
    # Create new markdown table
    print("\n3. Creating new markdown table...")
    new_markdown = create_markdown_table(models)
    
    # 从新markdown中提取模型名称（为了与现有文件比较）
    # 这里我们直接使用models列表来获取模型名称（去掉前缀）
    new_names = set()
    for model_id in models:
        if model_id.startswith('FlagRelease/'):
            short_name = model_id[len('FlagRelease/'):]
        else:
            short_name = model_id
        new_names.add(short_name)
    
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
    
    # 获取一些统计信息（可选）
    print("\n5. Fetching some model statistics...")
    sample_models = models[:5]  # 只获取前5个模型的详细信息作为示例
    for model_id in sample_models:
        details = get_model_details(model_id)
        if details:
            downloads = details.get('downloads', 0)
            likes = details.get('likes', 0)
            short_name = model_id.split('/')[-1]
            print(f"   {short_name}: {downloads} downloads, {likes} likes")
    
    # Check if we need to update the file
    new_hash = hashlib.md5(new_markdown.encode('utf-8')).hexdigest()
    
    if old_hash != new_hash:
        print(f"\n6. Changes detected. Updating {output_filename}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        # Write new file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_markdown)
        
        print(f"   ✓ File updated successfully")
        
        # Create a summary file
        summary_filename = os.path.join(script_dir, "huggingface-update-summary.txt")
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write(f"HuggingFace Model List Update Summary\n")
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
        
        # Exit with code 0 indicating changes
        exit(0)
    else:
        print(f"\n6. No changes detected. File {output_filename} is up to date.")
        
        # Exit with code 1 indicating no changes
        exit(1)

if __name__ == "__main__":
    main()
