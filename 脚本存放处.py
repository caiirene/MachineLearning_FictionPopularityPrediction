import pandas as pd

# 定义原始文件路径和新文件路径
input_file_path = 'JinjiangBooks.csv'  # 需要替换成您的实际路径
output_file_path = 'CorrectedJinjiangBooks.csv'  # 输出文件的路径

# 读取CSV文件
data = pd.read_csv(input_file_path, header=None)  # 不使用自动列名

# 定义正确的列名顺序
correct_columns = [
    'book_id', 'book_name', 'author', 'NonVIP_average_click',
    'reviews_num', 'collected_num', 'nutrient_num', 'credits',
    'genre', 'perspective', 'progress', 'contract_status',
    'chapter_launch_time', 'total_word_count'
]

# 为所有数据设置统一的列名
data.columns = correct_columns

# 分割数据为正确的部分和错误的部分
correct_data = data.iloc[:7609]
incorrect_data = data.iloc[7609:]

# 错误的列顺序（从7610行开始，假设您已知道错误的具体列顺序）
error_columns = [
    'book_id', 'book_name', 'author', 'NonVIP_average_click',
    'reviews_num', 'collected_num', 'nutrient_num', 'genre',
    'perspective', 'progress', 'contract_status', 'credits',
    'chapter_launch_time', 'total_word_count'
]

# 为错误数据部分设置临时列名，并按照正确的顺序重排
incorrect_data.columns = error_columns
incorrect_data = incorrect_data[correct_columns]

# 合并两部分数据
corrected_data = pd.concat([correct_data, incorrect_data], ignore_index=True)

# 将合并后的数据保存到新的CSV文件
corrected_data.to_csv(output_file_path, header=False, index=False, encoding='utf-8-sig')

print("Data has been corrected and saved to", output_file_path)
