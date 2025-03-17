import os
import re
import sys
import argparse
from googletrans import Translator
import time
from tqdm import tqdm
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("translation.log"),
        logging.StreamHandler()
    ]
)

def is_binary_file(file_path):
    """Check if file is binary"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return False
    except UnicodeDecodeError:
        return True

def is_translatable_file(file_path):
    """Check if the file should be translated based on extension"""
    extensions = ['.py', '.html', '.txt', '.md', '.css', '.js']
    return any(file_path.endswith(ext) for ext in extensions)

def translate_text(text, translator):
    """Translate text from Chinese to English"""
    if not text.strip():
        return text
        
    # Skip if the text doesn't contain any Chinese characters
    if not re.search('[\u4e00-\u9fff]', text):
        return text
        
    try:
        # Add delay to avoid API throttling
        time.sleep(0.5)
        translation = translator.translate(text, src='zh-cn', dest='en')
        return translation.text
    except Exception as e:
        logging.error(f"Translation error: {e} for text: {text[:30]}...")
        return text

def translate_python_file(file_path, translator):
    """Translate a Python file"""
    logging.info(f"Translating Python file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Make a backup of the original file
        with open(f"{file_path}.bak", 'w', encoding='utf-8') as backup:
            backup.write(content)
        
        # Translate comments (# ...)
        content = re.sub(
            r'(#\s*)(.*[\u4e00-\u9fff].*)',
            lambda match: match.group(1) + translate_text(match.group(2), translator),
            content
        )
        
        # Translate docstrings (""" ... """)
        content = re.sub(
            r'(""")(.*?)(""")',
            lambda match: match.group(1) + translate_text(match.group(2), translator) + match.group(3),
            content, 
            flags=re.DOTALL
        )
        
        # Translate single and double quoted strings containing Chinese
        content = re.sub(
            r'([\'"])(.*?[\u4e00-\u9fff].*?)([\'"])',
            lambda match: match.group(1) + translate_text(match.group(2), translator) + match.group(3),
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        logging.info(f"Successfully translated: {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error translating {file_path}: {e}")
        return False

def translate_html_file(file_path, translator):
    """Translate an HTML file"""
    logging.info(f"Translating HTML file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Make a backup of the original file
        with open(f"{file_path}.bak", 'w', encoding='utf-8') as backup:
            backup.write(content)
        
        # Translate text between tags
        content = re.sub(
            r'(>)(.*?[\u4e00-\u9fff].*?)(<)',
            lambda match: match.group(1) + translate_text(match.group(2), translator) + match.group(3),
            content,
            flags=re.DOTALL
        )
        
        # Translate attributes
        content = re.sub(
            r'(\w+=[\'"])(.*?[\u4e00-\u9fff].*?)([\'"])',
            lambda match: match.group(1) + translate_text(match.group(2), translator) + match.group(3),
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        logging.info(f"Successfully translated: {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error translating {file_path}: {e}")
        return False

def translate_text_file(file_path, translator):
    """Translate a text file line by line"""
    logging.info(f"Translating text file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Make a backup of the original file
        with open(f"{file_path}.bak", 'w', encoding='utf-8') as backup:
            backup.writelines(lines)
        
        translated_lines = []
        for line in lines:
            if re.search('[\u4e00-\u9fff]', line):
                # Only translate lines that contain Chinese characters
                translated_lines.append(translate_text(line, translator))
            else:
                translated_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(translated_lines)
        
        logging.info(f"Successfully translated: {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error translating {file_path}: {e}")
        return False

def translate_file(file_path, translator):
    """Translate a file based on its extension"""
    if file_path.endswith('.py'):
        return translate_python_file(file_path, translator)
    elif file_path.endswith('.html'):
        return translate_html_file(file_path, translator)
    elif file_path.endswith('.txt') or file_path.endswith('.md'):
        return translate_text_file(file_path, translator)
    else:
        # For other text files, just translate all Chinese text
        logging.info(f"Translating other text file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Make a backup of the original file
            with open(f"{file_path}.bak", 'w', encoding='utf-8') as backup:
                backup.write(content)
            
            # Translate any text containing Chinese characters
            content = re.sub(
                r'(.*[\u4e00-\u9fff].*)',
                lambda match: translate_text(match.group(1), translator),
                content
            )
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            logging.info(f"Successfully translated: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Error translating {file_path}: {e}")
            return False

def traverse_directory(directory, translator, exclude_dirs=None, limit=None):
    """Recursively traverse directory and translate files"""
    if exclude_dirs is None:
        exclude_dirs = ['.git', '.venv', '__pycache__', 'media', 'static/fonts', 'static/images', '.idea']
    
    all_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            if file.endswith('.bak'):  # Skip backup files
                continue
                
            file_path = os.path.join(root, file)
            if is_translatable_file(file_path) and not is_binary_file(file_path):
                all_files.append(file_path)
    
    logging.info(f"Found {len(all_files)} files to translate")
    
    # Limit the number of files to translate if specified
    if limit and limit > 0:
        all_files = all_files[:limit]
        logging.info(f"Limited to translating {limit} files")
    
    successful = 0
    failed = 0
    
    for file_path in tqdm(all_files):
        logging.info(f"Processing {file_path}")
        try:
            result = translate_file(file_path, translator)
            if result:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            logging.error(f"Error translating {file_path}: {e}")
            failed += 1
    
    logging.info(f"Translation complete: {successful} successful, {failed} failed")

def main():
    parser = argparse.ArgumentParser(description='Translate Django project from Chinese to English')
    parser.add_argument('--directory', type=str, default='.', help='Directory to traverse')
    parser.add_argument('--file', type=str, help='Single file to translate')
    parser.add_argument('--limit', type=int, help='Limit the number of files to translate')
    args = parser.parse_args()
    
    translator = Translator()
    
    if args.file:
        if os.path.exists(args.file):
            translate_file(args.file, translator)
        else:
            logging.error(f"File not found: {args.file}")
    else:
        traverse_directory(args.directory, translator, limit=args.limit)

if __name__ == '__main__':
    main() 