import csv

# 打开第一个文件并读取数据
with open('UpdatedOldJinjiangBooksWithWordCount.csv', 'r', newline='', encoding='utf-8') as file1:
    reader1 = csv.DictReader(file1)
    data = list(reader1)  # 将第一个文件的数据读取到列表中

# 打开第二个文件并追加数据
with open('CleanedJinjiangBooksNew.csv', 'r', newline='', encoding='utf-8') as file2:
    reader2 = csv.DictReader(file2)
    data.extend(list(reader2))  # 将第二个文件的数据追加到列表中

# 写入新的CSV文件，合并后的数据
with open('MergedJinjiangBooks.csv', 'w', newline='', encoding='utf-8') as merged_file:
    fieldnames = reader1.fieldnames  # 假设两个文件有相同的字段
    writer = csv.DictWriter(merged_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)  # 写入合并后的数据

print("CSV files have been merged successfully.")
