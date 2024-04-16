import math

# 假设这是文档总数
total_documents = 1000

# 假设这是各个词在多少不同文档中出现过的统计
word_document_counts = {
    '词语1': 100,
    '词语2': 150,
    '词语3': 250,
    '词语4': 50,
}

# 计算IDF值并写入文件
with open('idf.txt', 'w', encoding='utf-8') as file:
    for word, count in word_document_counts.items():
        idf = math.log((total_documents + 1) / (count + 1))
        file.write(f'{word} {idf}\n')
