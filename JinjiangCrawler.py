from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re

fieldnames = [
    'book_id', 
    'book_name', 
    'author', 
    'NonVIP_average_click', 
    'reviews_num', 
    'collected_num', 
    'nutrient_num', 
    'genre', 
    'perspective', 
    'progress', 
    'contract_status',
    'credits',
    'chapter_launch_time',
    'total_word_count'  # 新增字段
]



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

        try:
            # 使用JavaScript直接获取非v章节章均点击数的文本
            NonVIP_average_click_text = driver.execute_script(
                "return document.querySelector('span#totleclick').textContent.trim();")
            book_data['NonVIP_average_click'] = int(NonVIP_average_click_text)

        except Exception as e:
            print(f"Failed to retrieve non-VIP average click count for URL {url}: {e}")
            book_data['NonVIP_average_click'] = None  # 或者设置为0或其他默认值

        try:
            # 使用JavaScript获取包含积分的div的文本，通过定位class为'sptd'的td的子div元素
            credits_text = driver.execute_script(
                "return document.querySelector('td.sptd > div[align=\"center\"]').textContent;")
            
            # 使用正则表达式查找其中的数字（假设积分总是由逗号分隔的数字）
            credits_match = re.search(r'文章积分：([\d,]+)', credits_text)
            if credits_match:
                # 将找到的数字字符串中的逗号去除，并转换为整数
                credits = int(credits_match.group(1).replace(',', ''))
                book_data['credits'] = credits
            else:
                book_data['credits'] = 0  # 如果没有找到匹配项，设置默认值为0

        except Exception as e:
            print(f"Failed to retrieve credits for URL {url}: {e}")
            book_data['credits'] = 0  # 如果出现异常，也设置为默认值


        try:
            # 使用JavaScript获取总书评数
            reviews_num_text = driver.execute_script(
                "return document.querySelector('span[itemprop=\"reviewCount\"]').textContent.trim();")
            book_data['reviews_num'] = int(reviews_num_text)
        except Exception as e:
            print(f"Failed to retrieve review numbers for URL {url}: {e}")
            book_data['reviews_num'] = None  # 或设置为默认值

        try:
            # 使用JavaScript获取当前被收藏数
            collected_num_text = driver.execute_script(
                "return document.querySelector('span[itemprop=\"collectedCount\"]').textContent.trim();")
            book_data['collected_num'] = int(collected_num_text)
        except Exception as e:
            print(f"Failed to retrieve collected count for URL {url}: {e}")
            book_data['collected_num'] = None  # 或设置为默认值

        try:
            # 使用JavaScript获取营养液数
            nutrient_num_text = driver.execute_script(
                "return document.querySelector('div[align=\"center\"] span:nth-child(4)').textContent.trim();")
            book_data['nutrient_num'] = int(nutrient_num_text)
        except Exception as e:
            print(f"Failed to retrieve nutrient number for URL {url}: {e}")
            book_data['nutrient_num'] = None  # 或设置为默认值



                
        
        # 获取文章类型
        genre_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='genre']")))
        book_data['genre'] = genre_span.text.strip()

        # 获取作品视角
        perspective_span = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='righttd']/ul/li[2]")))
        book_data['perspective'] = perspective_span.text.split('：')[-1].strip()
        

        # 获取文章进度
        status_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='updataStatus']")))
        status_text = status_span.text.strip()
        if status_text == "连载":
            book_data['progress'] = 0
        elif status_text == "完结":
            book_data['progress'] = 1
        else:
            book_data['progress'] = -1
        """

        # 获取版权转换
        copyright_span = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='righttd']/ul/li[6]/span[2]")))
        copyright_text = copyright_span.text.strip()
        if "尚未出版" in copyright_text:
            book_data['copyright'] = 0
        else:
            book_data['copyright'] = 1
        """

        # 获取签约状态
        contract_span = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='righttd']/ul/li[7]/b/font")))
        contract_text = contract_span.text.strip()
        if contract_text == "已签约":
            book_data['contract_status'] = 1
        else:
            book_data['contract_status'] = 0

        try:
            # 使用JavaScript获取包含时间信息的td元素的title属性
            chapter_time_text = driver.execute_script(
                "return document.querySelector('tr[itemprop=\"chapter\"] td[title]').getAttribute('title');")
            
            # 使用正则表达式从title属性中提取“章节首发时间”
            chapter_launch_time_match = re.search(r'章节首发时间：([\d\- :]+)', chapter_time_text)
            if chapter_launch_time_match:
                chapter_launch_time = chapter_launch_time_match.group(1)
                book_data['chapter_launch_time'] = chapter_launch_time  # 存储到book_data中
            else:
                book_data['chapter_launch_time'] = 'Unavailable'  # 如果未找到时间，使用默认值

        except Exception as e:
            print(f"Failed to retrieve chapter launch time for URL {url}: {e}")
            book_data['chapter_launch_time'] = 'Error'  # 如果出现异常，设置为错误标志


        try:
            # 获取全文字数
            total_word_count_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='wordCount']")))
            total_word_count_text = total_word_count_span.text.strip()
            
            # 提取数字部分
            total_word_count = ''.join(filter(str.isdigit, total_word_count_text))
            book_data['total_word_count'] = int(total_word_count) if total_word_count else 0

        except Exception as e:
            print(f"Failed to retrieve total word count for URL {url}: {e}")
            book_data['total_word_count'] = 0  # 如果出现异常，设置为0


        return book_data

    except Exception as e:
        print(f"Error while processing URL {url}: {e}")
        return None

count = 0

with open('JinjiangBooksNew.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:  # 如果文件为空，则写入表头
        writer.writeheader()

    for book_id in range(3610733, 6581942, 4):  # 示例中仅爬取前100本书
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
