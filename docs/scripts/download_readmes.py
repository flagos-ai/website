#!/usr/bin/env python3
"""
For your directory structure: Read model list from docs/flagrelease_en directory,
and download files to docs/flagrelease_en/model_readmes/
"""

import os
import sys
import shutil

from modelscope.hub.snapshot_download import snapshot_download

def download_models():
    """Download all model readme files to the specified directory"""
    # 1. Get absolute path of script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    
    # 2. Construct project root path (assuming script is in docs/scripts/)
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    print(f"Project root directory: {project_root}")
    
    # 3. Model list file path
    list_file = os.path.join(project_root, 'docs', 'flagrelease_en', 'model_list.txt')
    print(f"Model list file path: {list_file}")
    
    if not os.path.exists(list_file):
        print(f"❌ Error: Cannot find model list file '{list_file}'")
        print(f"Current working directory: {os.getcwd()}")
        sys.exit(1)
    
    # 4. Read model list
    with open(list_file, 'r', encoding='utf-8') as f:
        model_ids = [line.strip() for line in f 
                    if line.strip() and not line.startswith('#')]
    
    print(f"📋 Found {len(model_ids)} models to process")
    
    # 5. Output directory
    output_dir = os.path.join(project_root, 'docs', 'flagrelease_en', 'model_readmes')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    success_count = 0
    failed_models = []
    
    for idx, model_id in enumerate(model_ids, 1):
        print(f"\n[{idx}/{len(model_ids)}] 🔍 Processing: {model_id}")
        
        try:
            # Create temporary directory
            safe_name = model_id.replace('/', '_')
            temp_dir = os.path.join('/tmp', f"modelscope_{safe_name}")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download readme files
            snapshot_download(
                model_id=model_id,
                allow_patterns=['*README.md', '*readme.md'],
                local_dir=temp_dir,
                local_files_only=False
            )
            
            # Find and copy readme file
            found = False
            for possible_name in ['README.md', 'readme.md']:
                source_path = os.path.join(temp_dir, possible_name)
                if os.path.exists(source_path):
                    target_filename = f"{safe_name}.md"
                    target_path = os.path.join(output_dir, target_filename)
                    shutil.copy2(source_path, target_path)
                    print(f"   ✅ Saved: {target_filename}")
                    success_count += 1
                    found = True
                    break
            
            if not found:
                print(f"   ⚠️  No readme file found")
                failed_models.append(f"{model_id} (file not found)")
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        except Exception as e:
            print(f"   ❌ Download failed: {str(e)}")
            failed_models.append(f"{model_id} (error: {str(e)[:50]})")
    
    # Generate summary report
    print("\n" + "="*50)
    print("📊 Download Summary")
    print("="*50)
    print(f"Success: {success_count}/{len(model_ids)}")
    if failed_models:
        print(f"Failed: {len(failed_models)}")
        for failed in failed_models:
            print(f"  - {failed}")
    
    # 6. List downloaded files
    if os.path.exists(output_dir):
        downloaded_files = os.listdir(output_dir)
        print(f"\n📄 Downloaded files ({len(downloaded_files)} items):")
        for f in sorted(downloaded_files):
            if f.endswith('.md'):
                print(f"  - {f}")
    
    return success_count > 0

if __name__ == "__main__":
    try:
        print("="*50)
        print("🚀 Starting ModelScope model documentation download")
        print("="*50)
        
        success = download_models()
        
        if success:
            print("\n🎉 Download task completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️ Download task completed with some failures")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Script execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)