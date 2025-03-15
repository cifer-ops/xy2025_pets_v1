from googletrans import Translator
import time

def translate_text_to_english(input_file, output_file):
    print(f"正在读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 将内容分成较小的块进行翻译，避免超出API限制
    chunk_size = 4000  # 每次翻译约4000个字符
    chunks = []
    for i in range(0, len(content), chunk_size):
        chunks.append(content[i:i+chunk_size])
    
    translator = Translator()
    translated_chunks = []
    
    print(f"开始翻译，总共 {len(chunks)} 个块")
    for i, chunk in enumerate(chunks):
        try:
            print(f"正在翻译第 {i+1}/{len(chunks)} 块...")
            # 使用googletrans进行翻译
            translated = translator.translate(chunk, src='zh-cn', dest='en')
            translated_chunks.append(translated.text)
            # 添加延迟以避免API限制
            time.sleep(2)
        except Exception as e:
            print(f"翻译第 {i+1} 块时出错: {str(e)}")
            # 如果翻译失败，保留原始文本
            translated_chunks.append(f"[TRANSLATION ERROR: {str(e)}]\n{chunk}")
            time.sleep(5)  # 出错后等待更长时间
    
    # 将所有翻译块合并
    translated_content = '\n'.join(translated_chunks)
    
    # 保存翻译结果
    print(f"保存翻译结果到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_content)
    
    print("翻译完成！")

if __name__ == "__main__":
    input_file = "宠物领养平台系统论文_纯文本.txt"
    output_file = "Pet_Adoption_Platform_System_English.txt"
    translate_text_to_english(input_file, output_file) 