import pandas as pd
import jieba
import jieba.analyse

# 加载CSV文件
df = pd.read_csv('QidianBooks.csv')

# 选取book_intro_detail列
text_series = df['book_intro_detail']

# 设置jieba的TF-IDF关键词提取
jieba.analyse.set_idf_path("/path/to/your/idf.txt")  # 如果有自定义的IDF文件，可以设置路径

# 提取每段话的关键词
keywords_list = []
for text in text_series:
    # 使用TF-IDF算法提取关键词，这里提取前5个关键词
    keywords = jieba.analyse.extract_tags(text, topK=5)
    keywords_list.append(keywords)

# 将关键词结果添加到DataFrame
df['keywords'] = keywords_list

# 显示更新后的DataFrame
print(df[['book_intro_detail', 'keywords']])
