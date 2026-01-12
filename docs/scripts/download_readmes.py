#!/usr/bin/env python3
"""
针对你的目录结构：从docs/flagrelease_en目录读取模型列表，
并将文件下载到docs/flagrelease_en/model_readmes/
"""

import os
import sys
import shutil
from modelscope.hub.snapshot_download import snapshot_download

def download_models():
    """下载所有模型的readme文件到指定目录"""
    # 1. 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"脚本目录: {script_dir}")
    
    # 2. 构建项目根目录路径（假设脚本在 docs/scripts/）
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    print(f"项目根目录: {project_root}")
    
    # 3. 模型列表文件路径
    list_file = os.path.join(project_root, 'docs', 'flagrelease_en', 'model_list.txt')
    print(f"模型列表文件路径: {list_file}")
    
    if not os.path.exists(list_file):
        print(f"❌ 错误：找不到模型列表文件 '{list_file}'")
        print(f"当前工作目录: {os.getcwd()}")
        sys.exit(1)
    
    # 4. 读取模型列表
    with open(list_file, 'r', encoding='utf-8') as f:
        model_ids = [line.strip() for line in f 
                    if line.strip() and not line.startswith('#')]
    
    print(f"📋 找到 {len(model_ids)} 个模型需要处理")
    
    # 5. 输出目录
    output_dir = os.path.join(project_root, 'docs', 'flagrelease_en', 'model_readmes')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 输出目录: {output_dir}")
    
    success_count = 0
    failed_models = []
    
    for idx, model_id in enumerate(model_ids, 1):
        print(f"\n[{idx}/{len(model_ids)}] 🔍 处理: {model_id}")
        
        try:
            # 创建临时目录
            safe_name = model_id.replace('/', '_')
            temp_dir = os.path.join('/tmp', f"modelscope_{safe_name}")
            os.makedirs(temp_dir, exist_ok=True)
            
            # 下载readme文件
            snapshot_download(
                model_id=model_id,
                allow_patterns=['*README.md', '*readme.md'],
                local_dir=temp_dir,
                local_files_only=False
            )
            
            # 查找并复制readme文件
            found = False
            for possible_name in ['README.md', 'readme.md']:
                source_path = os.path.join(temp_dir, possible_name)
                if os.path.exists(source_path):
                    target_filename = f"{safe_name}.md"
                    target_path = os.path.join(output_dir, target_filename)
                    shutil.copy2(source_path, target_path)
                    print(f"   ✅ 已保存: {target_filename}")
                    success_count += 1
                    found = True
                    break
            
            if not found:
                print(f"   ⚠️  未找到readme文件")
                failed_models.append(f"{model_id} (未找到文件)")
            
            # 清理临时目录
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        except Exception as e:
            print(f"   ❌ 下载失败: {str(e)}")
            failed_models.append(f"{model_id} (错误: {str(e)[:50]})")
    
    # 生成总结报告
    print("\n" + "="*50)
    print("📊 下载总结")
    print("="*50)
    print(f"成功: {success_count}/{len(model_ids)}")
    if failed_models:
        print(f"失败: {len(failed_models)}")
        for failed in failed_models:
            print(f"  - {failed}")
    
    # 6. 列出下载的文件
    if os.path.exists(output_dir):
        downloaded_files = os.listdir(output_dir)
        print(f"\n📄 已下载的文件 ({len(downloaded_files)}个):")
        for f in sorted(downloaded_files):
            if f.endswith('.md'):
                print(f"  - {f}")
    
    return success_count > 0

if __name__ == "__main__":
    try:
        print("="*50)
        print("🚀 开始下载ModelScope模型文档")
        print("="*50)
        
        success = download_models()
        
        if success:
            print("\n🎉 下载任务完成！")
            sys.exit(0)
        else:
            print("\n⚠️ 下载任务完成，但有部分失败")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 脚本执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)