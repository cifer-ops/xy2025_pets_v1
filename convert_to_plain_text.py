import re

# 读取markdown格式的文本文件
with open('论文.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 处理Markdown格式
def convert_markdown_to_plain_text(markdown_text):
    # 处理标题
    plain_text = re.sub(r'# (.*?)$', r'\1\n', markdown_text, flags=re.MULTILINE)
    plain_text = re.sub(r'## (.*?)$', r'\1\n', plain_text, flags=re.MULTILINE)
    plain_text = re.sub(r'### (.*?)$', r'\1\n', plain_text, flags=re.MULTILINE)
    plain_text = re.sub(r'#### (.*?)$', r'\1\n', plain_text, flags=re.MULTILINE)
    
    # 处理列表项
    plain_text = re.sub(r'- (.*?)$', r'• \1', plain_text, flags=re.MULTILINE)
    plain_text = re.sub(r'\* (.*?)$', r'• \1', plain_text, flags=re.MULTILINE)
    
    # 处理表格（仅保留内容，用空格分隔）
    lines = plain_text.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 如果是表格行
        if line.startswith('|') and i + 1 < len(lines) and lines[i+1].startswith('|'):
            # 提取表格内容
            header_cells = [cell.strip() for cell in line.split('|')[1:-1]]
            processed_lines.append('  '.join(header_cells))
            
            # 跳过分隔行
            i += 1
            
            # 处理数据行
            i += 1
            while i < len(lines) and lines[i].startswith('|'):
                row_cells = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                processed_lines.append('  '.join(row_cells))
                i += 1
            
            # 由于我们已经处理了当前行，需要减1以抵消后面的i+=1
            i -= 1
        else:
            processed_lines.append(line)
        
        i += 1
    
    # 重建文本
    plain_text = '\n'.join(processed_lines)
    
    # 删除链接格式，只保留链接文本
    plain_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', plain_text)
    
    # 删除图片
    plain_text = re.sub(r'!\[.*?\]\(.*?\)', '', plain_text)
    
    # 删除粗体和斜体
    plain_text = re.sub(r'\*\*(.*?)\*\*', r'\1', plain_text)
    plain_text = re.sub(r'\*(.*?)\*', r'\1', plain_text)
    plain_text = re.sub(r'__(.*?)__', r'\1', plain_text)
    plain_text = re.sub(r'_(.*?)_', r'\1', plain_text)
    
    # 删除代码块
    plain_text = re.sub(r'```.*?```', '', plain_text, flags=re.DOTALL)
    
    # 删除行内代码
    plain_text = re.sub(r'`(.*?)`', r'\1', plain_text)
    
    return plain_text

# 转换内容
plain_text_content = convert_markdown_to_plain_text(content)

# 保存为纯文本文件
with open('宠物领养平台系统论文_纯文本.txt', 'w', encoding='utf-8') as file:
    file.write(plain_text_content)

print('转换完成，已保存为"宠物领养平台系统论文_纯文本.txt"') 