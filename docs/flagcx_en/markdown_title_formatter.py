import os
import re
import argparse
from pathlib import Path
from collections import Counter

def extract_title_text(line):
    """从Markdown标题行中提取纯文本内容（去除#号和空格）"""
    # 匹配Markdown标题语法：以#开头，后面跟着空格，然后是标题内容
    match = re.match(r'^(#{1,6})\s+(.+)$', line)
    if match:
        return match.group(2).strip()
    return None

def extract_candidate_proper_nouns_from_text(text):
    """从标题文本中提取可能是专业名词的候选词"""
    if not text:
        return []
    
    # 分割单词，考虑连字符的情况
    words = re.findall(r'\b[\w\'-]+\b', text)
    proper_noun_candidates = []
    
    for word in words:
        # 过滤掉太短的单词
        if len(word) <= 2:
            continue
            
        # 检查是否可能是专业名词（基于一些启发式规则）
        # 规则1: 全大写单词（如API, JSON, XML等）
        if word.isupper() and len(word) > 1:
            proper_noun_candidates.append(word)
        # 规则2: 首字母大写且包含大写字母的单词（如JavaScript, GitHub等）
        elif word[0].isupper() and any(c.isupper() for c in word[1:]):
            proper_noun_candidates.append(word)
        # 规则3: 包含特殊字符的常见技术术语（如C++, .NET等）
        elif re.search(r'[.+&\-]', word) and len(word) > 1:
            proper_noun_candidates.append(word)
        # 规则4: 常见的专业名词后缀
        elif any(word.lower().endswith(suffix) for suffix in ['.js', '.py', '.md', '.ts', '.go', '.java', '.cpp']):
            proper_noun_candidates.append(word)
    
    return proper_noun_candidates

