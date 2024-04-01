from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

fieldnames = ['book_id', 'book_name', 'author', 'NonVIP_average_click', 'reviews_num', 'collected_num', 'nutrient_num', 'credits']

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)

def get_one_book(url):
    book_data = {}
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 2)
        
        # 检查是否存在提示文本“该文不存在或者已经删除”
        error_element = driver.find_elements(By.CSS_SELECTOR, "center[style='font-size:16px;color:red;font-weight:bold;margin-top:20px']")
        if error_element:
            return None
        
        # 获取书名
        book_name_tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
        book_data['book_name'] = book_name_tag.text.strip()

        # 获取作者
        author_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='author']")))
        book_data['author'] = author_span.text.strip()

        """
        print("hello")
        # 获取非v章节章均点击数
        NonVIP_average_click_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span#totleclick")))
        book_data['NonVIP_average_click'] = int(NonVIP_average_click_span.text.strip())

        # 获取总书评数
        reviews_num_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='reviewCount']")))
        book_data['reviews_num'] = int(reviews_num_span.text.strip())

        # 获取当前被收藏数
        collected_num_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='collectedCount']")))
        book_data['collected_num'] = int(collected_num_span.text.strip())

        # 获取营养液数
        nutrient_num_span = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@align='center']/span[4]")))
        book_data['nutrient_num'] = int(nutrient_num_span.text.strip())

        # 获取积分
        credits_div = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@align='center' and contains(text(), '文章积分')]")))
        credits_text = credits_div.text.strip()
        credits = [int(s.replace(',', '')) for s in credits_text.split() if s.isdigit()][0]
        """

        # 获取非v章节章均点击数
        NonVIP_average_click_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span#totleclick")))
        book_data['NonVIP_average_click'] = int(NonVIP_average_click_span.text.strip())

        # 获取总书评数
        reviews_num_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='reviewCount']")))
        book_data['reviews_num'] = int(reviews_num_span.text.strip())

        # 获取当前被收藏数
        collected_num_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='collectedCount']")))
        book_data['collected_num'] = int(collected_num_span.text.strip())
        
        # 获取营养液数
        nutrient_num_span = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@align='center']/span[4]")))
        book_data['nutrient_num'] = int(nutrient_num_span.text.strip())


        return book_data

    except Exception as e:
        print(f"Error while processing URL {url}: {e}")
        return None

count = 0

with open('JinjiangBooks.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:  # 如果文件为空，则写入表头
        writer.writeheader()

    for book_id in range(113782, 113800 + 1):  # 示例中仅爬取前100本书
        url = f"http://www.jjwxc.net/onebook.php?novelid={book_id}"
        book_data = get_one_book(url)
        if book_data:
            book_data['book_id'] = book_id
            print(f"{book_id}爬取成功")
            writer.writerow(book_data)
            count += 1
        else:
            print(f"{book_id}无法爬取或不存在")

print("--------------------------------")
print(f"总计爬取{count}本书")
