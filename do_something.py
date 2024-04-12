import pandas as pd

# 读取CSV文件
df = pd.read_csv('QidianBooks.csv')

# 打印行数
print(f"总共有 {len(df)} 行")
