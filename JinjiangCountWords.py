import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# 读取现有的CSV文件
with open('JinjiangBooks.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    books = list(reader)

# 更新每条记录，添加总字数
for book in books:
    book_id = book['book_id']
    url = f"http://www.jjwxc.net/onebook.php?novelid={book_id}"
    try:
        driver.get(url)
        # 定位并获取总字数
        total_word_count_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='wordCount']")))
        total_word_count_text = total_word_count_span.text.strip()
        total_word_count = ''.join(filter(str.isdigit, total_word_count_text))
        book['total_word_count'] = int(total_word_count) if total_word_count else 0
    except Exception as e:
        print(f"Failed to retrieve total word count for book ID {book_id}: {e}")
        book['total_word_count'] = 0

driver.quit()

# 写入新的CSV文件
new_fieldnames = reader.fieldnames + ['total_word_count']  # 添加新列
with open('UpdatedOldJinjiangBooksWithWordCount.csv', 'w', newline='', encoding='utf-8') as new_csvfile:
    writer = csv.DictWriter(new_csvfile, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(books)

print("CSV file has been updated with total word counts.")