def collect_all_titles_and_proper_nouns(directory, extensions):
    """收集所有标题和潜在的专业名词"""
    all_titles = []
    proper_noun_candidates = Counter()
    
    # 递归遍历目录
    for ext in extensions:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(f'.{ext}'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            for line in f:
                                title_text = extract_title_text(line)
                                if title_text:
                                    all_titles.append(title_text)
                                    # 提取潜在的专业名词
                                    candidates = extract_candidate_proper_nouns_from_text(title_text)
                                    for candidate in candidates:
                                        proper_noun_candidates[candidate] += 1
                    except Exception as e:
                        print(f"读取文件 {filepath} 时出错: {e}")
    
    return all_titles, proper_noun_candidates

def filter_proper_nouns(candidates_counter, min_frequency=1, min_length=2):
    """过滤专业名词候选词"""
    proper_nouns = []
    
    for candidate, freq in candidates_counter.most_common():
        # 过滤条件
        if (freq >= min_frequency and 
            len(candidate) >= min_length and
            # 排除一些常见非专业名词
            not candidate.lower() in ['the', 'and', 'for', 'with', 'that', 'this', 'from', 'have', 'been']):
            
            # 规范化专业名词的格式
            if candidate.isupper():
                # 全大写保持原样
                proper_nouns.append(candidate)
            elif candidate[0].isupper():
                # 首字母大写的保留
                proper_nouns.append(candidate)
            else:
                # 其他情况首字母大写
                proper_nouns.append(candidate.capitalize())
    
    return proper_nouns

def to_sentence_case(text, proper_nouns):
    """将文本转换为sentence case，但保留专业名词的原始大小写"""
    if not text:
        return text
    
    # 将文本拆分成单词
    words = text.split()
    processed_words = []
    
    for i, word in enumerate(words):
        # 清理单词中的标点符号，但保留原始单词
        clean_word = re.sub(r'[^\w\'-]', '', word)
        
        # 检查单词是否是专业名词（忽略大小写）
        clean_word_lower = clean_word.lower()
        is_proper_noun = False
        original_proper_noun = None
        
        for proper_noun in proper_nouns:
            if proper_noun.lower() == clean_word_lower:
                is_proper_noun = True
                original_proper_noun = proper_noun
                break
        
        if is_proper_noun:
            # 如果是专业名词，保持原样
            # 需要将原始单词中的专业名词部分替换为正确的大小写形式
            # 这里我们简单地将整个单词替换为专业名词的形式
            processed_words.append(word.replace(clean_word, original_proper_noun))
        else:
            if i == 0:
                # 第一个单词首字母大写
                processed_words.append(word.capitalize())
            else:
                # 其他单词保持小写
                processed_words.append(word.lower())
    
    # 重新组合句子
    result = ' '.join(processed_words)
    return result

def process_markdown_file(filepath, proper_nouns, dry_run=False):
    """处理单个Markdown文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified_lines = []
        modified = False
        
        for line in lines:
            title_text = extract_title_text(line)
            
            if title_text:
                # 处理标题文本
                new_title_text = to_sentence_case(title_text, proper_nouns)
                
                if new_title_text != title_text:
                    # 重新构建标题行
                    match = re.match(r'^(#{1,6})\s+', line)
                    if match:
                        hashes = match.group(1)
                        new_line = f"{hashes} {new_title_text}\n"
                        modified_lines.append(new_line)
                        modified = True
                        
                        if dry_run:
                            print(f"  标题修改: '{title_text}' -> '{new_title_text}'")
                        else:
                            print(f"  {filepath}: '{title_text}' -> '{new_title_text}'")
                    else:
                        modified_lines.append(line)
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)
        
        # 如果文件有修改且不是干跑模式，则写回文件
        if modified and not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(modified_lines)
        
        return modified
        
    except Exception as e:
        print(f"处理文件 {filepath} 时出错: {e}")
        return False

def find_markdown_files(directory, extensions):
    """递归查找目录下的所有Markdown文件"""
    markdown_files = []
    
    for ext in extensions:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(f'.{ext}'):
                    filepath = os.path.join(root, file)
                    markdown_files.append(filepath)
    
    return markdown_files

def load_proper_nouns(filepath=None, fallback_to_default=True):
    """从文件加载专业名词列表，如果没有则使用默认列表"""
    proper_nouns = []
    
    # 默认的专业名词列表（可以作为后备）
    default_proper_nouns = [
        "Python", "JavaScript", "HTML", "CSS", "React", "Vue.js",
        "Node.js", "TypeScript", "Git", "GitHub", "Docker", "Kubernetes",
        "AWS", "Azure", "Linux", "Windows", "macOS", "iOS", "Android",
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
        "TensorFlow", "PyTorch", "OpenAI", "GPT", "API", "REST",
        "JSON", "XML", "YAML", "Markdown", "Jupyter", "NumPy", "Pandas"
    ]
    
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    noun = line.strip()
                    if noun:
                        proper_nouns.append(noun)
            print(f"从文件 {filepath} 加载了 {len(proper_nouns)} 个专业名词")
        except Exception as e:
            print(f"加载专业名词文件失败: {e}")
            if fallback_to_default:
                proper_nouns = default_proper_nouns
    elif fallback_to_default:
        proper_nouns = default_proper_nouns
    
    return proper_nouns

def save_proper_nouns(proper_nouns, filepath):
    """保存专业名词列表到文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for noun in sorted(set(proper_nouns)):
                f.write(f"{noun}\n")
        print(f"已将 {len(set(proper_nouns))} 个专业名词保存到 {filepath}")
        return True
    except Exception as e:
        print(f"保存专业名词列表失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='将Markdown文件中的标题转换为sentence case，同时保护专业名词'
    )
    parser.add_argument('directory', help='要处理的目录路径')
    parser.add_argument('-n', '--dry-run', action='store_true', 
                       help='干跑模式，只显示将要进行的修改而不实际执行')
    parser.add_argument('-p', '--proper-nouns', 
                       help='专业名词列表文件路径（每行一个专业名词）')
    parser.add_argument('-e', '--extensions', default='md,markdown',
                       help='要处理的文件扩展名，用逗号分隔（默认: md,markdown）')
    parser.add_argument('-s', '--scan-only', action='store_true',
                       help='仅扫描并提取专业名词，不进行修改')
    parser.add_argument('-o', '--output-proper-nouns',
                       help='将提取的专业名词保存到指定文件')
    parser.add_argument('--min-frequency', type=int, default=1,
                       help='专业名词最小出现频率（默认: 1）')
    parser.add_argument('--no-default-nouns', action='store_true',
                       help='不使用默认的专业名词列表')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误: 目录 '{args.directory}' 不存在")
        return
    
    # 处理文件扩展名
    extensions = [ext.strip().lower() for ext in args.extensions.split(',')]
    print(f"查找扩展名为 {extensions} 的文件...")
    
    # 第一步：收集所有标题和提取潜在专业名词
    print("正在扫描文件并提取标题...")
    all_titles, proper_noun_candidates = collect_all_titles_and_proper_nouns(args.directory, extensions)
    
    print(f"共扫描到 {len(all_titles)} 个标题")
    print(f"发现 {len(proper_noun_candidates)} 个潜在专业名词")
    
    # 显示最常见的候选专业名词
    print("\n最常见的候选专业名词:")
    for candidate, freq in proper_noun_candidates.most_common(20):
        print(f"  {candidate}: {freq} 次")
    
    # 第二步：过滤专业名词
    print(f"\n根据频率阈值 {args.min_frequency} 过滤专业名词...")
    extracted_proper_nouns = filter_proper_nouns(proper_noun_candidates, 
                                                 min_frequency=args.min_frequency)
    
    print(f"过滤后得到 {len(extracted_proper_nouns)} 个专业名词")
    
    # 第三步：加载用户提供的专业名词（如果有）
    user_proper_nouns = []
    if args.proper_nouns:
        user_proper_nouns = load_proper_nouns(args.proper_nouns, fallback_to_default=False)
    
    # 第四步：合并专业名词列表
    all_proper_nouns = list(set(extracted_proper_nouns + user_proper_nouns))
    
    # 第五步：如果需要，添加默认专业名词
    if not args.no_default_nouns and not args.proper_nouns:
        default_nouns = load_proper_nouns(None, fallback_to_default=True)
        all_proper_nouns = list(set(all_proper_nouns + default_nouns))
    
    print(f"\n总共使用 {len(all_proper_nouns)} 个专业名词进行保护:")
    for i, noun in enumerate(sorted(all_proper_nouns)[:30]):  # 只显示前30个
        print(f"  {noun}")
    if len(all_proper_nouns) > 30:
        print(f"  ... 还有 {len(all_proper_nouns) - 30} 个专业名词")
    
    # 保存专业名词到文件（如果指定）
    if args.output_proper_nouns:
        save_proper_nouns(all_proper_nouns, args.output_proper_nouns)
    
    # 如果只是扫描模式，则退出
    if args.scan_only:
        print("\n扫描完成，未进行任何修改。")
        if args.output_proper_nouns:
            print(f"专业名词列表已保存到 {args.output_proper_nouns}")
        return
    
    # 第六步：查找所有Markdown文件
    print(f"\n查找扩展名为 {extensions} 的文件...")
    markdown_files = find_markdown_files(args.directory, extensions)
    
    if not markdown_files:
        print(f"在目录 '{args.directory}' 中没有找到Markdown文件")
        return
    
    print(f"找到 {len(markdown_files)} 个Markdown文件")
    
    if args.dry_run:
        print("\n干跑模式 - 不会实际修改文件")
    
    # 第七步：处理文件
    print("\n开始处理文件...")
    modified_count = 0
    
    for i, filepath in enumerate(markdown_files, 1):
        print(f"[{i}/{len(markdown_files)}] 处理: {filepath}")
        
        if process_markdown_file(filepath, all_proper_nouns, args.dry_run):
            modified_count += 1
    
    print(f"\n处理完成!")
    print(f"总共处理了 {len(markdown_files)} 个文件")
    print(f"修改了 {modified_count} 个文件")
    
    if args.dry_run:
        print("\n注意: 这是在干跑模式下，没有实际修改任何文件。")
        print("要实际修改文件，请去掉 -n/--dry-run 参数")

if __name__ == "__main__":
    main()